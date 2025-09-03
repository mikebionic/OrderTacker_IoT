from flask import make_response, abort, request, jsonify, current_app
from datetime import datetime
from sqlalchemy.orm import joinedload
from flask_login import current_user

from . import api
from main import db
from main.models import Access_log, Finger, Location, User


@api.route("/rfid_logger/")
def rfid_logger():
	code = request.args.get("code", None, str)
	location = request.args.get("location", "entrance", str)

	if not code:
		abort(400)
	
	this_finger = Finger.query.filter_by(code=code).first()
	if not this_finger:
		abort(404)

	this_user = this_finger.user
	this_location = Location.query\
		.filter(Location.name.ilike(f"%{location}%"))\
		.first()

	last_log = Access_log.query\
		.filter_by(finger_id=this_finger.id)
	
	if this_location:
		last_log = last_log.filter(Access_log.location_id == this_location.id)
	
	last_log = last_log.order_by(Access_log.date.desc())\
		.first()

	this_entrance_type = 1
	if last_log:
		print(last_log.to_json())
		if last_log.entrance_type == 1:
			this_entrance_type = 0

	new_log_data = {
		"finger_id": this_finger.id,
		"entrance_type": this_entrance_type,
		"location_id": this_location.id if this_location else None,
	}

	new_log = Access_log(**new_log_data)
	db.session.add(new_log)
	db.session.commit()

	return make_response({
		"user": this_user.to_json(),
		"location": this_location.to_json() if this_location else None,
		"entrance_type": this_entrance_type, 
	})


@api.route("/access_logs/")
def access_logs():
	filtering = {}

	finger_id = request.args.get("finger_id", None, str)
	if finger_id:
		filtering["finger_id"] = finger_id

	access_type = request.args.get("access_type", None, str)
	if access_type:
		filtering["access_type"] = access_type

	entrance_type = request.args.get("entrance_type", None, str)
	if entrance_type:
		filtering["entrance_type"] = entrance_type
	
	location_id = request.args.get("location_id", None, str)
	if location_id:
		filtering["location_id"] = location_id

	print(filtering)
	logs = Access_log.query\
		.order_by(Access_log.id.desc())\
		.filter_by(**filtering)\
		.all()
	
	logs_list = [log.to_json() for log in logs]
	print(logs_list)
	return make_response(jsonify(logs_list))


@api.route("/finger_logger/")
def finger_logger():
	device_key = request.args.get("device_key", None, str)
	finger_id = request.args.get("finger_id", 0, int)
	access_type = request.args.get("access_type", None, str)

	if not device_key:
		abort(400)
	
	if not finger_id and not access_type:
		abort(400)

	if device_key != current_app.config["DEVICE_SECRET"]:
		abort(401)

	if finger_id:
		this_finger = Finger.query.filter_by(id=finger_id).first()
		if not this_finger:
			this_finger = Finger(
				user_id=None,
				code=str(finger_id),
				name=str(datetime.now())
			)
			db.session.add(this_finger)
			db.session.commit()
		
		new_log = Access_log(
			finger_id=this_finger.id,
			access_type="Fingerprint",
			date=datetime.now()
		)

	else:
		new_log = Access_log(
			access_type=access_type,
			date=datetime.now()
		)

	db.session.add(new_log)
	db.session.commit()

	return make_response('success'), 201


@api.route("/access_logs_auth/")
def access_logs_auth():
	if not current_user.is_authenticated:
		abort(401)

	logs = Access_log.query\
		.options(joinedload(Access_log.finger))\
		.order_by(Access_log.date.desc())\
		.all()

	data = []
	for log in logs:
		log_data = log.to_json()
		log_data["name"] = log.finger.name if log.finger else ''
		data.append(log_data)

	response = {
		"data": data,
		"total": len(logs),
		"message": "Access logs"
	}

	return make_response(response)


@api.route("/fingerprints_data/")
def fingers_data():
	if not current_user.is_authenticated:
		abort(401)

	fingers = Finger.query.all()

	response = {
		"data": [finger.to_json() for finger in fingers],
		"total": len(fingers),
		"message": "Finger data"
	}

	return make_response(response)


@api.route("/configure_fingerprint/", methods=["POST"])
def configure_fingerprint():
	if not current_user.is_authenticated:
		abort(401)
	
	if request.method == 'POST':
		data = {}

		request_data = request.get_json()
		finger_id = request_data.get("finger_id")
		name = request_data.get("name")

		this_finger = Finger.query.filter_by(id=finger_id).first()

		if this_finger and name:
			this_finger.name = name

			db.session.add(this_finger)
			db.session.commit()
			data = this_finger.to_json()

		response = {
			"data": data,
			"total": 1 if data else 0,
			"message": "Finger data"
		}

		return make_response(response)