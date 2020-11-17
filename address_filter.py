import json

with open("data.json","r",encoding="utf-8") as f:
	data = json.load(f)

result = {}

for c in data:
	city = {}
	city["id"] = c["code"]
	city["name"] = c["name"]
	city["districts"] = {}

	for d in c["districts"]:
		district = {}
		district["id"] = d["id"]
		district["name"] = d["name"]
		district["wards"] = {}
		for w in d["wards"]:
			ward = {}
			ward["id"] = w["id"]
			ward["name"] = w["name"]
			district["wards"][w["id"]] = ward
		city["districts"][d["id"]] = district
	result[city["id"]] = city 

with open("search.json", "w", encoding="utf-8") as f:
	json.dump(result, f, ensure_ascii=False)
