from flask import (
	render_template,
)
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