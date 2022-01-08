from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    reset_upon_login = db.Column(db.Boolean, default=False)
    manager = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    invite_key = db.Column(db.String(8))
    config = db.Column(db.String(250))

