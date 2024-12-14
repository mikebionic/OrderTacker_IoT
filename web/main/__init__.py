from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from main.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_view = 'login_page'
login_manager.login_message = 'Ulgama girin!'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	CORS(app)
	db.init_app(app)
	login_manager.init_app(app)

	from main.api import api as main_api
	app.register_blueprint(main_api, url_prefix='/api')

	from main.views import bp as views_bp
	app.register_blueprint(views_bp)

	return app