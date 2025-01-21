from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Course, User
from flask_login import login_required, current_user

course_bp = Blueprint('course', __name__)

@course_bp.route('/list')
def list():
    courses = Course.query.all()
    return render_template('course/list.html', courses=courses)

@course_bp.route('/<int:course_id>')
def detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course/detail.html', course=course)

@course_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_program_staff:
        flash('You must be program staff to create a course.', 'error')
        return redirect(url_for('course.list'))

    if request.method == 'POST':
        new_course = Course(
            title=request.form['title'],
            description=request.form['description'],
            program_staff_id=current_user.id
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('course.list'))
    return render_template('course/create.html')

@course_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.program_staff_id:
        flash('You can only edit your own courses.', 'error')
        return redirect(url_for('course.list'))

    if request.method == 'POST':
        course.title = request.form['title']
        course.description = request.form['description']
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('course.detail', course_id=course.id))
    return render_template('course/edit.html', course=course)

@course_bp.route('/<int:course_id>/delete', methods=['POST'])
@login_required
def delete(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user.id != course.program_staff_id:
        flash('You can only delete your own courses.', 'error')
        return redirect(url_for('course.list'))

    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('course.list'))

@course_bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user in course.participants:
        flash('You are already enrolled in this course.', 'info')
    else:
        course.participants.append(current_user)
        db.session.commit()
        flash('You have successfully enrolled in the course.', 'success')
    return redirect(url_for('course.detail', course_id=course.id))

@course_bp.route('/<int:course_id>/unenroll', methods=['POST'])
@login_required
def unenroll(course_id):
    course = Course.query.get_or_404(course_id)
    if current_user in course.participants:
        course.participants.remove(current_user)
        db.session.commit()
        flash('You have successfully unenrolled from the course.', 'success')
    else:
        flash('You are not enrolled in this course.', 'info')
    return redirect(url_for('course.detail', course_id=course.id))