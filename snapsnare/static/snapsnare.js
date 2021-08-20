var context;
window.addEventListener('load', init, false);
function init() {
  try {
    // Fix up for prefixing
    window.AudioContext = window.AudioContext||window.webkitAudioContext;
    context = new AudioContext();

    console.log('audio context created')
  }
  catch(e) {
    alert('Web Audio API is not supported in this browser');
  }
}

var flow_ext = {
    init: function() {
        console.log("flow_ext.init");
    },
};


function muis() {
    console.log('muis exectuded')
}