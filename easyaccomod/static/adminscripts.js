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
            accept_pr.querySelector("#acceptuser").classList.add("nodisplay");
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
            reject_pr.querySelector("small.text-muted").innerHTML = "Status: " + data["owner_status_confirm"];
            reject_pr.querySelector("#acceptuser").classList.remove("nodisplay");
        }
        msg = document.createTextNode(data["msg"]);
        container.appendChild(msg);
    })
}

function validateInput(event) {
    var value = document.getElementById("searchname").value;
    if (value.length <= 0) {
        event.preventDefault();
        console.log("empty input search!!");
    }
}

function sendYearStatistic(event) {
    event.preventDefault();
    var data = document.getElementById("year").value;
    console.log(data)
    if (isNaN(data) || data == "") {
        alert("please check the input!");
    } else {
        // postData("/statistics", {
        //     year = data
        // })
    }
}