from flask import render_template, redirect, \
    url_for, session, flash, Blueprint
from functools import wraps
from project import app, db
# import models
from project.models import *


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


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
@home_blueprint.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost)
    return render_template('index.html', posts=posts)


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

