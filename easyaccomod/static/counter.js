namespace = '';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
socket.on('connect', function(){
    socket.emit("connected");
});

socket.on("update new noti count", function(data){
    a = document.getElementById("new_noti");
    if(a != null)
        a.firstChild.nodeValue = data["new_noti_count"];
});

socket.on("update new msg count", function(data){
    a = document.getElementById("new_noti");
    if(a != null) a.firstChild.nodeValue = data["new_msg_count"];
});