from flask import Blueprint, render_template
from . import db
from flask_login import current_user

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/profile')
def profile():
    return current_user.name + "   " + current_user.email