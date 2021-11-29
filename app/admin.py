from flask import Blueprint
from . import db
from .models import User
import json

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin')
def admin():
    return 'Admin'

@admin_blueprint.route('/admin/api/list_manager')
def list_manager():
    managers = User.query.filter_by(manager=True).all()
    list = []
    for manager in managers:
        list.append([manager.email, manager.name, manager.active, manager.reset_upon_login])
    print(list)
    return list
    
