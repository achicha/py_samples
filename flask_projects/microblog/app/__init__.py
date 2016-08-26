from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

# app
app = Flask(__name__)
app.config.from_object('config')
# login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
# database
db = SQLAlchemy(app)

from app import views, models
