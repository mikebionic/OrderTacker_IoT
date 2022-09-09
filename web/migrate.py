from main import db

from main.config import Config
from main.models import User, Finger

db.drop_all()
db.create_all()

admin_user = User(username=Config.ADMIN_USERNAME, pin = Config.ADMIN_PIN)
db.session.add(admin_user)

users_data = [
	{
		"id":	2,
		"username": "plan",
		"name": "Plan",
		"surname": "Planyyew",
		"patronomic": "Planyyewic",
		"position": "Uly l-nt",
		"pin": "",
		"avatar": "",
	},
	{
		"id":	3,
		"username": "jemal",
		"name": "Jemal",
		"surname": "Planyyewa",
		"patronomic": "Planyyewna",
		"position": "Kapitan-leytenant",
		"pin": "",
		"avatar": "",
	}
]

fingers_data = [
	{
		"id": 1,
		"user_id": 2,
		"code": "8B;44:12:22",
		"name": "",
	},
	{
		"id": 2,
		"user_id": 3,
		"code": "8433:2:12:22",
		"name": "",
	}
]


locations_data = [
	{
		"id": 1,
		"name": "study_place",
		"full_name": "Plan yerin plan bolumcesenin okuw binasy",
		"address": "Parahat 01",
		"latitude": "11112",
		"longitude": "92323",
	},
	{
		"id": 2,
		"name": "entrance",
		"full_name": "Plan yerin girelgesi",
		"address": "Parahat 01",
		"latitude": "11121",
		"longitude": "92333",
	},
]


for user in users_data:
	current_user = User(**user)
	db.session.add(current_user)
	# db.session.commit()

for finger in fingers_data:
	current_finger = Finger(**finger)
	db.session.add(current_finger)

for location in locations_data:
	current_location = Location(**location)
	db.session.add(current_location)

db.session.commit()