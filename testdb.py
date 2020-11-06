from easyaccomod import app, db
from easyaccomod.owner_models import *
from easyaccomod.models import *

db.drop_all()
db.create_all()