// var spanNav = document.querySelectorAll("div.card-header>ul#navigation li.nav-item span")

HTMLElement.prototype.empty = function () {
    var that = this;
    while (that.hasChildNodes()) {
        that.removeChild(that.lastChild);
    }
};

// Example POST method implementation:
async function postData(url = '', data = {}) {
    // Default options are marked with *
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

function Accept(myself, id) {
    postData("/post/accept", {
        post_id: id
    }).
    then(data => {
        container = document.getElementById("msg");
        container.innerHTML = "";
        container.empty();
        // child = document.createElement("div")
        // child.classList.add("alert");
        container.classList.remove("nodisplay");
        if (data["status"] == "error") {
            container.classList.add("alert-danger");
        } else {
            container.classList.add("alert-success");
            var accept_pr = myself.parentNode;
            myself.parentNode.childNodes[3].innerHTML = data["post_pending"];
            //myself.parentNode.parentNode.childNodes[15].firstChild.innerHTML = "Pending: " + data["post_pending"];
            console.log(myself.parentNode.childNodes);
            myself.parentNode.removeChild(myself.nextSibling);
            //console.log(myself.parentNode.childNodes);
            myself.parentNode.removeChild(myself)
            console.log(accept_pr.childNodes);
        }
        msg = document.createTextNode(data["msg"]);
        // child.appendChild(msg)
        container.appendChild(msg);
    });
}

function Reject(myself, id) {
    postData("/post/reject", {
        post_id: id
    }).
    then(data => {
        container = document.getElementById("msg");
        container.innerHTML = "";
        container.empty();
        container.classList.remove("nodisplay");
        if (data["status"] == "error") {
            container.classList.add("alert-danger");
        } else {
            container.classList.add("alert-success");
            var reject_pr = myself.parentNode;
            console.log(reject_pr.childNodes);
            myself.parentNode.childNodes[3].innerHTML = data["post_pending"];
            if (reject_pr.childNodes.length == 11) {
                var childafter = reject_pr.childNodes[4];
                var txtNode = document.createTextNode("");
                var acptNode = document.createElement("a");
                var acptContent = document.createTextNode("Accept");
                acptNode.appendChild(acptContent);
                acptNode.classList.add("btn", "btn-info", "btn-sm", "m-1");
                acptNode.addEventListener("click", function () {
                    Accept(acptNode, id);
                });
                //myself.parentNode.parentNode.childNodes[15].firstChild.innerHTML = "Pending: " + data["post_pending"];
                reject_pr.insertBefore(acptNode, childafter);
                reject_pr.insertBefore(txtNode, acptNode);
            }
        }
        msg = document.createTextNode(data["msg"]);
        container.appendChild(msg);
    });
}

function acceptOwner(myself, id) {
    postData("/owner/accept", {
        user_id: id
    }).then(data => {
        container = document.getElementById("msg");
        container.innerHTML = "";
        container.empty();
        container.classList.remove("nodisplay");
        if (data["status"] == "error") {
            container.classList.add("alert-danger");
        } else {
            container.classList.add("alert-success");
            var accept_pr = myself.parentNode;
            accept_pr.querySelector("small.text-muted").innerHTML = "Status: " + data["owner_status_confirm"];
            accept_pr.querySelector("#acceptuser").style.display = "none";
        }
        msg = document.createTextNode(data["msg"]);
        container.appendChild(msg);
    })
}

function rejectOwner(myself, id) {
    postData("/owner/reject", {
        user_id: id
    }).then(data => {
        container = document.getElementById("msg");
        container.innerHTML = "";
        container.empty();
        container.classList.remove("nodisplay");
        if (data["status"] == "error") {
            container.classList.add("alert-danger");
        } else {
            container.classList.add("alert-success");
            var reject_pr = myself.parentNode;
            reject_pr.querySelector("#acceptuser").style.display = "inline-block";
            reject_pr.querySelector("small.text-muted").innerHTML = "Status: " + data["owner_status_confirm"];
        }
        msg = document.createTextNode(data["msg"])
        container.appendChild(msg)
    })
}

function convertStrToList(str) {
    var ans = [];
    var temp = [];
    for (let i = 0; i < str.length; i++) {
        if (str[i] == "'") {
            temp.push(i);
        }
    }
    var str_element = "";
    for (let j = 0; j < temp.length; j+=2) {
        for (let k = temp[j]+1; k < temp[j+1]; k++) {
            str_element += str[k];
        }
        ans.push(str_element);
        str_element = "";
    }
    return(ans)
}

function loadImage(check, room_image) {
    var arr = convertStrToList(room_image);
    for (let i = 0; i < arr.length; i++) {
        var x = document.createElement("img");
        var src = window.origin + "/static/room_pics/" + arr[i];
        x.setAttribute("src", src);
        x.style.padding = '2px';
        x.style.margin = '1px';
        x.setAttribute("width", "150");
        x.setAttribute("height", "150");
        x.setAttribute("alt", arr[i]);
        x.classList.add("room-image");
        check.querySelector("#image").appendChild(x);
    }
}

var arr = document.querySelectorAll("article.media.content-section");
for (let i = 0; i < arr.length; i++) {
    loadImage(arr[i], arr[i].querySelector("#room_image").innerHTML);
}