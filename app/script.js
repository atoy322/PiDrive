var slider1 = HTMLElement;
var slider2 = HTMLElement;
var h1 = HTMLElement;
var head = false;
var back = false;
var w = new WebSocket("ws://raspberrypi.local:8080");

function onload() {
    h1 = document.getElementById("val");
    btn1 = document.getElementById("head");
    btn2 = document.getElementById("back");
    slider1 = document.getElementById("slider1");
    slider2 = document.getElementById("slider2");

    w.addEventListener("open", onsocketopen);
    w.addEventListener("close", onsocketclose);
    slider1.addEventListener("touchmove", touchmove);
    slider2.addEventListener("touchmove", touchmove); 
    slider1.addEventListener("touchend", touchend);
    slider2.addEventListener("touchend", touchend);
    btn1.addEventListener("touchstart", onclick);
    btn2.addEventListener("touchstart", onclick);
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

function touchend(e) {
    w.send("slider1: 50");
    w.send("slider2: 50");
    e.target.value = 50;
}

function onsocketopen(event) {
    console.log("[Connected]");
    w.send("ready");
}

function onsocketclose(event) {
    console.log("[Closed]");
    alert("Connection closed");
}

function onclick(e) {
    if(e.target.id == "head") {
        if(head) {
            w.send("head: 0");
            head = false;
        }else{
            w.send("head: 1");
            head = true;
        }
    }else if(e.target.id == "back") {
        if(back) {
            w.send("back: 0");
            back = false;
	}else{
            w.send("back: 1");
            back = true;
        }
    }
}

