async function postData(url = '', data = {}) {
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }

function createAlert(container, subclass, value){
    al = document.createElement("div");
    al.classList.add("alert");
    al.classList.add(subclass);
    alText = document.createTextNode(value);
    al.appendChild(alText);
    container.appendChild(al);
}

function Register(){
    var data = {
        username:document.getElementById("username").value,
        password:document.getElementById("password").value,
        check_password:document.getElementById("check_password").value,
        email:document.getElementById("email").value,
        fullname:document.getElementById("fullname").value,
        identity_number:document.getElementById("identity_number").value,
        phone_number:document.getElementById("phone_number").value,
        city_code:document.getElementById("city").value,
        district_id:document.getElementById("district").value,
        ward_id:document.getElementById("ward").value,
    }
    postData("/owner/api/register", data)
        .then(json => {
            msg = document.getElementById("msg");
            if(json.status === "success"){
                createAlert(msg, "alert-success", json["msg"]);
                document.getElementById("register").reset();    
            }
            else {
                createAlert(msg, "alert-danger", json["msg"]);
            };
        });

}