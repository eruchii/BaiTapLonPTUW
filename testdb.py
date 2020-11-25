from easyaccomod.models import *
from easyaccomod.owner_models import *
from easyaccomod.owner_db import *
import random

def Fake_user():
	username = "eruru{}".format(random.randint(1, 100))
	password = "123456"
	check_password = "123456"
	fullname = "a b c"
	identity_number = str(random.randint(1000, 100000))
	phone_number = str(random.randint(1000, 100000))
	email = "{}@ajfasf.com".format(str(random.randint(1000, 100000)))
	city_code = "HN"
	district_id = "1"
	ward_id = "43"
	print(add_user(username, password, check_password, email, fullname, identity_number, phone_number, city_code, district_id, ward_id))

# def Fake_room():
	

if __name__ == "__main__":
	Fake_user()