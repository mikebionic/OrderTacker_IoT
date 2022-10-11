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
		forms_data = {
			"card_code": request.form.get('card_code'),
			"sender_name": request.form.get('sender_name'),
			"sender_surname": request.form.get('sender_surname'),
			"postal_phone_number": request.form.get('postal_phone_number'),
			"sender_phone_number": request.form.get('sender_phone_number'),
			"sender_email": request.form.get('sender_email'),
			"place_to_deliver": request.form.get('place_to_deliver'),
			"city": request.form.get('city'),
			"address": request.form.get('address'),
			"paid": request.form.get('paid'),
			"info": request.form.get('info'),
		}
		print(forms_data)
		
	return render_template("sender.html")


@bp.route("/customer")
def client():
	access_logs = Access_log.query.all()
	return render_template("timeline.html", access_logs = access_logs)