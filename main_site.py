"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""

import configparser
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

from dates import generate_application_timeline
from db_connection import get_db_connection

load_dotenv(find_dotenv(usecwd=True))

# Gracefully handle running locally without eventbrite token
try:
    eventbrite = Eventbrite(os.environ["EVENTBRITE_OAUTH_TOKEN"])
except Exception:
    print("Not able to authenticate to Eventbrite.")

app = Flask(__name__)
sslify = SSLify(app)

# Connect to Database
engine = get_db_connection()


# MVP
app.register_blueprint(application_bp, url_prefix="/application")
app.register_blueprint(course_bp, url_prefix="/course")


# MAIN HANDLERS
@app.route("/")
def render_home_page():
    """
    Renders the home page from jinja2 template
    """
    timeline = generate_application_timeline()
    try:
        events = get_events()
        return render_template("home.html", events=events, timeline=timeline)
    except Exception:
        return render_template("home.html", timeline=timeline)


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
    timeline = generate_application_timeline()
    return render_template("mentor.html", timeline=timeline)


@app.route("/full-time-program/")
def render_ft_program_page():
    """
    Generates time-bound text and application extension variable
    Renders the full-time program page from jinja2 template with relevant times
    """
    timeline = generate_application_timeline()
    return render_template("full-time-program.html", timeline=timeline)


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
    PAYMENT_FORM_URL = "https://sandbox.web.squarecdn.com/v1/square.js"
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
    return render_template(
        "job-form.html",
        APPLICATION_ID=APPLICATION_ID,
        PAYMENT_FORM_URL=PAYMENT_FORM_URL,
        LOCATION_ID=LOCATION_ID,
        ACCOUNT_CURRENCY="USD",
        ACCOUNT_COUNTRY="ACCOUNT_COUNTRY",
        idempotencyKey=str(uuid4()),
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
