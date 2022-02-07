from . import db
from .models import User, Class, Subject, Grade, Bucket, Absence
from datetime import datetime

def enrol(user_id, key):
    user = User.query.filter_by(id=user_id).first()
    class_id = Class.query.filter_by(invite_key=key).first().id
    print(class_id)
    user.class_id = class_id
    db.session.commit()
    

def gather_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    info_obj = {
        "class_name": "",
        "class_manager": "",
        "subjects_registered": []
    }
    if user.class_id:
        class_obj = Class.query.filter_by(id=user.class_id).first()
        info_obj["class_name"] = class_obj.class_name
        info_obj["class_manager"] = User.query.filter_by(class_id=user.class_id, manager=True).first().name
        subjects = Subject.query.filter_by(class_id=user.class_id)
        for subject in subjects:
            info_obj["subjects_registered"].append(subject.name)
    else:
        info_obj["class_name"] = "Not set."

    return info_obj

def gather_grades(user_id):
    ret_obj = {
        "averages": [],
        "bucket_averages": [],
        "grades": []
    }
    class_id = User.query.filter_by(id=user_id).first().class_id
    subjects = Subject.query.filter_by(class_id=class_id).all()
    buckets = Bucket.query.filter_by(class_id=class_id).all()

    for subject in subjects:
        grades = Grade.query.filter_by(user_id=user_id, subject_id=subject.id).all()
        sum = 0.0
        for grade in grades:
            sum += grade.value
        average = sum / len(grades)
        name = subject.name
        subject_id = subject.id
        ret_obj["averages"].append({
            "name": name,
            "average": average,
            "sid": subject_id
        })

    for bucket in buckets:
        subjects = Subject.query.filter_by(class_id=class_id, bucket_id=bucket.id).all()
        bucket_hundreth = 0
        for subject in subjects:
            grades = Grade.query.filter_by(user_id=user_id, subject_id=subject.id).all()
            sum = 0.0
            for grade in grades:
                sum += grade.value
            average = sum / len(grades)
            rounded_average = round(average*2)/2
            bucket_hundreth += rounded_average * subject.weight
        bucket_average = bucket_hundreth / 100
        ret_obj["bucket_averages"].append(
            {
                "name": bucket.name,
                "average": bucket_average
            })

    grades = Grade.query.filter_by(user_id=user_id).all()
    for grade in grades:
        ret_obj["grades"].append({"sid": grade.subject_id, "grade": grade.value})

    return ret_obj

def submit_grade(user_id, s_id, grade, final):
    grade = Grade(user_id=user_id, subject_id=s_id, value=grade, final=final, date=datetime.now())
    db.session.add(grade)
    db.session.commit()

def get_subjects(user_id):
    user = User.query.filter_by(id=user_id).first()
    class_id = Class.query.filter_by(id=user.class_id).first().id
    subjects = Subject.query.filter_by(class_id=class_id).all()
    print(subjects)
    return subjects


def submit_absence(user_id, s_id, count, date=datetime.now()):
    absence = Absence(user_id=user_id, subject_id=s_id, count=count)
    db.session.add(absence)
    db.session.commit()

def gather_absences(user_id):
    ret_obj = {
        "subjects": []
    }
    class_id = User.query.filter_by(id=user_id).first().class_id
    weeks = Class.query.filter_by(id=class_id).first().weeks
    min = Class.query.filter_by(id=class_id).first().min_presence
    subjects = Subject.query.filter_by(class_id=class_id).all()
    for subject in subjects:
        absences = Absence.query.filter_by(subject_id=subject.id, user_id=user_id).all()
        count = 0
        if len(absences) > 0:
            for absence in absences:
                count += absence.count
        ret_obj["subjects"].append({
            "count": count,
            "percentage": count / (weeks * subject.weekly) * 100,
            "min_satisfied": False if (count / (weeks * subject.weekly) * 100) > (100 - min) else True
        })
    return ret_obj