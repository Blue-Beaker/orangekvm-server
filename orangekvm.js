var ws;
var host = window.location.hostname;
var hostip = host.replace("http://","").replace("https://","")
function linkws(addr) {
    ws = new WebSocket(addr);
}
function pressKey(key,press=2) {
    ws.send("pressKey "+key+" "+press)
}
function mouseAbsolute(x,y,wheel=0) {
    ws.send("mouseAbsolute "+x+" "+y+" "+wheel)
}
function mouseRelative(x,y,wheel=0) {
    ws.send("mouseRelative "+x+" "+y+" "+wheel)
}
function pressMouse(key,press) {
    ws.send("pressMouse "+key+" "+press)
}