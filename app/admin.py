from flask import Blueprint
from . import db

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin')
def admin():
    return 'Admin'
