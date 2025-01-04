"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""
import os
import sys

import configparser
import pendulum
import requests
import json
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, redirect, render_template, url_for, request, jsonify, flash
from flask_sslify import SSLify
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user # UserMixin, 
from pydantic import BaseModel
from square.client import Client
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
# from application_automation.routes import application_bp
# from course_management.routes import course_bp
# from models import db, User, Application, Course, Assignment, Submission, Message
# from config import Config

load_dotenv(find_dotenv(usecwd=True))

# Gracefully handle running locally without eventbrite token
try:
    eventbrite = Eventbrite(os.environ["EVENTBRITE_OAUTH_TOKEN"])
except BaseException:
    print("Not able to authenticate to Eventbrite")

app = Flask(__name__)
sslify = SSLify(app)


# MAIN HANDLERS
@app.route("/")
def render_home_page():
    """
    Renders the home page from jinja2 template
    """
    try:
        events = get_events()
        return render_template("home.html", events=events)
    except BaseException:
        return render_template("home.html")


@app.route("/team/")
def render_team_page():
    """
    Renders the team page from jinja2 template
    """
    return render_template("team.html")


@app.route("/careers/")
def render_careers_page():
    """
    Renders the careers page from jinja2 template
    """
    return redirect(url_for("render_openings_page"))


@app.route("/conduct/")
def render_conduct_page():
    """
    Renders the conduct page from jinja2 template
    """
    return render_template("conduct.html")


@app.route("/privacy/")
def render_privacy_page():
    """
    Renders the privacy page from jinja2 template
    """
    return render_template("privacy.html")


@app.route("/thankyou/")
def render_thankyou_page():
    """
    Renders the newsletter signup's thank you page from jinja2 template.
    """
    return render_template("thankyou.html")


@app.route("/sponsor/")
def render_sponsor_page():
    """
    Renders the sponsor page from jinja2 template
    """
    return render_template("sponsor.html")


@app.route("/faqs/")
def render_faqs_page():
    """
    Renders the FAQs page from jinja2 template
    """
    return render_template("faqs.html")


@app.route("/openings/")
def render_openings_page():
    """
    Renders the openings page from jinja2 template
    """
    return render_template("openings.html")


# @app.route("/openings/stem/")
# def render_stem_page():
#     """
#     Renders the STEM page from jinja2 template
#     """
#     return render_template("stem.html")


# @app.route("/openings/tapm/")
# def render_tapm_page():
#     """
#     Renders the TAPM page from jinja2 template
#     """
#     return render_template("tapm.html")

@app.route("/openings/ta/")
def render_ta_page():
    """
    Renders the TA page from jinja2 template
    """
    return render_template("ta.html")


# @app.route("/openings/partnershipsmanager/")
# def render_partnershipsmanager_page():
#     """
#     Renders the Partnerships Manager JD from jinja2 template
#     """
#     return render_template("partnershipsmanager.html")

@app.route("/openings/sponsorshipslead/")
def render_sponsorshipslead_page():
    """
    Renders the Sponsorships Lead JD from jinja2 template
    """
    return render_template("sponsorshipslead.html")

# @app.route("/openings/curriculumdev/")
# def render_curriculumdev_page():
#     """
#     Renders the curriculum dev page from jinja2 template
#     """
#     return render_template("curriculumdev.html")


@app.route("/openings/board/")
def render_board_page():
    """
    Renders the board page from jinja2 template
    """
    return render_template("board.html")


@app.route("/mentor/")
def render_mentor_page():
    """
    Renders the mentor page from jinja2 template
    """
    return render_template("mentor.html")

@app.route("/full-time-program/")
def render_ft_program_page():
    """
    Renders the full-time program page from jinja2 template
    """
    return render_template("full-time-program.html")


@app.route("/donate/")
def render_donate_page():
    """
    Renders the donate page from jinja2 template
    """
    return render_template("donate.html")

@app.route("/volunteer/")
def render_volunteer_page():
    """
    Renders the volunteer page from jinja2 template
    """
    return render_template("volunteer.html")


@app.route("/news/")
def render_news_page():
    """
    Renders the news page from jinja2 template
    """
    return render_template("news.html")

@app.route("/testimonials/")
def render_testimonials_page():
    """
    Renders the news page from jinja2 template
    """
    return render_template("testimonials.html")

def get_events():
    try:
        group_id = eventbrite.get_user()["id"]
        response = eventbrite.get(
            f"/organizations/{group_id}/events/",
            data={"status": "live", "order_by": "start_asc", "page_size": 4},
            expand=("venue",),
        )
        events = [Event(event) for event in response["events"]]
        return events
    except NameError:
        # Gracefully handle failures getting events from Eventbrite
        print("Not returning Eventbrite Events:", sys.exc_info()[1])
        return []


