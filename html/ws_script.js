console.log("script");

function startSock(){
    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onopen = function() {
        ws.send(JSON.stringify({"type":"subscribe", "topic":["heartbeat"]}));
    };
    ws.onmessage = function (evt) {
        console.log(evt.data);
    };
}
startSock();