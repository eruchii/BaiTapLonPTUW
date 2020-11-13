namespace = '';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
socket.on('connect', function(){
    socket.emit("connected")
});
socket.on('new msg', function(data) {
    console.log("new msg")
    addMsg(data);
});

function Send(){
    msg_box = document.getElementById("msg-box")
    msg = msg_box.value;
    msg_box.value = "";
    recv = document.getElementById("recv").value;
    socket.emit("send msg", {recv:recv,msg:msg});
    data = {sender:"You", msg:msg};
    addMsg(data);
}

function addMsg(data){
    p = document.getElementById("msg");
    text = '<li>'+data.sender+":"+data.msg+'</li>';
    p.innerHTML += text;
}
