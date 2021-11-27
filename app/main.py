from flask import Blueprint, render_template
from . import db

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/profile')
def profile():
    return 'Profile'