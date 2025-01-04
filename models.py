# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from datetime import datetime

# db = SQLAlchemy()

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     is_admin = db.Column(db.Boolean, default=False)
#     is_participant = db.Column(db.Boolean, default=False)
#     is_staff = db.Column(db.Boolean, default=False)

# class Application(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     program = db.Column(db.String(50), nullable=False)
#     statement = db.Column(db.Text, nullable=False)
#     status = db.Column(db.String(20), default='Submitted')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref=db.backref('applications', lazy=True))

# class Course(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     staff = db.relationship('User', backref=db.backref('courses_taught', lazy=True))

# class Assignment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     due_date = db.Column(db.DateTime, nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
#     course = db.relationship('Course', backref=db.backref('assignments', lazy=True))

# class Submission(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
#     grade = db.Column(db.Float)
#     assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
#     participant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     assignment = db.relationship('Assignment', backref=db.backref('submissions', lazy=True))
#     participant = db.relationship('User', backref=db.backref('submissions', lazy=True))

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     sender = db.Column(db.String(50), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('messages', lazy=True))

# enrollments = db.Table('enrollments',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
# )

# User.enrolled_courses = db.relationship('Course', secondary=enrollments, lazy='subquery',
#     backref=db.backref('participants', lazy=True))

# # class Enrollment(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# #     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)