class Event(object):
    def __init__(self, event):
        self.title = event["name"]["text"]
        self.url = event["url"]
        self.venue = None
        self.address = None
        self.date = (
            pendulum.parse(event["start"]["local"])
            .set(tz=event["start"]["timezone"])
            .format("MMMM D, YYYY, h:mmA zz")
        )

        if event["venue"]:
            self.venue = event["venue"]["name"]
            self.address = event["venue"]["address"][
                "localized_multi_line_address_display"
            ]


# ONLINE PAYMENT HANDLING ********************************************************

# Config setting
config = configparser.ConfigParser()
config.read("config.ini")

# Slack credentials
SLACK_WEBHOOK = config.get("slack", "slack_webhook")

# Square credentials
CONFIG_TYPE = config.get("default", "environment")
if CONFIG_TYPE == "production":
    PAYMENT_FORM_URL = "https://web.squarecdn.com/v1/square.js"
else:
    PAYMENT_FORM_URL= "https://sandbox.web.squarecdn.com/v1/square.js"
# PAYMENT_FORM_URL = (
#     "https://web.squarecdn.com/v1/square.js"
#     if CONFIG_TYPE == "production"
#     else "https://sandbox.web.squarecdn.com/v1/square.js"
# )
APPLICATION_ID = config.get(CONFIG_TYPE, "square_application_id")
LOCATION_ID = config.get(CONFIG_TYPE, "square_location_id")
ACCESS_TOKEN = config.get(CONFIG_TYPE, "square_access_token")

client = Client(
    access_token=ACCESS_TOKEN,
    environment=config.get("default", "environment"),
    user_agent_detail="techtonica_payment",
)

class Payment(BaseModel):
    token: str
    idempotencyKey: str

#old route - redirects to avoid breaking old links
@app.route("/payment-form")
def render_payment_form():
    """
    Redirects to current job-form route
    """
    return redirect(url_for('render_job_form'))

@app.route("/share-a-job")
def render_job_form():
    """
    Renders the job-form page from jinja2 template
    """
    return render_template("job-form.html",
        APPLICATION_ID=APPLICATION_ID,
        PAYMENT_FORM_URL=PAYMENT_FORM_URL,
        LOCATION_ID=LOCATION_ID,
        ACCOUNT_CURRENCY="USD",
        ACCOUNT_COUNTRY="ACCOUNT_COUNTRY",
        idempotencyKey=str( uuid4() ))

# Square payment api route
@app.route("/process-payment", methods = ['POST'])
def create_payment():
    # Charge the customer's card
    account_currency = "USD" # TODO: Are you hard-coding this to USD?
    data = request.json
    print(data)

    create_payment_response = client.payments.create_payment(
        body={
            "source_id": data.get('token'),
            "idempotency_key": data.get('idempotencyKey'),
            "amount_money": {
                "amount": 10000,  # $100.00 charge
                "currency": account_currency,
            },
        }
    )

    print("Payment created", create_payment_response)
    if create_payment_response.is_success():
        print('success')
        return create_payment_response.body
    elif create_payment_response.is_error():
        print('error')
        return {'errors': create_payment_response.errors}

# Slack webhook route
@app.route('/send-posting', methods=['POST'])
def send_posting():
    data = request.json
    print(f"Received data: {data}")

    x = requests.post(SLACK_WEBHOOK,
        json = {'text': f"A new job has been posted to Techtonica! Read the details below to see if you're a good fit!  \n\n JOB DETAILS \n Job Title: {data['jobTitle']} \n Company: {data['company']} \n Type: {data['type']} \n Education Requirement: {data['educationReq']} \n Location: {data['location']} \n Referral offered: {data['referral']} \n Salary Range: {data['salaryRange']} \n Description: {data['description']} \n Application Link: {data['applicationLink']} \n \n CONTACT INFO \n Name: {data['firstName']} {data['lastName']}  \n Email: {data['email']}  \n "})

    print(f"Message sent: {x.text}")
    return jsonify({'message': 'Data received successfully', 'received_data': data})



# ===========================================================
# Application Automation & Course Management System Routes
# ===========================================================

# app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/apply') #, methods=['GET', 'POST'])
def application_form():
    # if request.method == 'POST':
    #     application = Application(
    #         full_name=request.form['full_name'],
    #         email=request.form['email'],
    #         program=request.form['program'],
    #         statement=request.form['statement'],
    #         user_id=current_user.id if current_user.is_authenticated else None
    #     )
    #     db.session.add(application)
    #     db.session.commit()
        # flash('Application submitted successfully!', 'success')
        # return redirect(url_for('application_dashboard'))
    return render_template('application_form.html')

@app.route('/application-dashboard')
@login_required
def application_dashboard():
    # application = Application.query.filter_by(user_id=current_user.id).first()
    # messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('application_dashboard.html') #, application=application, messages=messages)

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    # applications = Application.query.order_by(Application.created_at.desc()).limit(10).all()
    return render_template('admin_dashboard.html') #, applications=applications)

