var ws;
var host = window.location.hostname;
var hostip = host.replace("http://","").replace("https://","")
var ws
var wslinked = false
var worker
var mouseMoveReady=true
var mouseMode=0
var debug=0
var debugstr=""
function linkws(addr) {
    if(!"Websocket" in window){
        alert("Your browser doesn't support websocket. Please use a browser with websocket support.")
        return
    }
    ws = new WebSocket(addr);
    ws.onmessage = function (messageEvent) {
        var message=messageEvent.data;
        if (debug) console.log("<- "+message);
        if(message.startsWith("keyPressed ")){
            onKeyPressed(message.slice(start=10));
        }
    }
    ws.onopen = function () {
        wslinked=true
        document.getElementById("wsstatus").style.setProperty("color","lime")
        setTimeout("getPressed()",2000);
    }
    ws.onclose = function () {
        wslinked=false
        document.getElementById("wsstatus").style.setProperty("color","red")
    }
}
function wssend(message){
    if(wslinked){
    ws.send(message);
    debugstr="-> "+message;
    if(debug) console.log("-> "+message);}
    else
    reconnect();
}
function pressKey(key,press=2) {
    wssend("pressKey "+key+" "+press);
}
function mouseAbsolute(x,y,wheel=0) {
    wssend("mouseAbsolute "+x+" "+y+" "+wheel);
}
function mouseRelative(x,y,wheel=0) {
    wssend("mouseRelative "+x+" "+y+" "+wheel);
}
function pressMouse(key,press) {
    wssend("pressMouse "+key+" "+press);
}
function mousePressButtons(buttons) {
    wssend("mousePressButtons "+buttons);
}
function releaseAll() {
    wssend("releaseAll");
}
function getPressed() {
    wssend("getPressed");
}
function getInfo() {
    wssend("getInfo");
}


