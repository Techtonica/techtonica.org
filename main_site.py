"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""

import datetime
import os
import sys
from uuid import uuid4

import pendulum
import requests
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sslify import SSLify
from pydantic import BaseModel
from square.client import Client

from application_process import application_bp
from course_management import course_bp

load_dotenv(find_dotenv(usecwd=True))


# Gracefully handle running locally without eventbrite token
try:
    eventbrite = Eventbrite(os.environ["EVENTBRITE_OAUTH_TOKEN"])
except BaseException:
    print("Not able to authenticate to Eventbrite")

app = Flask(__name__)
sslify = SSLify(app)

# Gracefully handle running locally without app open date infortmation
try:
    app_open_date_string = os.environ["APP_OPEN_DATE"]
    is_extended = os.environ["APP_EXTENDED"].lower() == "true"

    # Gracefully handle running locally w app_open_date formatted incorrectly
    try:
        app_open_date = datetime.datetime.strptime(
            app_open_date_string, "%m/%d/%y %H:%M:%S"
        )
    except BaseException:
        print("Application open date is incorrectly formatted.")
        app_open_date = None
except BaseException:
    print("Not able to retrieve application date information.")
    app_open_date = None


# MVP
app.register_blueprint(application_bp, url_prefix="/application")
app.register_blueprint(course_bp, url_prefix="/course")


# MAIN HANDLERS
@app.route("/")
def render_home_page():
    """
    Renders the home page from jinja2 template
    """
    times = get_time()
    try:
        events = get_events()
        return render_template("home.html", events=events, times=times)
    except BaseException:
        return render_template("home.html", times=times)


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


@app.route("/consulting/")
def render_consulting_page():
    """
    Renders the consulting page from jinja2 template
    """
    return render_template("consulting.html")


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

