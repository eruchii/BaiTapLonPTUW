from easyaccomod import db, app, login_manager


class Owner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), unique = True)
	password = db.Column(db.String(120))
	fullname = db.Column(db.String(120))
	identity_number = db.Column(db.String(120))
	phone_number = db.Column(db.String(120))
	email = db.Column(db.String(120), unique = True)
	city_code = db.Column(db.String(5), db.ForeignKey('city.code'))
	district_id = db.Column(db.String(10), db.ForeignKey('district.id'))
	ward_id = db.Column(db.String(10), db.ForeignKey('ward.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # add fk to user_id
	status = db.Column(db.Integer, db.ForeignKey('confirm.id'))

	rooms = db.relationship("Room", backref="owner")
	def __repr__(self):
		return "<Owner(username='%s', password='%s', fullname='%s', identity_number='%s', phone_number='%s', status='%s'>" % (
			self.username, self.password, self.fullname, self.identity_number, self.phone_number, self.status
			)

class Room(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('owner.id')) #lien ket owner
	city_code = db.Column(db.String(5), db.ForeignKey('city.code')) #lien ket voi bang city
	district_id = db.Column(db.String(10), db.ForeignKey('district.id')) #lien ket voi district
	ward_id = db.Column(db.String(10), db.ForeignKey('ward.id')) #lien ket voi ward
	info = db.Column(db.String(120))
	room_type_id = db.Column(db.Integer)
	room_number = db.Column(db.Integer)
	price = db.Column(db.Integer)

	chung_chu = db.Column(db.Boolean)
	phong_tam = db.Column(db.Integer)
	nong_lanh = db.Column(db.Boolean)
	phong_bep = db.Column(db.Integer)
	dieu_hoa = db.Column(db.Boolean)
	ban_cong = db.Column(db.Boolean)
	gia_dien = db.Column(db.Integer)
	gia_nuoc = db.Column(db.Integer)
	tien_ich_khac = db.Column(db.Text)
	image = db.Column(db.Text)
	pending = db.Column(db.Boolean)

	def __repr__(self):
		return "<Room(id='{}', owner_id='{}'>".format(self.id, self.owner_id)

class City(db.Model):
	code = db.Column(db.String(5), primary_key=True)
	name = db.Column(db.String(120))
	owners = db.relationship("Owner", backref="city", lazy=True)
	rooms = db.relationship("Room", backref="city", lazy=True)
	def __repr__(self):
		return "<City(code='{}', name='{}'>".format(self.code, self.name) 

class District(db.Model):
	city_code = db.Column(db.String(5), db.ForeignKey('city.code'))
	id = db.Column(db.String(10), primary_key=True)
	name = db.Column(db.String(120))
	owners = db.relationship("Owner", backref="district", lazy=True)
	rooms = db.relationship("Room", backref="district", lazy=True)
	def __repr__(self):
		return "<District(city.code='{}', id='{}', name='{}'>".format(self.city_code, self.id, self.name)

class Ward(db.Model):
	city_code = db.Column(db.String(5), db.ForeignKey('city.code'))
	district_id = db.Column(db.String(10), db.ForeignKey('district.id'))
	id = db.Column(db.String(10), primary_key=True)
	name = db.Column(db.String(120))
	owners = db.relationship("Owner", backref="ward", lazy=True)
	rooms = db.relationship("Room", backref="ward", lazy=True)
	def __repr__(self):
		return "<Ward(city.code='{}', district.id='{}', id='{}', name='{}'>".format(self.city_code, self.district_id, self.id, self.name)
