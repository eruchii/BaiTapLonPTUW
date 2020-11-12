
var spanNav = document.querySelectorAll("div.card-header>ul#navigation li.nav-item span")

HTMLElement.prototype.empty = function() {
    var that = this;
    while (that.hasChildNodes()) {
        that.removeChild(that.lastChild);
    }
};

function setClassActive(myself) {
    for (let i = 0; i < spanNav.length; i++) {
        spanNav[i].classList.remove('active');
    }
    myself.classList.add('active')
}

document.getElementById("post").onclick = function() {
    fetch("/post").then(response => {
        if (response.status == 200) {
            response.json().then(data => {
                document.getElementById("blockinfo").empty()
                console.log(data.posts[0].title);
                for (let i = 0; i < data.posts.length; i++) {
                    let dv = document.createElement("div")
                    let para = document.createElement("p");
                    para.innerHTML = data.posts[i].title;
                    console.log(data.posts[i].title)
                    dv.appendChild(para);
                    document.getElementById("blockinfo").appendChild(dv);
                }
            })
        }
    })
}