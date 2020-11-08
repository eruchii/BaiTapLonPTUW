# db for admin

from easyaccomod import db, app, bcrypt
from easyaccomod.models import *
from easyaccomod.owner_models import *

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

# password = "123456"

# hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
# user = User(username="hones_admin", email="honest.1311.tbvn@gmail.com", password=hashed_password, role_id=1, status_confirm=1)
# db.session.add(user)

db.session.commit()