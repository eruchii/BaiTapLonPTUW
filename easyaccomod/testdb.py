from __init__ import app, db
from owner_models import Owner, Room
from db import add_user

username = "abc"
password = "123456"
check_password = "123456"
fullname= "Nguyen Van A"
phone_number= "123456"
identity_number= "123456"
db.create_all()
x, msg = add_user(username, password, check_password, fullname, identity_number, phone_number)

print(x, msg)
