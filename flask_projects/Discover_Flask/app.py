from flask import Flask, render_template, request, redirect, \
    url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

################
# config
################

# create the application object
app = Flask(__name__)
app.config.from_object('config.DevConfig')  # import config from file
bcrypt = Bcrypt(app)


# create sqlalchemy object
db = SQLAlchemy(app)

# import models
from models import *
from project.users.views import users_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('users.login'))
    return wrapper


################
# routes
################

# use decorators to link the function to an url
@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost)
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0')
