from flask import Blueprint, render_template, redirect, url_for
from . import db
from .models import User
import json
from .decorators import admin_required
from .admin_controller import list_manager

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin')
@admin_required
def admin():
    return render_template('admin.html', manager=list_manager())

@admin_blueprint.route('/admin/api/update/<id>/state')
@admin_required
def update_state(id):
    user = User.query.filter_by(id=id).first()
    if not user.active:
        user.active = True
    else:
        user.active = False
    db.session.commit()
    return redirect(url_for('admin.admin'))

@admin_blueprint.route('/admin/api/update/<id>/triggerreset')
@admin_required
def update_reset(id):
    user = User.query.filter_by(id=id).first()
    if not user.reset_upon_login:
        user.reset_upon_login = True
    else:
        user.reset_upon_login = False
    db.session.commit()
    return redirect(url_for('admin.admin'))


