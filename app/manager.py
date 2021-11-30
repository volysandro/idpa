from flask import Blueprint, render_template, redirect, url_for
from . import db
from .models import User
import json
from .decorators import manager_required

manager_blueprint = Blueprint('manager', __name__)

@manager_blueprint.route('/manager')
@manager_required
def manager_index():
    return "Hello Manager"