from crypt import methods
from flask import (
	request,
	redirect,
	render_template,
	url_for
)
# from flask_login import login_required, current_user, login_user
# from main.models import User
from main.models import Order, Access_log

from . import bp


@bp.route("/")
@bp.route("/main")
def main():
	return render_template("main.html")


@bp.route("/sender", methods=["GET","POST"])
def sender():
	if request.method == "POST":
		name = request.form['firstName']
		print(name)
		forms_data = {
			"card_code": request.form['card_code'],
			"sender_name": request.form['sender_name'],
			"sender_surname": request.form['sender_surname'],
			"postal_phone_number": request.form['postal_phone_number'],
			"sender_phone_number": request.form['sender_phone_number'],
			"sender_email": request.form['sender_email'],
			"place_to_deliver": request.form['place_to_deliver'],
			"city": request.form['city'],
			"address": request.form['address'],
			"paid": request.form['paid'],
			"info": request.form['info'],
		}
		
	return render_template("sender.html")


@bp.route("/customer")
def client():
	access_logs = Access_log.query.all()
	return render_template("timeline.html", access_logs = access_logs)