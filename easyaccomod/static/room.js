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
            document.getElementById("room_form").reset();    
        }
        else {
            createAlert(msg, "alert-danger", json["msg"]);
        };
    });
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}