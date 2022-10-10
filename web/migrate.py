from main import db

from main.config import Config
from main.models import User, Finger, Location, Order

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
		"position": "Iş ýörediji",
		"pin": "",
		"avatar": "",
	},
	{
		"id":	3,
		"username": "jemal",
		"name": "Jemal",
		"surname": "Planyyewa",
		"patronomic": "Planyyewna",
		"position": "Mugallym",
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
		"code": "8A:4B:81:7F",
		"name": "",
	}
]


orders_data = [
	{
		"order_code": 1,
		"sender_name": "Muhammetberdi",
		"sender_surname": "Jepbarov",
		"postal_phone_number": "+99361234567",
		"sender_phone_number": "+99361234567",
		"sender_email": "plain@mail.com",
		"place_to_deliver": "warehouse",
		"city": "Ashgabat",
		"address": "Azadi 98/2",
		"paid": 1,
		"info": "",
	}
]

order_products_data = [
	{
		"order_code": 1,
		"product_name": "HP wireless optical mouse",
		"price": 110,
		"currency": "m.",
		"qty": 1,
	},
	{
		"order_code": 1,
		"product_name": "Air Pods",
		"price": 50,
		"currency": "m.",
		"qty": 3,
	},
	{
		"order_code": 1,
		"product_name": "Arduino Set #1",
		"price": 982,
		"currency": "m.",
		"qty": 1,
	}
]

locations_data = [
	{
		"id": 1,
		"name": "aeroport",
		"full_name": "International Aeroport of Turkmenistan",
		"address": "Gurbansoltan-eje",
		"key": "crypted_code_of_international_aeroport",
		"latitude": "11112",
		"longitude": "92323",
	},
	{
		"id": 2,
		"name": "entrance",
		"full_name": "Plan yerin girelgesi",
		"address": "Parahat 01",
		"key": "crypted_code_2",
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

for order in orders_data:
	current_order = Order(**order)
	db.session.add(current_order)

# db.session.commit()
#	for order_product in order_products_data:
#		#this_product_order = Order.query.filter_by(order_code == order['order_code']).first()
#		order_product["order_id"] = 1
#		current_product = Order_product(**order_product)

db.session.commit()