from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from . import db
from .models import User
import json
from .decorators import manager_required

manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/manager')
@manager_required
def index():
    if not current_user.class_id:
        return redirect(url_for('manager.setup'))
    return "Hello Manager"

@manager_blueprint.route('/manager/setup')
@manager_required
def setup():
    return "Setup"



