from . import db
from .models import User, Class, Subject

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