from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Application
from app import db

application_bp = Blueprint('application', __name__)

@application_bp.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        # Process application form submission
        new_application = Application(
            user_id=current_user.id,
            name=request.form['name'],
            email=request.form['email'],
            # Add other fields as necessary
        )
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for('application.dashboard'))
    return render_template('application_automation/application_form.html')

@application_bp.route('/dashboard')
@login_required
def dashboard():
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('application_automation/applicant_dashboard.html', applications=applications)

@application_bp.route('/admin')
@login_required
def admin_dashboard():
    # Add admin check here
    applications = Application.query.all()
    return render_template('application_automation/admin_dashboard.html', applications=applications)