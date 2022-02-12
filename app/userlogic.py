from . import db
from .models import User, Class, Subject, Grade, Bucket, Absence, SBucket, SGrade, STest
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
        average = sum / len(grades) if len(grades) > 0 else "No grades yet"
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
            average = sum / len(grades) if len(grades) > 0 else "No grades yet"
            rounded_average = round(average*2)/2 if len(grades) > 0 else "No grades yet"
            if len(grades) > 0:
                bucket_hundreth += rounded_average * subject.weight
        bucket_average = bucket_hundreth / 100
        ret_obj["bucket_averages"].append(
            {
                "name": bucket.name,
                "average": bucket_average
            })

    grades = Grade.query.filter_by(user_id=user_id).all()
    for grade in grades:
        ret_obj["grades"].append({"sid": grade.subject_id, "grade": grade.value, "date": grade.date.strftime("%m/%d/%Y, %H:%M:%S")})

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


def submit_absence(user_id, s_id, count):
    absence = Absence(user_id=user_id, subject_id=s_id, count=count, date=datetime.now())
    db.session.add(absence)
    db.session.commit()

def submit_special_grade(user_id, t_id, grade):
    sgrade = SGrade(user_id=user_id, sgrade_id=t_id, value=grade, date=datetime.now())
    db.session.add(sgrade)
    db.session.commit()

def get_special_tests(user_id):
    user = User.query.filter_by(id=user_id).first()
    class_id = Class.query.filter_by(id=user.class_id).first().id
    ssubjects = SBucket.query.filter_by(class_id=class_id).all()
    tests = []
    for subject in ssubjects:
        ids = subject.tests
        for test_id in ids:
            test = STest.query.filter_by(id=test_id).first()
            if not len(SGrade.query.filter_by(user_id=user_id, sgrade_id=test_id).all())>0:
                tests.append({
                    "name": test.name,
                    "id": test.id,
                    "integrity": test_id,
                    "subject": subject.name,
                    "weight": test.weight
                })
    if len(tests) == 0:
        tests.append(False)
    return tests

def gather_special_grades(user_id):
    user = User.query.filter_by(id=user_id).first()
    class_id = Class.query.filter_by(id=user.class_id).first().id
    ssubjects = SBucket.query.filter_by(class_id=class_id).all()
    ret = []
    for subject in ssubjects:
        name = subject.name
        test_ids = subject.tests

        append = {
            "name": name,
            "tests": test_ids,
            "grades": [],
            "average": 0.0
        }

        values_weighted = 0
        for test_id in test_ids:
            weight = STest.query.filter_by(id=test_id).first().weight
            sgrade = SGrade.query.filter_by(sgrade_id=test_id, user_id=user_id).first()
            if sgrade:
                value = sgrade.value
                date = sgrade.date
                sname = STest.query.filter_by(id=test_id).first().name
                values_weighted += (value * weight)
                append["grades"].append({
                    "name": sname,
                    "grade": value,
                    "date": date.strftime("%m/%d/%Y, %H:%M:%S"),
                    "weight": str(weight) + "%"
                })
        average = round((values_weighted / 100)/len(test_ids)*2)/2
        append["average"] = average
        ret.append(append)
    return ret


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
            "sid": subject.id,
            "name": subject.name,
            "count": count,
            "percentage": count / (weeks * subject.weekly) * 100,
            "min_satisfied": False if (count / (weeks * subject.weekly) * 100) > (100 - min) else True
        })
    return ret_obj

def gather_subject_grades(user_id, subject_id):
    user = User.query.filter_by(id=user_id).first()
    grades = Grade.query.filter_by(user_id=user_id, subject_id=subject_id).all()

    ret_obj = {
        "name": "",
        "grades":[]
    }
    ret_obj["name"] = Subject.query.filter_by(id=subject_id).first().name
    for grade in grades:
        ret_obj["grades"].append({
            "id": grade.id,
            "grade": grade.value,
            "date": grade.date.strftime("%m/%d/%Y, %H:%M:%S")
        })
    return ret_obj

def delete_grade(id, user_id):
    Grade.query.filter_by(id=id, user_id=user_id).delete()
    db.session.commit()

def delete_absence(id, user_id):
    Absence.query.filter_by(id=id, user_id=user_id).delete()
    db.session.commit()



def gather_subject_absences(user_id, subject_id):
    user = User.query.filter_by(id=user_id).first()
    subject = Subject.query.filter_by(id=subject_id).first()
    ret_obj = {
        "name": subject.name,
        "absences": []

    }

    if not user.class_id == subject.class_id:
        return "Dont try dumb stuff"
    absences = Absence.query.filter_by(subject_id=subject_id).all()
    for absence in absences:
        ret_obj["absences"].append({
            "date": absence.date,
            "lessons": absence.count,
            "id": absence.id
        })
    return ret_obj

