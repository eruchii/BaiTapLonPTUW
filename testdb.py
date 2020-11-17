from easyaccomod import db, bcrypt
from easyaccomod.models import *
from easyaccomod.owner_models import *
from easyaccomod.owner_db import *

def Fake_user():
	username = "nct1"
	password = "123456"
	check_password = "123456"
	fullname = "a b c"
	identity_number = "12"
	phone_number = "12"
	email = "assd@ajfasf.com"
	city_code = "HN"
	district_id = "1"
	ward_id = "43"
	print(add_user(username, password, check_password, email, fullname, identity_number, phone_number, city_code, district_id, ward_id))

# def Fake_room():
	

if __name__ == "__main__":
	Fake_user()