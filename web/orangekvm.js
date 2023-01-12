var ws;
var host = window.location.hostname;
var hostip = host.replace("http://","").replace("https://","")
var ws
var wslinked = false
var worker
var mouseMoveReady=true
var mouseMode=0
function linkws(addr) {
    if(!"Websocket" in window){
        alert("Your browser doesn't support websocket. Please use a browser with websocket support.")
        return
    }
    ws = new WebSocket(addr);
    ws.onmessage = function (messageEvent) {
        var message=messageEvent.data;
        console.log("<- "+message);
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
    console.log("-> "+message);}
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
    stream.addEventListener("click",function(event){event.preventDefault()});
    stream.addEventListener("touchstart",onTouchDrag);
    stream.addEventListener("touchmove",onTouchDrag);
    stream.addEventListener("touchend",onTouchDrag);
    stream.addEventListener("touchcancel",onTouchDrag);
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
function onMouseDrag(event=new MouseEvent()){
    event.preventDefault()
    if(event.type=="mousemove"){
        if(!mouseMoveReady) return;
        mouseMoveReady=false;
        setTimeout(function(){mouseMoveReady=true},100)
    }
    var stream = document.getElementById("stream")
    var mouseX=event.offsetX/stream.width
    var mouseY=event.offsetY/stream.height
    var button=0
    if(event.button==1) button=2
    else if(event.button==2) button=1
    else button=event.button
    if(event.type=="mousedown") pressMouse(button,1)
    if(event.type=="mouseup") pressMouse(button,0)
    mouseAbs(mouseX,mouseY,event.button)
}
function onTouchDrag(event=new TouchEvent()){
    event.preventDefault()
    if(event.type=="touchmove"){
        if(!mouseMoveReady) return;
        mouseMoveReady=false;
        setTimeout(function(){mouseMoveReady=true},100)
    }
    if(event.targetTouches.length>=1){
        var touch = event.targetTouches[0]
        var stream = document.getElementById("stream")
        var mouseX=touch.pageX/stream.width
        var mouseY=touch.pageY/stream.height
        var button=0
        if(event.targetTouches.length==2) button=2
        else if(event.targetTouches.length==3) button=1
        else button=event.targetTouches.length-1
        if(event.type=="touchstart") pressMouse(button,1)
        mouseAbs(mouseX,mouseY,event.targetTouches.length)
    }
    if(event.type=="touchend" || event.type=="touchcancel") pressMouse(button,0)
}
function mouseAbs(x,y,args){
    var x=Math.max(0,Math.min(1,x))
    var y=Math.max(0,Math.min(1,y))
    mouseAbsolute(Math.floor(x*4095),Math.floor(y*4095),0);
    var debugstr=args+","+" "+x+","+y+" "+x*4095+","+y*4095
    document.getElementById("debugoutput").innerHTML=debugstr;
}
function mouseRel(x,y,args){

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
function onLoadComplete(){
    onResize();
    addListeners();
    window.addEventListener("resize", onResize);
}