@app.route('/participant-dashboard')
@login_required
def participant_dashboard():
    if not current_user.is_participant:
        flash('Access denied. Participant privileges required.', 'error')
        return redirect(url_for('index'))
    enrolled_courses = current_user.enrolled_courses
    # assignments = Assignment.query.filter(Assignment.course_id.in_([c.id for c in enrolled_courses])).all()
    return render_template('participant_dashboard.html', courses=enrolled_courses) #, assignments=assignments)

@app.route('/staff-dashboard')
@login_required
def staff_dashboard():
    if not current_user.is_staff:
        flash('Access denied. Staff privileges required.', 'error')
        return redirect(url_for('index'))
    # courses = Course.query.filter_by(staff_id=current_user.id).all()
    return render_template('staff_dashboard.html') #, courses=courses)

@app.route('/course/<int:course_id>')
@login_required
def course_content(course_id):
    # course = Course.query.get_or_404(course_id)
    return render_template('course_content.html') #, course=course)

@app.route('/assignment/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def assignment_submission(assignment_id):
    # assignment = Assignment.query.get_or_404(assignment_id)
    # if request.method == 'POST':
    #     submission = Submission(
    #         assignment_id=assignment_id,
    #         participant_id=current_user.id,
    #         content=request.form['content']
    #     )
    #     db.session.add(submission)
    #     db.session.commit()
    #     flash('Assignment submitted successfully!', 'success')
    #     return redirect(url_for('participant_dashboard'))
    return render_template('assignment_submission.html') #, assignment=assignment)

@app.route('/sign-in') #, methods=['GET', 'POST'])
def sign_in():
    # if request.method == 'POST':
    #     user = User.query.filter_by(username=request.form['username']).first()
    #     if user and check_password_hash(user.password_hash, request.form['password']):
    #         login_user(user)
    #         return redirect(url_for('index'))
    #     flash('Invalid username or password', 'error')
    return render_template('sign_in.html')

@app.route('/register') #, methods=['GET', 'POST'])
def register():
    # if request.method == 'POST':
    #     user = User(
    #         username=request.form['username'],
    #         email=request.form['email'],
    #         password_hash=generate_password_hash(request.form['password'])
    #     )
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Registration successful. Please sign in.', 'success')
    #     return redirect(url_for('sign_in'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# app.register_blueprint(application_bp, url_prefix='/application')
# app.register_blueprint(course_bp, url_prefix='/course')

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# @app.route('/applicant-to-participant')
# @login_required
# def applicant_to_participant():
#     if not current_user.is_admin:
#         flash('Access denied. Admin privileges required.', 'error')
#         return redirect(url_for('participant_dashboard'))
#     accepted_applicants = Application.query.filter_by(status='Accepted').all()
#     return render_template('applicant_to_participant.html', accepted_applicants=accepted_applicants)

# @app.route('/enroll-participant/<int:applicant_id>')
# @login_required
# def enroll_participant(applicant_id):
#     if not current_user.is_admin:
#         flash('Access denied. Admin privileges required.', 'error')
#         return redirect(url_for('participant_dashboard'))
#     applicant = Application.query.get_or_404(applicant_id)
#     # Create a new participant user
#     participant = User(username=f"participant_{applicant.id}", email=applicant.email, is_staff=False)
#     participant.set_password(generate_password())  # Generate a random password
#     db.session.add(participant)
#     # Update application status
#     applicant.status = 'Enrolled'
#     db.session.commit()
#     # Send enrollment confirmation email with login credentials
#     send_enrollment_email(participant.email, participant.username, participant.password)
#     flash(f'{applicant.full_name} has been enrolled as a participant.', 'success')
#     return redirect(url_for('applicant_to_participant'))

# @app.route('/transition-to-participant')
# @login_required
# def transition_to_participant():
#     application = Application.query.filter_by(user_id=current_user.id, status='Accepted').first()
#     if not application:
#         flash('You do not have an accepted application.', 'error')
#         return redirect(url_for('application_dashboard'))
#     return render_template('transition_to_participant.html', application=application)

# @app.route('/complete-transition', methods=['POST'])
# @login_required
# def complete_transition():
#     application = Application.query.filter_by(user_id=current_user.id, status='Accepted').first()
#     if not application:
#         flash('You do not have an accepted application.', 'error')
#         return redirect(url_for('application_dashboard'))
#     # Update user to participant status
#     current_user.is_participant = True
#     current_user.participant_id = request.form['participant_id']
#     current_user.program = application.program
#     current_user.start_date = request.form['start_date']
#     # Update application status
#     application.status = 'Enrolled'
#     db.session.commit()
#     flash('You have successfully enrolled as a participant!', 'success')
#     return redirect(url_for('participant_dashboard'))


if __name__ == "__main__":
    app.debug = False
    db.create_all()
    # app.run(host='0.0.0.0', port=9999)