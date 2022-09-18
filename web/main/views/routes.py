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
@bp.route("/main")
def main():
	return render_template("main.html")


@bp.route("/sender")
def sender():
	return render_template("sender.html")


@bp.route("/customer")
def client():
	return render_template("timeline.html")