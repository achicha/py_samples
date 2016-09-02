from flask import render_template, Blueprint
from project.models import *
from flask_login import login_required

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


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

