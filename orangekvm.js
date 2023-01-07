var ws;
var host = window.location.hostname;
var hostip = host.replace("http://","").replace("https://","")
var ws
var wslinked = false
var worker
function linkws(addr) {
    if(!"Websocket" in window){
        alert("Your browser doesn't support websocket. Please use a browser with websocket support.")
        return
    }
    ws = new WebSocket(addr);
    ws.onmessage = function (messageEvent) {
        var message=messageEvent.data;
        console.log("<-"+message);
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
    if(wslinked)
    ws.send(message);
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
                button.style.backgroundColor="#5599FF";
                button.style.color="#FFFFFF";
            }else{
                button.style.backgroundColor="#F0F0F0";
                button.style.color="#000000";
            }
        }
    }
}
function captureTouch(){
    var keyboard = document.getElementById("keyboard");
    var buttons=keyboard.getElementsByTagName("button");
    for (i in buttons) {
        var button=buttons[i]
        if(button.id && button.id.startsWith("keyboard_")){
            var name=button.id.replace("keyboard_","")
            console.log(name);
            button.addEventListener("touchstart",function(){pressKey(name,1)});
            button.addEventListener("touchend",function(){pressKey(name,0)});
            button.addEventListener("touchcancel",function(){pressKey(name,0)});
        }
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

function timedUpdate()
{
    if(wslinked){
        getPressed();
    }else{
        reconnect();
    }
    setTimeout("timedUpdate()",2000);
}

function onLoadComplete(){
    onResize();
    captureTouch();
    window.addEventListener("resize", onResize);
    // timedUpdate();
}