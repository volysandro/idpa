from flask import Blueprint, render_template, url_for, redirect, request
from . import db
from flask_login import current_user, login_required
from .userlogic import enrol, gather_info
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    if current_user.manager == True:
        return redirect(url_for("manager.index"))
    if not current_user.class_id:
        return redirect("/enterclass")
    return redirect('/profile')

@main_blueprint.route('/profile')
@login_required
def profile():
    return render_template("profile.html", info=gather_info(current_user.id))

@main_blueprint.route('/enterclass')
def enterclass():
    return render_template('enterclass.html')

@main_blueprint.route('/submitclasskey', methods = ["POST"])
def submitclasskey():
    key = request.form.get("key")
    enrol(current_user.id, key)
    return redirect('/profile')