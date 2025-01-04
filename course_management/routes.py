from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Course, Enrollment
from app import db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses')
@login_required
def course_list():
    courses = Course.query.all()
    return render_template('course_management/course_list.html', courses=courses)

@course_bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_management/course_detail.html', course=course)

@course_bp.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return redirect(url_for('course.course_detail', course_id=course_id))