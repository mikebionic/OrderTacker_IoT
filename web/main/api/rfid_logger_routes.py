from flask import make_response, abort, request, jsonify

from . import api
from main import db
from main.models import Access_log, Finger, Location, Order



@api.route("/order_locator/")
def order_locator():
	code = request.args.get("code",None,str)
	location = request.args.get("location","",str)
	location_key = request.args.get("location_key","",str)
	entrance_type = request.args.get("entrance_type","",str)
	description = request.args.get("description","",str)

	if not code:
		abort(400)
	order = Order.query.filter_by(card_code = code, completed=False).first()
	if not order:
		abort(404)
	this_location = Location.query\
		.filter(Location.key.ilike(f"%{location_key}%"))\
		.first()

	this_entrance_type = 0 if entrance_type == "exit" else 1
	new_log_data = {
		"order_code": order.order_code,
		"entrance_type": this_entrance_type,
		"location_id": this_location.id if this_location else None,
		"location_info": location if location else f"{this_location.address} {this_location.full_name}" if this_location else "Unknown",
		"description": description,
	}

	new_log = Access_log(**new_log_data)
	db.session.add(new_log)
	print(new_log.to_json())
	db.session.commit()

	return make_response({
		"location": this_location.to_json(),
		"access_log": new_log.to_json(),
		"entrance_type": this_entrance_type,
	})


@api.route("/rfid_logger/")
def rfid_logger():
	code = request.args.get("code",None,str)
	location = request.args.get("location","",str)
	location_key = request.args.get("location_key","",str)
	entrance_type = request.args.get("entrance_type","",str)

	if not code:
		abort(400)
	this_finger = Finger.query.filter_by(code = code).first()
	if not this_finger:
		abort(404)

	this_user = this_finger.user.to_json() if this_finger.user else None
	this_location = Location.query\
		.filter(Location.key.ilike(f"%{location_key}%"))\
		.first()

	this_entrance_type = 0 if entrance_type == "exit" else 1

	if not entrance_type:
		last_log = Access_log.query\
			.filter_by(finger_id = this_finger.id)
		if this_location:
			last_log = last_log.filter(Access_log.location_id == this_location.id)
		
		last_log = last_log.order_by(Access_log.date.desc())\
			.first()
		if last_log:
			print(last_log.to_json())
			if last_log.entrance_type == 1:
				this_entrance_type = 0

	new_log_data = {
		"finger_id": this_finger.id,
		"entrance_type": this_entrance_type,
		"location_id": this_location.id if this_location else None,
		"location_info": location if location else f"{this_location.address} {this_location.full_name}",
	}

	new_log = Access_log(**new_log_data)
	db.session.add(new_log)
	db.session.commit()

	return make_response({
		"user": this_user,
		"location": this_location.to_json(),
		"entrance_type": this_entrance_type,
	})


@api.route("/access_logs/")
def access_logs():
	filtering = {}

	finger_id = request.args.get("finger_id",None,str)
	if finger_id:
		filtering["finger_id"] = finger_id

	access_type = request.args.get("access_type",None,str)
	if access_type:
		filtering["access_type"] = access_type

	entrance_type = request.args.get("entrance_type",None,str)
	if entrance_type:
		filtering["entrance_type"] = entrance_type
	
	location_id = request.args.get("location_id",None,str)
	if location_id:
		filtering["location_id"] = location_id

	logs = Access_log.query\
		.order_by(Access_log.id.desc())\
		.filter_by(**filtering)\
		.all()
	logs_list = [log.to_json() for log in logs]
	print(logs_list)
	return make_response(jsonify(logs_list))