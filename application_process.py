from flask import Blueprint, render_template, request, redirect, url_for, flash

application_bp = Blueprint('application', __name__)

@application_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Simulate form submission without database
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('application.dashboard'))
    return render_template('application/form.html')

@application_bp.route('/dashboard')
def dashboard():
    # Simulate fetching applications
    applications = [
        {'full_name': 'John Doe', 'email': 'john@example.com', 'program': 'Computer Science', 'status': 'Submitted'},
        {'full_name': 'Jane Smith', 'email': 'jane@example.com', 'program': 'Engineering', 'status': 'Under Review'}
    ]
    return render_template('application/dashboard.html', applications=applications)