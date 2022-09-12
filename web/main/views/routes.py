from flask import (
	request,
	redirect,
	render_template,
	url_for
)
# from flask_login import login_required, current_user, login_user
# from main.models import User

from . import bp


@bp.route("/")
@bp.route("/home")
@bp.route("/app/access_logs")
def home():
	print("h")
	return render_template('home.html')