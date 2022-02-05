from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login')
def login():
    return render_template('login.html')

@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    if not user.active:
        flash('This manager account is not active yet. Please notify a site administrator or wait until he enables the account.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    manager = True if request.form.get('manager') else False
    active = True if request.form.get('manager') else True
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    admin=False
    if len(User.query.all()) == 0:
        admin=True

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), manager=manager, active=active, admin=admin)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))