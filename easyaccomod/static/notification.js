namespace = '';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
socket.on('connect', function(){
    socket.emit("connected");
});

sample = {
    "title":"test title",
    "msg":"test msg",
    "created_at":"Nov 30 2020"
}

function createNotification(data){
    container = document.createElement("div");
    container.classList.add("card");
    container.classList.add("mb-3")
    
    headerDiv = document.createElement("div");
    headerDiv.classList.add("card-header");
    headerText = document.createTextNode(data["title"]);
    headerDiv.appendChild(headerText);

    bodyDiv = document.createElement("div");
    bodyDiv.classList.add("card-body");
    blockquote = document.createElement("blockquote");
    blockquote.classList.add("blockquote");
    p = document.createElement("p");
    bodyText = document.createTextNode(data["msg"]);
    created_at = document.createTextNode(data["created_at"]);
    footer = document.createElement("footer");
    footer.classList.add("blockquote-footer");
    
    p.appendChild(bodyText);
    footer.appendChild(created_at);
    blockquote.appendChild(p); blockquote.appendChild(footer);
    bodyDiv.appendChild(blockquote);

    container.appendChild(headerDiv);
    container.appendChild(bodyDiv);

    n = document.getElementById("noti");
    n.insertBefore(container, n.childNodes[0]);
}