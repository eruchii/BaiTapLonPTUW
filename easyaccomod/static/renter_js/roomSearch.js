district =  document.querySelector('.district')
    street = document.querySelector('.street')

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


console.log(district.value + ' ' + street.value)