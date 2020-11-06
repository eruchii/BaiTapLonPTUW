from easyaccomod import db, app, login_manager
#from easyaccomod.__init__ import db, app, login_manager # test


class Owner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique = True)
	password = db.Column(db.String)
	fullname = db.Column(db.String)
	identity_number = db.Column(db.String)
	phone_number = db.Column(db.String)
	status = db.Column(db.Integer, db.ForeignKey('confirm.id'))
	def __repr__(self):
		return "<Owner(username='%s', password='%s', fullname='%s', identity_number='%s', phone_number='%s', status='%s'>" % (
			self.username, self.password, self.fullname, self.identity_number, self.phone_number, self.status
			)

class Room(db.Model):
	__tablename__ = 'room_pending'
	id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(db.Integer) 
	city_code = db.Column(db.String, db.ForeignKey('city.code')) #lien ket voi bang city
	district_id = db.Column(db.Integer, db.ForeignKey('district.id')) #lien ket voi district
	ward_id = db.Column(db.Integer, db.ForeignKey('ward.id')) #lien ket voi ward
	info = db.Column(db.String)
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

	def __repr__(self):
		return "<Room(id='{}', owner_id='{}'>".format(self.id, self.owner_id)

class City(db.Model):
	code = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)
	def __repr__(self):
		return "<City(city_code='{}', city_name='{}'>".format(self.city_code, self.city_name) 

class District(db.Model):
	city_code = db.Column(db.String, db.ForeignKey('city.code'))
	id = db.Column(db.String, primary_key=True)
	ame = db.Column(db.String)
	def __repr__(self):
		return "<District(city.code='{}', id='{}', name='{}'>".format(self.city_code, self.id, self.name)

class Ward(db.Model):
	city_code = db.Column(db.String, db.ForeignKey('city.code'))
	district_id = db.Column(db.String, db.ForeignKey('district.id'))
	id = db.Column(db.String, primary_key=True)
	name = db.Column(db.String)
	def __repr__(self):
		return "<Ward(city.code='{}', district.id='{}', id='{}', name='{}'>".format(self.city_code, self.district_id, self.id, self.name)