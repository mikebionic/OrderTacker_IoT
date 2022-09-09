from flask import make_response, abort, request

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
	last_log = Access_log.query\
		.filter_by(finger_id = this_finger.id)\
		.order_by(date.desc())\
		.first()

	print(last_log.to_json())
	this_entrance_type = 1
	if last_log.entrance_type == 1:
		this_entrance_type = 0

	this_location = Location.query\
		.filter(Location.name.ilike(f"%{location}%"))\
		.first()

	new_log_data = {
		"finger_id": this_finger.id,
		"entrance_type": this_entrance_type,
		"location_id": this_location.id if this_location else None,
	}

	new_log = Access_log(**new_log)
	db.session.add(new_log)

	return make_response(this_user.to_json())



@app.route("/rfid_logs/")
def rfid_logs():

	logs = Access_log.query.filter_by(**filtering)
	return