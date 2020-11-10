from easyaccomod import db, bcrypt
from easyaccomod.models import *
from easyaccomod.owner_models import *
from easyaccomod.db import *

def Fake_user():
	username = "abcd"
	password = "123456"
	check_password = "123456"
	fullname = "a b c"
	identity_number = "123456789"
	phone_number = "123456789"
	email = "asodk@ajfasf.com"
	city_code = "HN"
	district_id = "1"
	ward_id = "43"
	print(add_user(username, password, check_password, email, fullname, identity_number, phone_number, city_code, district_id, ward_id))


if __name__ == "__main__":
	Fake_user()
	a = Owner.query.all()[0]
	print(a.district.name)