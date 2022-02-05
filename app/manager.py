from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from . import db
from .models import User, Class
from .configparser import parse
import json
from .decorators import manager_required
from random import choice
from string import ascii_uppercase


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
    return render_template("classsetup.html")

@manager_blueprint.route('/manager/setup/initclass', methods=['POST'])
@manager_required
def init_class():
    name = request.form.get("name")
    if Class.query.filter_by(class_name=name).first():
        return "Class name already exists"
    new_class = Class(class_name = name, invite_key = ''.join(choice(ascii_uppercase) for i in range(8)))
    db.session.add(new_class)
    db.session.commit()
    manager = User.query.filter_by(id=current_user.id).first()
    manager.class_id = Class.query.filter_by(class_name=name).first().id
    db.session.commit()
    return redirect(url_for('manager.configform'))


@manager_blueprint.route('/manager/setup/configform')
@manager_required
def configform():
    invite_key = Class.query.filter_by(id=current_user.class_id).first().invite_key
    return render_template("configform.html", invite_key=invite_key)

@manager_blueprint.route('/manager/setup/addconfig', methods=["POST"])
@manager_required
def addconfig():
    config = request.form.get("config")
    print(config)
    rsp = parse(config)
    if rsp == "NOK_REQ":
        return "Config is not complete"
    elif rsp == "NOK_NEX":
        return "Class name specified does not exist"
    elif rsp == "NOK_PTL":
        return "Minimum presence specified does not meet the percentile requirement"
    elif rsp == "NOK_WCT":
        return "Week count does not meet requirements or is straight up cruel (must be between 10 and 50)"
    elif rsp == "NOK_SJK":
        return "Something seems off with the subject-bucket keys"

    return "Parsing"