# db for admin

import json
from flask import jsonify
from easyaccomod import db, bcrypt
from easyaccomod.models import *
from easyaccomod.owner_models import *
from easyaccomod.admin.utils import *

# db.drop_all()
# db.create_all()

# role1 = Role(title="admin", name="admin", description="admin can do anything, but can not register by normal way")
# role2 = Role(title="renter", name="renter", description="renter can find accommodation that meets their needs")
# role3 = Role(title="owner", name="owner", description="owner can post accommodation information to find renter")

# db.session.add(role1)
# db.session.add(role2)
# db.session.add(role3)

# cnf1 = Confirm(name="OK", description="Your account has been approved!")
# cnf2 = Confirm(name="WAIT", description="Your account is waiting for admin approval!")
# cnf3 = Confirm(name="REJECT", description="Your account has been denied! Please contact admin for more details")

# db.session.add(cnf1)
# db.session.add(cnf2)
# db.session.add(cnf3)

password = "123456"

hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
# user = User(username="honest_admin", email="honest.1311.tbvn@gmail.com", password=hashed_password, role_id=1, status_confirm=1)
# db.session.add(user)
# db.session.flush()
# owner1 = Owner(username="testowner", password=hashed_password, fullname="testfullname", identity_number="123456789", phone_number="0987654321", email="owner.test@gmail.com", status="1")
# us_id = addUserByAdmin(owner1.username, owner1.password, owner1.email)
# owner1.user_id = us_id
# db.session.add(owner1)
# db.session.flush()
# room1 = Room(owner_id=owner1.id, city_code="HN", district_id="1", ward_id="44", info="thue nha",room_type_id=1, room_number=3, price=10000, chung_chu=True, phong_tam=2, nong_lanh=True, phong_bep=1, dieu_hoa=True, ban_cong=False, gia_dien=4000,gia_nuoc=20000, tien_ich_khac="None", image="df.jpg", pending=False)
# db.session.add(room1)

# owner2 = Owner(username="testowner3", password=hashed_password, fullname="owner2 fullname", identity_number=11111111, phone_number=19008198, email="owner3.test@gmail.com", status=2)
# print(addUserByOwner(owner2.username, hashed_password, owner2.email))


# owner2.user_id = us_id
# db.session.add(owner2)

# db.session.commit()