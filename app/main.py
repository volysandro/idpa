from flask import Blueprint, render_template, url_for, redirect, request
from . import db
from flask_login import current_user, login_required
from .userlogic import enrol, gather_info, gather_grades, submit_grade, get_subjects, submit_absence, gather_absences, get_special_tests, submit_special_grade, gather_special_grades, gather_subject_grades, delete_grade
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
    return render_template("profile.html", info=gather_info(current_user.id), grades=gather_grades(current_user.id), user=current_user, absences=gather_absences(current_user.id), specials=gather_special_grades(current_user.id))

@main_blueprint.route('/enterclass')
def enterclass():
    return render_template('enterclass.html')

@main_blueprint.route('/submitclasskey', methods = ["POST"])
def submitclasskey():
    key = request.form.get("key")
    enrol(current_user.id, key)
    return redirect('/profile')

@main_blueprint.route('/grades/submit')
def newgrade():
    return render_template("newgrade.html", subjects=get_subjects(current_user.id))

@main_blueprint.route('/absences/submit')
def newabsence():
    return render_template("newabsence.html", subjects=get_subjects(current_user.id))

@main_blueprint.route('/specialgrades/submit')
def newspecialgrade():
    return render_template("newspecialgrade.html", tests=get_special_tests(current_user.id))

@main_blueprint.route('/user/api/grade/submit', methods = ["POST"])
def submitgrade():
    s_id = request.form.get("subject")
    grade = request.form.get("grade")
    final = request.form.get("final")
    submit_grade(current_user.id, s_id, grade, final)
    return redirect('/profile')

@main_blueprint.route('/user/api/absence/submit', methods = ["POST"])
def submitabsence():
    s_id = request.form.get("subject")
    count = request.form.get("count")
    submit_absence(current_user.id, s_id, count)
    return redirect('/profile')

@main_blueprint.route('/user/api/specialgrade/submit', methods = ["POST"])
def submitspecialgrade():
    t_id = request.form.get("test")
    grade = request.form.get("grade")
    submit_special_grade(current_user.id, t_id, grade)
    return "OK"


@main_blueprint.route("/grades/<subject>/")
def gradesforsubject(subject):
    id = subject
    user_id = current_user.id
    return render_template("grades.html", grades=gather_subject_grades(current_user.id, id))

@main_blueprint.route("/api/grades/<id>/delete")
def deletegrade(id):
    delete_grade(id)
    return redirect("/profile")