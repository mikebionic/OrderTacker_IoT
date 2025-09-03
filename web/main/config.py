import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PIN = os.environ.get('ADMIN_PIN') or '1234'
    DEVICE_SECRET = os.environ.get('DEVICE_SECRET') or 'finger_secret_key'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    SESSION_PROTECTION = 'strong'
    
    CORS_ORIGINS = ['*']  # Change this to specific origins in production
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True