from flask import (
	request,
	redirect,
	render_template,
	url_for
)
# from flask_login import login_required, current_user, login_user
# from main.models import User

from main import app


@app.route("/")
@app.route("/home")
@app.route("/app/access_logs")
def home():
	return render_template('home.html')