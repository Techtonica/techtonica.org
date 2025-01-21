from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Application

application_bp = Blueprint('application', __name__)

@application_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        new_application = Application(
            full_name=request.form['full_name'],
            email=request.form['email'],
            program=request.form['program']
        )
        db.session.add(new_application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('application.dashboard'))
    return render_template('application/form.html')

@application_bp.route('/dashboard')
def dashboard():
    applications = Application.query.all()
    return render_template('application/dashboard.html', applications=applications)