function onKeyPressed(message=""){
    var pressedKeys=message.split(" ");
    var keyboard = document.getElementById("keyboard");
    var buttons=keyboard.getElementsByTagName("button");
    for (i in buttons) {
        // var button2 = document.getElementById("keyboard_"+pressedKeys[i]);
        var button=buttons[i]
        if(button.id && button.id.startsWith("keyboard_")){
            var name=button.id.replace("keyboard_","")
            if(pressedKeys.includes(name)){
                // button.style.backgroundColor="#5599FF";
                // button.style.color="#FFFFFF";
                button.classList.add("activekey")
            }else{
                // button.style.backgroundColor="#F0F0F0";
                // button.style.color="#000000";
                button.classList.remove("activekey")
            }
        }
    }
}
function onPressKey(event=new TouchEvent()){
    if(event.type.startsWith("touch")) event.preventDefault()
    if(event.target.id.startsWith("keyboard_")){
        var key=event.target.id.replace("keyboard_","")
        console.log(key)
        if(event.type=="touchstart" || event.type=="mousedown") {
            pressKey(key,1)
        }
        else if(event.type=="touchend" || event.type=="touchcancel" || event.type=="mouseup") {
            pressKey(key,0)
        }
    }
}
function onWheel(event=new WheelEvent()){
    event.preventDefault()
    debugstr=event.deltaX+","+event.deltaY+","+event.deltaZ+","
    if(event.deltaY>0) mouseRelative(0,0,-1)
    if(event.deltaY<0) mouseRelative(0,0,1)
}
function onMouseDrag(event=new MouseEvent()){
    event.preventDefault()
    var stream = document.getElementById("stream")
    var mouseX=event.offsetX/stream.width
    var mouseY=event.offsetY/stream.height
    var button=0
    var immediate=false
    if(event.button==1) button=2
    else if(event.button==2) button=1
    else button=event.button
    if(event.type=="mousedown"){pressMouse(button,1);immediate=true;}
    if(event.type=="mouseup"){pressMouse(button,0);immediate=true;}
    if(mouseMode==1){
        mouseAbs(mouseX,mouseY,immediate)
    }else{
        mouseRelOffset(event.movementX,event.movementY,immediate)
    }
}
var lastTouchX=0
var lastTouchY=0
function onTouchDrag(event=new TouchEvent()){
    var button
    var immediate=false
    if(event.type=="touchstart" || event.type=="touchend") immediate=true;
    if(event.targetTouches.length==0) button=0
    else if(event.targetTouches.length==1) {
        button=1
        event.preventDefault()
    }
    else if(event.targetTouches.length==2) button=10
    else if(event.targetTouches.length==3) button=100
    else if(event.targetTouches.length==4) button=1000
    else if(event.targetTouches.length>=5) button=10000
    // if(event.type=="touchend" || event.type=="touchcancel"){
    // }
    if(mouseMode==1) mousePressButtons(button)
    if(event.targetTouches.length>=1){
        var touch = event.targetTouches[0]
        var stream = document.getElementById("stream")
        var touchX=touch.pageX-stream.offsetLeft
        var touchY=touch.pageY-stream.offsetTop
        if(mouseMode==1){
            var mouseX=touchX/stream.width
            var mouseY=touchY/stream.height
            mouseAbs(mouseX,mouseY,immediate)
        }else if(mouseMode==0){
            if(event.type=="touchstart"){
                lastTouchX=touchX
                lastTouchY=touchY
            }
            mouseRelOffset(touchX-lastTouchX,touchY-lastTouchY,immediate)
            lastTouchX=touchX
            lastTouchY=touchY
        }
    }
}
function mouseAbs(x,y,immediate=false){
    if(!mouseMoveReady && !immediate) return;
    mouseMoveReady=false;
    var x=Math.max(0,Math.min(1,x))
    var y=Math.max(0,Math.min(1,y))
    mouseAbsolute(Math.floor(x*4095),Math.floor(y*4095),0);
}
var mouseRelativeX=0
var mouseRelativeY=0
function mouseRelOffset(x,y,immediate=false){
    mouseRelativeX=mouseRelativeX+x;
    mouseRelativeY=mouseRelativeY+y;
    if(mouseMoveReady || immediate){
        mouseRelative(Math.floor(mouseRelativeX),Math.floor(mouseRelativeY),0);
        mouseRelativeX=0
        mouseRelativeY=0
        mouseMoveReady=false;
    }
}
function cycleMouseMode(){
    if(mouseMode==1){
        mouseMode=0
        document.getElementById("mouseModeButton").innerHTML="Mouse Mode: Relative"
    }else if(mouseMode==0){
        mouseMode=1
        document.getElementById("mouseModeButton").innerHTML="Mouse Mode: Absolute"
    }
}
function onResize(){
    var w = document.documentElement.clientWidth;
    var h = document.documentElement.clientHeight;
    if(w<=560){
        document.getElementById("keyboard1").style.setProperty("width","100%")
    }else{
        document.getElementById("keyboard1").style.setProperty("width","560px")
    }
}
function addButtonListeners(btn,i){
    var down=function(event){event.preventDefault();pressMouse(i,1)}
    var up=function(event){event.preventDefault();pressMouse(i,0)}
    btn.addEventListener("mousedown",down);
    btn.addEventListener("touchstart",down);
    btn.addEventListener("mouseup",up);
    btn.addEventListener("touchend",up);
    btn.addEventListener("touchcancel",up);
}
function mouseButtonsListeners(){
    var msBtns = ["mouseButtonLeft","mouseButtonRight","mouseButtonMiddle","mouseButtonBack","mouseButtonForward"]
    var i=0
    for(i=0;i<5;i++){
        var btn = msBtns[i]
        addButtonListeners(document.getElementById(btn),i);
    }
}
function addListeners(){
    var keyboard = document.getElementById("keyboard");
    var buttons=keyboard.getElementsByTagName("button");
    for(i in buttons){
        btn=buttons[i];
        if(btn.addEventListener){
            btn.onclick=null
            btn.addEventListener("touchstart",onPressKey);
            btn.addEventListener("touchend",onPressKey);
            btn.addEventListener("touchcancel",onPressKey);
            btn.addEventListener("mousedown",onPressKey);
            btn.addEventListener("mouseup",onPressKey);
            btn.addEventListener("click",function(event){event.preventDefault()});
        }
    }
    var stream = document.getElementById("stream")
    stream.addEventListener("mousedown",onMouseDrag);
    stream.addEventListener("mouseup",onMouseDrag);
    stream.addEventListener("mousemove",onMouseDrag);
    stream.addEventListener("wheel",onWheel);
    stream.addEventListener("click",function(event){event.preventDefault()});
    stream.addEventListener("touchstart",onTouchDrag);
    stream.addEventListener("touchmove",onTouchDrag);
    stream.addEventListener("touchend",onTouchDrag);
    stream.addEventListener("touchcancel",onTouchDrag);
    mouseButtonsListeners();
}
function onLoadComplete(){''
    onResize();
    addListeners();
    window.addEventListener("resize", onResize);
    setInterval(function(){
        mouseMoveReady=true
        if(mouseRelativeX!=0 && mouseRelativeY!=0) mouseRelOffset(0,0)
    },100)
    setInterval(function() {
        document.getElementById("debugoutput").innerHTML=debugstr;
    },15)
}