$(document).ready(function()
{
    // Load District
    data = new Object()
    data.city = document.querySelector("#city").value
    console.log(data)
    postData("/renter/api/getDistrict",data).
    then( function(data)
        {   
            console.log(data)
            clearOldElement('#district')
            clearOldElement('#street')
            data.slice(1).forEach(addToDistrictDOM)
        }).
        then(function()
        {
            data = new Object()
            data.district = document.querySelector("#district").value
            data.city = document.querySelector("#city").value
            postData("/renter/api/getStreet",data).
            then( function(data)
                {   
                    clearOldElement('#street')
                    data.slice(1).forEach(addToStreetDOM)
                })
            })
            .catch(function (error) {
            console.log("Fetch error: " + error);
            });
})

// Search button event handle

var btn = document.querySelector(".search-button")


function clearOldElement(data){
    var _obj = document.querySelector(data)
    while (_obj.firstChild){
        _obj.removeChild(_obj.lastChild)
    }
}
function addToDistrictDOM(data){
    var op = document.createElement("option") 
    op.innerHTML = data
    district.appendChild(op)
}

function addToStreetDOM(data){
    var op = document.createElement("option") 
    op.innerHTML = data
    street.appendChild(op)
}

document.querySelector("#city").onchange = async function(){
        let payload = new Object;
        payload.city = document.querySelector("#city").value
        fetch(window.origin+"/renter/api/getDistrict",
        {
            method : 'POST',
            credentials : "include",
            body : JSON.stringify(payload),
            caches: 'no-cache',
            headers : new Headers(
            {
                "content-type":"application/json"
            })
        })
        .then( function(response)
        {
        if (response.status != 200)
            {
                console.log("Error" + response.status)
                return ;
            }
            response.json().then( function(data)
            {   
                clearOldElement('#district')
                clearOldElement('#street')
                data.slice(1).forEach(addToDistrictDOM)
            })
        })
        .catch(function (error) {
        console.log("Fetch error: " + error);
        });
    }

document.querySelector("#district").onchange = async function()
{
    let payload = new Object;
    payload.district = document.querySelector("#district").value
    payload.city = document.querySelector("#city").value
    postData("/renter/api/getStreet",payload)
        .then( function(data)
            {   
                console.log(data)
                clearOldElement('#street')
                data.slice(1).forEach(addToStreetDOM)
            })
        .catch(function (error) {
        console.log("Fetch error: " + error);
        })
}

// Like button handle

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


function testPost(){
    let payload = new Object();
    payload.city = document.querySelector('#city').value
    payload.district = document.querySelector("#district").value
    payload.street = document.querySelector("#street").value

    console.log(payload)
    postData("/renter/search",payload)
}

btn.onclick=function(e){
    e.preventDefault();
    testPost()
}