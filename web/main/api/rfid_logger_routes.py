from flask import make_response, abort, request


from main import app, db
from main.models import Access_log, Finger


@app.route("/rfid_logger/")
def rfid_logger():
	code = request.args.get("code",None,str)
	if not code:
		abort(400)


	this_finger = Finger.query.filter_by(code = code).first()
	if not this_finger:
		abort(404)

	this_user = this_finger.user
	print(this_user)

	return make_response(this_user.to_json())


