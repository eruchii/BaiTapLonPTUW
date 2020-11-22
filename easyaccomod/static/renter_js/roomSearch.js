var btn = document.querySelector(".btn-outline-info")
// xu ly submit
btn.onclick = async function(e){
    e.preventDefault()
    //let payload = [{'city': 'Hồ Chí Minh'}, {'district': 'Quận 4'}, {'street': '12'}, {'near': 'Hanoi'}, {'price': '2315'}, {'roomType': '545'}, {'area': '454654'}, {'phong_tam': '4'}, {'nong_lanh': 'False'}, {'dieu_hoa': 'False'}, {'ban_cong': 'False'}, {'chung_chu': 'False'}, {'gia_dien': '454564564'}, {'gia_nuoc': '454564564'}, {'tien_ich_khac': 'Koh'}]
   
    let payload =[]

    payload.push({'city' : document.querySelector(".city").value})
    payload.push({'district' : document.querySelector(".district").value })
    payload.push({'street': document.querySelector(".street").value})
    payload.push({'near' :  near = document.querySelector(".near").value })
    payload.push({'price' : document.querySelector(".price").value})
    payload.push({'roomType' :document.querySelector(".roomType").value })
    payload.push({'area': document.querySelector(".area").value })
    payload.push({'phong_tam' : document.querySelector(".phong_tam").value})
    payload.push({'nong_lanh' : document.querySelector(".nong_lanh").checked})
    payload.push({'dieu_hoa':document.querySelector(".dieu_hoa").checked})
    payload.push({'ban_cong' : document.querySelector(".ban_cong").checked})
    payload.push({'chung_chu': document.querySelector(".chung_chu").checked})
    payload.push({'gia_dien' : document.querySelector(".gia_dien").value})
    payload.push({'gia_nuoc' : document.querySelector('.gia_nuoc').value})
    payload.push({'tien_ich_khac': document.querySelector(".tien_ich_khac").value})
    
    console.log(payload)

    fetch(window.origin+"/renter/search",
        {
            method : 'POST',
            credentials : "include",
            body : JSON.stringify(['submit',payload]),
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
                document.querySelector(".test").removeAttribute("style")
                console.log(data)
            })
        })
        .catch(function (error) {
        console.log("Fetch error: " + error);
        });
    }


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

document.querySelector(".city").onchange = function(){
        fetch(window.origin+"/renter/search",
        {
            method : 'POST',
            credentials : "include",
            body : JSON.stringify(['city',document.querySelector(".city").value]),
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
                clearOldElement('.district')
                clearOldElement('.street')
                data.slice(1).forEach(addToDistrictDOM)
            })
        })
        .catch(function (error) {
        console.log("Fetch error: " + error);
        });
    }

    document.querySelector(".district").onchange = function(){
        fetch(window.origin+"/renter/search",
        {
            method : 'POST',
            credentials : "include",
            body : JSON.stringify(['district',document.querySelector(".district").value]),
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
                    clearOldElement('.street')
                    data.slice(1).forEach(addToStreetDOM)
                })
            })
            .catch(function (error) {
            console.log("Fetch error: " + error);
        });
    }


// Search button event handle
