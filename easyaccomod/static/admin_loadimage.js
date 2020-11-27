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
