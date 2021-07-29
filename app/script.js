function onload() {
    var h1 = document.getElementById("val");
    var slider1 = document.getElementById("slider1");
    var slider2 = document.getElementById("slider2");

    slider1.addEventListener("touchmove", (e)=>{
        e.preventDefault();
        h1.innerHTML = e.target.value;
        
        var touch = e.changedTouches[0];
        var rect = e.target.getBoundingClientRect();
        var X = rect.left + window.pageXOffset;
        var Y = rect.top + window.pageYOffset;

        var x = touch.clientX - X;
        var y = touch.clientY - Y;

        var val = (e.target.clientWidth - y) / e.target.clientWidth * 100;
        e.target.value = val;
        slider2.value = val;
    });
}