from flask import Flask, render_template, request, redirect, \
    url_for, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
# import sqlite3


# create the application object
app = Flask(__name__)
app.config.from_object('config.DevConfig')  # import config from file


# create sqlalchemy object
db = SQLAlchemy(app)

# import models
from models import *


# login required decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrapper


# use decorators to link the function to an url
@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost)
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            # The url_for() function generates an endpoint for the provided method.
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

# def connect_db():
#     return sqlite3.connect('posts.db')

# start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0')
