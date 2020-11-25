namespace = '';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
socket.on('connect', function(){
    socket.emit("connected");
    socket.emit("load list people");
});
socket.on('new msg', function(data) {
    if(document.getElementById("receiver").value == data.sender){
        if(data.type == 1) createIncomingMsg(data);
        else createOutgoingMsg(data);
    }
    else{
        socket.emit("load list people");
        Load();
    }    
});

socket.on('chat log', function(msgs){
    createHistoryMsg(msgs);
});

socket.on('loaded list people', function(data){
    container = document.getElementsByClassName("inbox_chat")[0];
    while (container.childNodes.length != 0){
        container.removeChild(container.childNodes[0]);
    }
    for(i = 0 ; i < data.length; i++){
        receiver = data[i];
        console.log(receiver);
        createChatList(receiver);
    }
});

function Send(){
    msg_box = document.getElementById("msg-box")
    msg = msg_box.value;
    if(msg.length == 0) return;
    msg_box.value = "";
    recv = document.getElementById("receiver").value;
    socket.emit("send msg", {recv:recv,msg:msg});
}

function Load(){
    recv = document.getElementById("receiver").value;
    socket.emit("load msg", {recv:recv});
}

function createIncomingMsg(data){

    incoming_msg_img = document.createElement("div");
    incoming_msg_img.classList.add("incoming_msg_img");
    img = document.createElement("img");
    img.src = data["img"];
    incoming_msg_img.appendChild(img);

    container = document.getElementsByClassName("msg_history")[0];
    incoming_msg = document.createElement("div");
    incoming_msg.classList.add("incoming_msg");
    received_msg = document.createElement("div");
    received_msg.classList.add("received_msg");
    recv_msg_child = document.createElement("div");
    recv_msg_child.classList.add("received_withd_msg");
    msg = document.createElement("p");
    msgText = document.createTextNode(data.msg);

    date = document.createElement("span");
    date.classList.add("time_date");
    dateText = document.createTextNode(data.date);

    msg.appendChild(msgText);
    date.appendChild(dateText);
    recv_msg_child.appendChild(msg);
    recv_msg_child.appendChild(date);
    received_msg.appendChild(recv_msg_child);
    incoming_msg.appendChild(incoming_msg_img);
    incoming_msg.appendChild(received_msg);
    container.appendChild(incoming_msg);

    container.scrollTop = container.scrollHeight;
}

function createOutgoingMsg(data){
    container = document.getElementsByClassName("msg_history")[0];
    outgoing_msg = document.createElement("div");
    outgoing_msg.classList.add("outgoing_msg");
    sent_msg = document.createElement("div");
    sent_msg.classList.add("sent_msg");
    msg = document.createElement("p");
    msgText = document.createTextNode(data.msg);
    date = document.createElement("span");
    date.classList.add("time_date");
    dateText = document.createTextNode(data.date);

    msg.appendChild(msgText);
    date.appendChild(dateText);
    sent_msg.appendChild(msg);
    sent_msg.appendChild(date);
    outgoing_msg.appendChild(sent_msg);
    container.appendChild(outgoing_msg);
    
    container.scrollTop = container.scrollHeight;
}

function createHistoryMsg(msgs){
    container = document.getElementsByClassName("msg_history")[0];
    while (container.childNodes.length != 0){
        container.removeChild(container.childNodes[0]);
    }
    for(let i = 0; i < msgs.length; i++){
        if(msgs[i].type == 1) createIncomingMsg(msgs[i]);
        else createOutgoingMsg(msgs[i]);
    }
}

function createChatList(data){
    date = document.createElement("span");
    dateText = document.createTextNode(data.date);
    date.appendChild(dateText);
    h5 = document.createElement("h5");
    h5Text = document.createTextNode(data.username+" ("+data.new_msg+")");
    h5.appendChild(h5Text);
    h5.appendChild(date);
    p = document.createElement("p");
    pText = document.createTextNode(data.msg);
    p.appendChild(pText);

    chat_ib = document.createElement("div");
    chat_ib.classList.add("chat_ib");
    chat_ib.appendChild(h5);
    chat_ib.appendChild(p);

    img = document.createElement("img");
    img.src = data.img;
    chat_img = document.createElement("div");
    chat_img.classList.add("chat_img");
    chat_img.appendChild(img);

    chat_people = document.createElement("div");
    chat_people.classList.add("chat_people");
    chat_people.appendChild(chat_img);
    chat_people.appendChild(chat_ib);

    chat_list = document.createElement("div");
    chat_list.classList.add("chat_list");
    chat_list.setAttribute("id",data.username)
    chat_list.appendChild(chat_people);
    chat_list.onclick = switchChatWindow
    container = document.getElementsByClassName("inbox_chat")[0];
    container.append(chat_list);
}

function switchChatWindow(){
    username = this.getAttribute("id");
    current_active = document.getElementsByClassName("active_chat");
    if(current_active.length != 0){
        current_active[0].classList.remove("active_chat");
    }
    chat_list = document.getElementById(username);
    chat_list.classList.add("active_chat");
    document.getElementById("receiver").value = username;
    Load();
}


document.getElementById("search-box").onchange = search;
function search(){
    socket.emit("search user", {search:this.value});
}