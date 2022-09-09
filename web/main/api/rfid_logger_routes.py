from flask import make_response, abort, request, jsonify

from main import app, db
from main.models import Access_log, Finger, Location


@app.route("/rfid_logger/")
def rfid_logger():
	code = request.args.get("code",None,str)
	location = request.args.get("location","entrance",str)

	if not code:
		abort(400)
	this_finger = Finger.query.filter_by(code = code).first()
	if not this_finger:
		abort(404)

	this_user = this_finger.user
	this_location = Location.query\
		.filter(Location.name.ilike(f"%{location}%"))\
		.first()

	last_log = Access_log.query\
		.filter_by(finger_id = this_finger.id)
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

	return make_response(this_user.to_json())


@app.route("/access_logs/")
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

	print(filtering)
	logs = Access_log.query\
		.order_by(Access_log.id.desc())\
		.filter_by(**filtering)\
		.all()
	logs_list = [log.to_json() for log in logs]
	print(logs_list)
	return make_response(jsonify(logs_list))