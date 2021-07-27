function onload() {
    var canvas = document.getElementById("screen");
    var ctx = canvas.getContext("2d");

    canvas.addEventListener("touchmove", onmove, false);

    //ctx.line(0, 0, 100, 100);
}

function onmove(evt) {
    var canvas = document.getElementById("screen");
    var ctx = canvas.getContext("2d");

    evt.preventDefault();

    ctx.clearRect(0, 0, 500, 500);
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