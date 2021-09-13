var slider1 = HTMLElement;
var slider2 = HTMLElement;
var h1 = HTMLElement;
var w = new WebSocket("ws://raspberrypi.local:8080");

function onload() {
    h1 = document.getElementById("val");
    slider1 = document.getElementById("slider1");
    slider2 = document.getElementById("slider2");

    w.addEventListener("open", onsocketopen);
    slider1.addEventListener("touchmove", touchmove);
    slider2.addEventListener("touchmove", touchmove);
}

function touchmove(e){
    e.preventDefault();
    var touch = TouchEvent;
    
    for(var i=0; i<e.changedTouches.length; i++) {
        if(e.target.id == e.changedTouches[i].target.id) {
            touch = e.changedTouches[i];
        }
    }
    var rect = e.target.getBoundingClientRect();
    var X = rect.left + window.pageXOffset;
    var Y = rect.top + window.pageYOffset;

    var x = touch.clientX - X;
    var y = touch.clientY - Y;

    if(e.target.id == "slider1") {
        var val = (e.target.clientWidth - y) / e.target.clientWidth * 100;
    }else if(e.target.id == "slider2") {
        var val = x / e.target.clientWidth * 100;
    }
    e.target.value = val;
    w.send(e.target.id + ": " + String(Math.min(Math.max(val, 0), 100)));
}

function onsocketopen(event) {
    console.log("[Connected]");
    w.send("ready");
}
