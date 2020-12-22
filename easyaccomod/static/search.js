function create_option(ele, text, value){
	option = document.createElement("option");
	optionText = document.createTextNode(text);
	option.setAttribute("value",value)
	option.appendChild(optionText)
	ele.appendChild(option)
}

function getSearchData(){
	if(localStorage.getItem("search") === null){
		url = "/static/search.json";
		fetch(url).then(
			response =>{
				if (!response.ok) {
					throw new Error("HTTP error " + response.status);
				}
				return response.json();
		}).then(json =>{
			localStorage.setItem("search",JSON.stringify(json));
		});
	}
	findCity();
}

getSearchData();

function findCity(){
	const search_data = JSON.parse(localStorage.getItem("search"));
	city = document.getElementById("city");
	   
	for(city_code in search_data){
		create_option(city,search_data[city_code]["name"], city_code);
	}
	findDistrict();
}

document.getElementById("city").onchange = findDistrict;
function findDistrict(){
	district = document.getElementById("district");
	district.innerHTML=""
	city_id = document.getElementById("city").value;
	search_data = JSON.parse(localStorage.getItem("search"));
	districts = search_data[city_id]["districts"];
	for(district_id in districts){
		create_option(district, districts[district_id]["name"], district_id);
	}
	findWard();
}

document.getElementById("district").onchange = findWard;
function findWard(){
	ward = document.getElementById("ward");
	ward.innerHTML = "";
	city_id = document.getElementById("city").value;
	district_id = document.getElementById("district").value;
	search_data = JSON.parse(localStorage.getItem("search"));
	wards = search_data[city_id]["districts"][district_id]["wards"];
	for(i in wards){
		create_option(ward, wards[i]["name"], i);
	}
}