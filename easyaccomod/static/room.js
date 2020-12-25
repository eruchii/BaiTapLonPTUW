function createAlert(container, subclass, value){
    al = document.createElement("div");
    al.classList.add("alert");
    al.classList.add(subclass);
    alText = document.createTextNode(value);
    al.appendChild(alText);
    container.appendChild(al);
}
function create_new_room(){
    form = document.getElementById("room_form");
    formData = new FormData(form);
    fetch("/owner/api/room/create", {
        method: 'POST', 
        body: formData
    }).then(response => response.json())
    .then(json => {
        msg = document.getElementById("msg");
        msg.innerHTML = "";
        console.log(json)
        if(json.status === "success"){
            createAlert(msg, "alert-success", json["msg"]);  
        }
        else {
            createAlert(msg, "alert-danger", json["msg"]);
        };
    }).catch(error => console.log(error) );
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function update_post(post_id){
    form = document.getElementById("room_form");
    formData = new FormData(form);
    fetch("/owner/api/post/update/"+post_id, {
        method: 'POST', 
        body: formData
    }).then(response => response.json())
    .then(json => {
        msg = document.getElementById("msg");
        msg.innerHTML = "";
        console.log(json)
        if(json.status === "success"){
            createAlert(msg, "alert-success", json["msg"]);    
        }
        else {
            createAlert(msg, "alert-danger", json["msg"]);
        };
    }).catch(error => console.log(error) );
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function delete_post(post_id){
    form = document.getElementById("room_form");
    formData = new FormData(form);
    fetch("/owner/api/post/delete/"+post_id, {
        method: 'POST', 
        body: formData
    }).then(response => response.json())
    .then(json => {
        msg = document.getElementById("msg");
        msg.innerHTML = "";
        console.log(json)
        if(json.status === "success"){
            createAlert(msg, "alert-success", json["msg"]);    
        }
        else {
            createAlert(msg, "alert-danger", json["msg"]);
        };
    }).catch(error => console.log(error) )
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function update_status(element, post_id){
    fetch("/owner/api/post/changestatus/"+post_id, {
        method: 'GET'
    }).then(response => response.json())
    .then(json => {
        msg = document.getElementById("msg");
        msg.innerHTML = "";
        console.log(json)
        if(json.status === "success"){
            createAlert(msg, "alert-success", json["msg"]);   
            new_text_node = document.createTextNode(json["textNodeValue"]); 
            element.removeChild(element.childNodes[0]);
            element.appendChild(new_text_node);
        }
        else {
            createAlert(msg, "alert-danger", json["msg"]);
        };
    }).catch(error => console.log(error));
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function delete_post(element, post_id){
    x = confirm("Bạn có chắc chắn muốn xóa post này?");
    if(x == false) return;
    fetch("/owner/api/post/delete/"+post_id, {
        method: 'GET'
    }).then(response => response.json())
    .then(json => {
        msg = document.getElementById("msg");
        msg.innerHTML = "";
        console.log(json)
        if(json.status === "success"){
            createAlert(msg, "alert-success", json["msg"]);  
            current_post = element.parentNode.parentNode.parentNode;
            current_post.remove();
        }
        else {
            createAlert(msg, "alert-danger", json["msg"]);
        };
    }).catch(error => console.log(error));
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}