# @app.route("/openings/ta/")
# def render_ta_page():
#     """
#     Renders the TA page from jinja2 template
#     """
#     return render_template("ta.html")


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
    & utilizes 'render_mentor_page' function
    """
    mentor_timeline = get_mentor_timeline()
    return render_template("mentor.html", mentor=mentor_timeline)


@app.route("/full-time-program/")
def render_ft_program_page():
    """
    Generates time-bound text and application extension variable
    Renders the full-time program page from jinja2 template with relevant times
    """
    times = get_time()
    return render_template("full-time-program.html", times=times)


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


@app.route("/app-form-details")
def app_form_details():
    return render_template("app-form-details.html")


@app.route("/app-form")
def app_form():
    return render_template("app-form.html")


@app.route("/app-additional")
def app_additional():
    return render_template("app-additional.html")


@app.route("/app-household")
def app_household():
    return render_template("app-household.html")


@app.route("/app-long-text")
def app_long_text():
    return render_template("app-long-text.html")


@app.route("/app-questionnaire")
def app_questionnaire():
    return render_template("app-questionnaire.html")


@app.route("/app-reference")
def app_reference():
    return render_template("app-reference.html")


@app.route("/app-form-admin")
def app_form_admin():
    return render_template("app-form-admin.html")


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


def get_time():
    """Returns a dictionary containing app_open (a boolean for current state of
    applications) and text (for application timeline-related button content)"""
    if app_open_date is None:
        app_open = True
        text = "Apply Now!"
    else:
        today = datetime.datetime.today()
        if is_extended:
            app_close_date = app_open_date + datetime.timedelta(days=42)
            date_string = app_close_date.strftime("%B %-d")
            text = """Extended!
            Apply by {date} (12pm PT)!""".format(
                date=date_string
            )
        else:
            app_close_date = app_open_date + datetime.timedelta(days=28)
            date_string = app_close_date.strftime("%B %-d")
            text = "Apply by {date} (12pm PT)!".format(date=date_string)

        app_open = app_open_date <= today <= app_close_date

    return {
        "app_open": app_open,
        "text": text,
    }


def get_mentor_timeline():
    """Returns dynamically calculated mentor timeline dates."""
    if app_open_date is None:
        print("Warning: app_open_date is None. Mentor timeline not generated.")

    else:
        # Utilizing app open date variable from line 38
        # Defining key dates
        app_close_date = app_open_date + datetime.timedelta(weeks=4)
        onboarding_day = app_close_date + datetime.timedelta(weeks=6)
        pre_work_start = onboarding_day + datetime.timedelta(days=1)
        start_day = pre_work_start + datetime.timedelta(weeks=4, days=3)

        # Defining Cohort Type (January H1 or July H2)
        start_month = start_day.strftime("%B")  # extracting month
        cohort_half = "H1" if start_month == "January" else "H2"

        # Defining training and job search periods
        training_end = start_day + datetime.timedelta(weeks=24)
        job_search_end = start_day + datetime.timedelta(weeks=48)

        return {
            "app_open_date": app_open_date.strftime("%B %d, %Y"),
            "app_close_date": app_close_date.strftime("%B %d, %Y"),
            "onboarding_day": onboarding_day.strftime("%B %d, %Y"),
            "pre_work_start": pre_work_start.strftime("%B %d, %Y"),
            "start_day": start_day.strftime("%B %d, %Y"),
            "start_month": start_month,  # January or July
            "year": start_day.year,
            "cohort_half": cohort_half,  # H1 or H2
            "training_start_month": start_month,
            "training_end_month": training_end.strftime("%B"),
            "job_search_start_month": training_end.strftime("%B"),
            "job_search_end_month": job_search_end.strftime("%B"),
        }


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


# ONLINE PAYMENT HANDLING *****************************************************

missing_credentials = []

# Slack credentials
try:
    SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
except BaseException:
    missing_credentials.append("SLACK_WEBHOOK")

# Square credentials
try:
    CONFIG_TYPE = os.environ["ENVIRONMENT"]
except BaseException:
    missing_credentials.append("ENVIRONMENT")
try:
    PAYMENT_FORM_URL = os.environ["PAYMENT_FORM_URL"]
except BaseException:
    missing_credentials.append("PAYMENT_FORM_URL")
try:
    APPLICATION_ID = os.environ["SQUARE_APPLICATION_ID"]
except BaseException:
    missing_credentials.append("SQUARE_APPLICATION_ID")
try:
    LOCATION_ID = os.environ["SQUARE_LOCATION_ID"]
except BaseException:
    missing_credentials.append("SQUARE_LOCATION_ID")
try:
    ACCESS_TOKEN = os.environ["SQUARE_ACCESS_TOKEN"]
except BaseException:
    missing_credentials.append("SQUARE_ACCESS_TOKEN")

if len(missing_credentials) > 0:
    missing_credentials_string = " ".join(missing_credentials)
    print(
        "The following credential(s) are missing: {credentials}".format(
            credentials=missing_credentials_string
        )
    )
else:
    if CONFIG_TYPE == "prod":
        SQUARE_ENVIRONMENT = "production"
    else:
        SQUARE_ENVIRONMENT = "sandbox"

    client = Client(
        access_token=ACCESS_TOKEN,
        environment=SQUARE_ENVIRONMENT,
        user_agent_detail="techtonica_payment",
    )


class Payment(BaseModel):
    token: str
    idempotencyKey: str


# old route - redirects to avoid breaking old links


@app.route("/payment-form")
def render_payment_form():
    """
    Redirects to current job-form route
    """
    return redirect(url_for("render_job_form"))

@app.route("/share-a-job")
def render_job_form():
    """
    Renders the job-form page from jinja2 template
    """
    if len(missing_credentials) > 0:
        return render_template("job-form.html", credentials=False)
    else:
        return render_template(
            "job-form.html",
            APPLICATION_ID=APPLICATION_ID,
            PAYMENT_FORM_URL=PAYMENT_FORM_URL,
            LOCATION_ID=LOCATION_ID,
            ACCOUNT_CURRENCY="USD",
            ACCOUNT_COUNTRY="ACCOUNT_COUNTRY",
            idempotencyKey=str(uuid4()),
            credentials=True,
        )

# Square payment api route
@app.route("/process-payment", methods=["POST"])
def create_payment():
    # Charge the customer's card
    account_currency = "USD"  # TODO: Are you hard-coding this to USD?
    data = request.json
    print(data)

    create_payment_response = client.payments.create_payment(
        body={
            "source_id": data.get("token"),
            "idempotency_key": data.get("idempotencyKey"),
            "amount_money": {
                "amount": 10000,  # $100.00 charge
                "currency": account_currency,
            },
        }
    )

    print("Payment created", create_payment_response)
    if create_payment_response.is_success():
        print("success")
        return create_payment_response.body
    elif create_payment_response.is_error():
        print("error")
        return {"errors": create_payment_response.errors}


# Slack webhook route
@app.route("/send-posting", methods=["POST"])
def send_posting():
    data = request.json
    print(f"Received data: {data}")

    x = requests.post(
        SLACK_WEBHOOK,
        json={
            "text": f"A new job has been posted to Techtonica! Read the details below to see if you're a good fit!  \n\n JOB DETAILS \n Job Title: {data['jobTitle']} \n Company: {data['company']} \n Type: {data['type']} \n Education Requirement: {data['educationReq']} \n Location: {data['location']} \n Referral offered: {data['referral']} \n Salary Range: {data['salaryRange']} \n Description: {data['description']} \n Application Link: {data['applicationLink']} \n \n CONTACT INFO \n Name: {data['firstName']} {data['lastName']}  \n Email: {data['email']}  \n "  # noqa: E501
        },
    )

    print(f"Message sent: {x.text}")
    return jsonify(
        {"message": "Data received successfully", "received_data": data}
    )  # noqa: E501


if __name__ == "__main__":
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
