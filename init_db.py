from easyaccomod import db, bcrypt
from easyaccomod.models import *
from easyaccomod.owner_models import *
import json
from easyaccomod.db import *

db.drop_all()
db.create_all()

print("create 'role'")
role1 = Role(title="admin", name="admin", description="admin can do anything, but can not register by normal way")
role2 = Role(title="renter", name="renter", description="renter can find accommodation that meets their needs")
role3 = Role(title="owner", name="owner", description="owner can post accommodation information to find renter")

db.session.add(role1)
db.session.add(role2)
db.session.add(role3)
db.session.commit()

print("create 'confirm'")
cnf1 = Confirm(name="OK", description="Your account has been approved!")
cnf2 = Confirm(name="WAIT", description="Your account is waiting for admin approval!")
cnf3 = Confirm(name="REJECT", description="Your account has been denied! Please contact admin for more details")

db.session.add(cnf1)
db.session.add(cnf2)
db.session.add(cnf3)
db.session.commit()

#Address tables
cities = json.load(open("cities.json","r",encoding="utf-8"))
districts = json.load(open("districts.json","r", encoding="utf-8"))
wards = json.load(open("wards.json","r", encoding="utf-8"))
print("create 'city'")
for city in cities:
    add_city(code=city["code"], name=city["name"], commit=False)
print("create 'district'")
for district in districts:
    add_district(city_code=district["city.code"], id=district["id"], name=district["name"], commit=False)
print("create 'ward'")
for ward in wards:
    add_ward(city_code=ward["city.code"], district_id=ward["district.id"], id=ward["id"], name=ward["name"], commit=False)
db.session.commit()

#Room type
RT1 = RoomType(name="Phòng trọ")
RT2 = RoomType(name="Chung cư mini")
RT3 = RoomType(name="Nhà nguyên căn")
RT4 = RoomType(name="Chung cư nguyên căn")
db.session.add(RT1)
db.session.add(RT2)
db.session.add(RT3)
db.session.add(RT4)
db.session.commit()