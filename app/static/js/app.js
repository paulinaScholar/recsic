// console.log("Hello");
setTimeout(postSong, 100);

function postSong(){
    console.log("Working")
    
    var button = document.getElementById("songlist")
    
    button.style.display = "block";
    }


function nothing(){
    console.log("Not Working")
    
    var button = document.getElementById("noSong")
    
    button.style.display = "block";
    }