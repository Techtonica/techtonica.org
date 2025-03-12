from flask import Blueprint, render_template

course_bp = Blueprint('course', __name__)

@course_bp.route('/list')
def list():
    # Simulate fetching courses
    courses = [
        {'id': 1, 'title': 'Introduction to Python'},
        {'id': 2, 'title': 'Web Development Fundamentals'}
    ]
    return render_template('course/list.html', courses=courses)

@course_bp.route('/<int:course_id>')
def detail(course_id):
    # Simulate fetching a specific course
    course = {'id': course_id, 'title': f'Course {course_id}', 'description': 'Course description goes here.'}
    return render_template('course/detail.html', course=course)