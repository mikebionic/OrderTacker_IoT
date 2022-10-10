from flask_login import UserMixin
from datetime import datetime

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
	location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
	order_code = db.Column(db.String())
	access_type = db.Column(db.String(255))
	location_info = db.Column(db.String())
	description = db.Column(db.String())
	# 1 is entrance
	entrance_type = db.Column(db.Integer, default=1)
	date = db.Column(db.DateTime, default = datetime.now())

	def to_json(self):
		return {
			"id": self.id,
			"finger_id": self.finger_id,
			"location_id": self.location_id,
			"order_code": self.order_code,
			"access_type": self.access_type,
			"location_info": self.location_info,
			"description": self.description,
			"entrance_type": self.entrance_type,
			"date": self.date,
		}

class Location(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	icon = db.Column(db.String())
	key = db.Column(db.String(1000))
	full_name = db.Column(db.String)
	address = db.Column(db.String)
	latitude = db.Column(db.String)
	longitude = db.Column(db.String)
	access_logs = db.relationship('Access_log', backref='location', lazy=True)

	def to_json(self):
		return {
			"id": self.id,
			"name": self.name,
			"icon": self.icon,
			"key": self.key,
			"full_name": self.full_name,
			"address": self.address,
			"latitude": self.latitude,
			"longitude": self.longitude,
		}

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	order_code = db.Column(db.String())
	card_code = db.Column(db.String())
	sender_name = db.Column(db.String())
	sender_surname = db.Column(db.String())
	postal_phone_number = db.Column(db.String())
	sender_phone_number = db.Column(db.String())
	sender_email = db.Column(db.String())
	place_to_deliver = db.Column(db.String())
	city = db.Column(db.String())
	address = db.Column(db.String())
	paid = db.Column(db.Integer(), default=0)
	info = db.Column(db.String())
	completed = db.Column(db.Boolean(), default=False)

	def to_json(self):
		return {
			"id": self.id,
			"order_code": self.order_code,
			"card_code": self.card_code,
			"sender_name": self.sender_name,
			"sender_surname": self.sender_surname,
			"postal_phone_number": self.postal_phone_number,
			"sender_phone_number": self.sender_phone_number,
			"sender_email": self.sender_email,
			"place_to_deliver": self.place_to_deliver,
			"city": self.city,
			"address": self.address,
			"paid": self.paid,
			"info": self.info,
			"completed": self.completed,
		}


class Finger(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	code = db.Column(db.String)
	name = db.Column(db.String(500))
	access_logs = db.relationship('Access_log', backref='finger', lazy=True)

	def to_json(self):
		return {
			"id": self.id,
			"user_id": self.user_id,
			"code": self.code,
			"name": self.name,
		}