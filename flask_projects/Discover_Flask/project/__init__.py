from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

################
# project config
################

# create the application object
app = Flask(__name__)
app.config.from_object('config.DevConfig')  # import config from file
bcrypt = Bcrypt(app)

# create sqlalchemy object
db = SQLAlchemy(app)

# import models
from project.users.views import users_blueprint
from project.home.views import home_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
