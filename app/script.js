var canvas = HTMLElement;
var ctx = CanvasRenderingContext2D

function onload() {
    canvas = document.getElementById("screen");
    ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight-500;

    canvas.addEventListener("touchmove", onmove);
    window.addEventListener("resize", onrotation);
    window.addEventListener("devicemotion", onmotion);
    var elem = document.getElementById("text");
    
    elem.innerHTML = window.DeviceOrientationEvent;
}

function onmove(evt) {
    evt.preventDefault();

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var touches = evt.changedTouches;
    console.log(evt);

    ctx.beginPath();

    var pos = evt.target.getBoundingClientRect();
    var X = pos.left + window.pageXOffset;
    var Y = pos.top  + window.pageYOffset;

    for(var i=0; i<touches.length; i++) {
        ctx.arc(touches[i].pageX - X, touches[i].pageY - Y, 10, 0, 2*Math.PI);
        ctx.fillStyle = "rgb(255, 255, 255)";
        ctx.fill();
    }

    ctx.closePath();
}

function onrotation() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight-500;

    console.log(window.innerWidth, window.innerHeight);
}

function onmotion(event) {
    var elem = document.getElementById("text");
    
    elem.innerHTML = window.DeviceOrientationEvent;
    //elem.innerHTML = String(event.accelerationIncludingGravity.x);
    //ctx.clearRect(0, 0, canvas.width, canvas.height);
    //ctx.font = "50px sans-serif";
    //ctx.fillText(String(event.alpha), 100, 500);
}