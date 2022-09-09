from flask_login import UserMixin

from main import db
from main import login_manager

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255))
	name = db.Column(db.String(500))
	surname = db.Column(db.String(500))
	patronomic = db.Column(db.String(500))
	position = db.Column(db.String(500))
	pin = db.Column(db.String(80))
	avatar = db.Column(db.String)
	fingers = db.relationship("Finger", backref='user', lazy=True)

	def to_json(self):
		return {
			"id": self.id,
			"username": self.username,
			"name": self.name,
			"surname": self.surname,
			"patronomic": self.patronomic,
			"position": self.position,
			"pin": self.pin,
		}


class Access_log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	finger_id = db.Column(db.Integer, db.ForeignKey('finger.id'))
	access_type = db.Column(db.String(255))
	# 1 is entrance
	entrance_type = db.Column(db.Integer, default=1)
	location = db.Column(db.String(1000))
	date = db.Column(db.DateTime)

	def to_json(self):
		return {
			"id": self.id,
			"finger_id": self.finger_id,
			"access_type": self.access_type,
			"entrance_type": self.entrance_type,
			"location": self.location,
			"date": self.date,
		}


class Finger(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	finger_id = db.Column(db.Integer)
	code = db.Column(db.String)
	name = db.Column(db.String(500))
	access_logs = db.relationship('Access_log', backref='finger', lazy=True)

	def to_json(self):
		return {
			"id": self.id,
			"user_id": self.user_id,			
			"finger_id": self.finger_id,			
			"code": self.code,			
			"name": self.name,
		}