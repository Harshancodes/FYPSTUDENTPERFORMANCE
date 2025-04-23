from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class UserProfile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    behaviour=db.Column(db.Integer,nullable=True)
    sleep=db.Column(db.Integer,nullable=True)
    performance=db.Column(db.Integer,nullable=True)