from .models import User
from app import db

def list_manager():
    managers = User.query.filter_by(manager=True).all()
    list = []
    for manager in managers:
        list.append(manager)
    print(list)
    return list
    