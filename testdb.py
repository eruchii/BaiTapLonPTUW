from easyaccomod import app, db
from easyaccomod.owner_models import Owner, Room, City, District, Ward
from easyaccomod.db import add_user

db.create_all()
city_code = 'HN'
city_name = "Hà Nội"
c = City(code=city_code, name=city_name)
db.session.add(c)
db.session.commit()