from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# contain the database models for both the application process and course management

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_participant = db.Column(db.Boolean, default=False)
    is_program_staff = db.Column(db.Boolean, default=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    program = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Submitted')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('applications', lazy=True))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    program_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    program_staff = db.relationship('User', backref=db.backref('courses_taught', lazy=True))