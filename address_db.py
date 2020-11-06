from easyaccomod import db
from easyaccomod.owner_models import City, District, Ward
from easyaccomod.db import add_city, add_district, add_ward
import json

db.create_all()

cities = json.load(open("cities.json","r",encoding="utf-8"))
districts = json.load(open("districts.json","r", encoding="utf-8"))
wards = json.load(open("wards.json","r", encoding="utf-8"))

for city in cities:
    add_city(code=city["code"], name=city["name"], commit=False)

for district in districts:
    add_district(city_code=district["city.code"], id=district["id"], name=district["name"], commit=False)

for ward in wards:
    add_ward(city_code=ward["city.code"], district_id=ward["district.id"], id=ward["id"], name=ward["name"], commit=False)

db.session.commit()