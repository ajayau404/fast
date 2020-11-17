console.log("script");

function startSock(){
    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onopen = function() {
        ws.send("Hello, world");
    };
    ws.onmessage = function (evt) {
        console.log(evt.data);
    };
}
startSock();