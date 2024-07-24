from app import app
from flask import render_template, request, redirect
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Route to main page

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/recommend/', methods=["GET", "POST"])
def recommend():
    if request.method == "POST":
        songRequest = request.form.get('song_input')
        # print(songRequest)
        data = readData(songRequest)

        return render_template('recommend.html', tblRec=[data.to_html()], titles=[''])

    return render_template('recommend.html')

def readData(songRequest):
    df = pd.read_csv('Spotify_Song_Attributes.csv')
    
    df = df.drop(['msPlayed', 'type', 'id', 'analysis_url', 'uri', 'track_href', 'duration_ms'], 
             axis='columns')
    df = df.replace('NaN', pd.NA)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    #* Data preparation
        #* Get rid of spaces in between artist and apply lower case
    df["trackName"] = df["trackName"].str.lower()
    df["artistName"] = df["artistName"].str.lower()
    df["genre"] = df["genre"].str.lower()

        #* Combine all columns and assgin as new column
    df["data"] = df.apply(lambda value: " ".join(value.astype("str")), axis=1)

    #* Models
    vectorizer = CountVectorizer()
    vectorized = vectorizer.fit_transform(df["data"])
    similarities = cosine_similarity(vectorized)

    #* Assign new dataframe with 'similarities' values
    df_tmp = pd.DataFrame(similarities, columns=df["trackName"], index=df["trackName"]).reset_index()
    df_tmp = pd.merge(df_tmp, df[['trackName', 'artistName']], on='trackName', how='left')

    true = True
    while true:
         #* Asking the user for a song
        while True:
            input_song = songRequest

            if input_song in df_tmp.columns:
                recommendation = df_tmp.nlargest(11, input_song)[["trackName", "artistName"]]
                return recommendation
                break
            
            else:
                # No song found
                true = False
                # return False
                break
        
        for song in recommendation.values[1:]:
            print(song)

        print("\n")
        true = False