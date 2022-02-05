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
    min_presence = db.Column(db.Integer)
    weeks = db.Column(db.Integer)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    bucket_bool = db.Column(db.Boolean, default=False)
    bucket_id = db.Column(db.Integer)
    weight = db.Column(db.Integer, default=100)
    weekly = db.Column(db.Integer)
    finals = db.Column(db.Integer, default=50)

class Bucket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    name = db.Column(db.String(50))

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    subject_id = db.Column(db.Integer)
    final = db.Column(db.Boolean, default=False)


