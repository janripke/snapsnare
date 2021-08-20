var nodes = [];

var audio = {
    init: function() {
        console.log("audio.init");

        audio.config = {
            nodes: [],
        }
    },
    play: function( id ) {
        var audioElement = document.getElementById(id);
        audioElement.loop=true;
        audioElement.play();
        console.log(audioElement);
        console.log("audio.play");
    },
    pause: function( id ) {
        var audioElement = document.getElementById(id);
        audioElement.pause();
        console.log(audioElement);
        console.log("audio.pause");
    },
    stop: function( id ) {
        var audioElement = document.getElementById(id);
        audioElement.currentTime=0;
        audioElement.pause();
        console.log(audioElement);
        console.log("audio.stop");
    },
    playing: function( id ) {
        console.log("audio.playing");
    },

};


audio.init();