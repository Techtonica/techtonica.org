"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""

import logging
import os
import sys
from uuid import uuid4

import pendulum
import requests
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sslify import SSLify
from pydantic import BaseModel
from square.client import Client

from dates import generate_application_timeline
from db_connection import get_db_connection
from drive_service_Oauth import get_or_create_user_folder, register_drive_routes, upload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv(usecwd=True))

# Gracefully handle running locally without eventbrite token
try:
    eventbrite = Eventbrite(os.environ["EVENTBRITE_OAUTH_TOKEN"])
except Exception:
    print("Not able to authenticate to Eventbrite.")

app = Flask(__name__)
sslify = SSLify(app)

# Connect to the drive
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")
register_drive_routes(app)


# Connect to Database
engine = get_db_connection()


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


# @app.route("/full-time-program/")
# def render_ft_program_page():
#     """
#     Generates time-bound text and application extension variable
#     Renders the full-time program page from jinja2 template with relevant
#     times
#     """
#     timeline = generate_application_timeline()
#     return render_template("full-time-program.html", timeline=timeline)


@app.route("/software-engineering-program/")
def render_swe_program_page():
    """
    Renders the part time software engineering page from jinja2 template
    """
    return render_template("software-engineering-program.html")


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
    return render_template("app/form-details.html")


@app.route("/app-form", methods=["GET", "POST"])
def app_form():
    if request.method == "POST":
        email = request.form.get("email")

        # save to session for later create folder
        session["user_email"] = email

        return redirect(url_for("app_household"))

    return render_template("app/form.html")


@app.route("/app-additional", methods=["GET", "POST"])
def app_additional():
    if request.method == "POST":
        if "credentials" not in session:
            return redirect(url_for("login"))
        credentials = session["credentials"]
        user_email = session.get("user_email")

        if not user_email:
            return "User email not found in session", 400

        # get or create folder
        folder_id = get_or_create_user_folder(credentials, user_email)

        # get two files
        typing_file = request.files.get("typing-test-screenshot")
        fcc_file = request.files.get("FCC-screenshot")

        if typing_file and typing_file.filename:
            typing_new_name = f"TypingTest_{user_email}_{typing_file.filename}"
            upload(credentials, folder_id, typing_file, typing_new_name)

        if fcc_file and fcc_file.filename:
            fcc_new_name = f"FCC_{user_email}_{fcc_file.filename}"
            upload(credentials, folder_id, fcc_file, fcc_new_name)

        return redirect(url_for("render_home_page"))

    return render_template("app/additional.html")


@app.route("/app-household", methods=["GET", "POST"])
def app_household():
    if request.method == "POST":
        action = request.form.get("action", "next")

        if "credentials" not in session:
            return redirect(url_for("login"))
        credentials = session["credentials"]
        user_email = session.get("user_email")

        if not user_email:
            return "User email not found in session", 400

        # get or create folder
        folder_id = get_or_create_user_folder(credentials, user_email)

        # get two files
        income_files = request.files.getlist("income-verification-docs")
        networth_files = request.files.getlist("net-worth-docs")

        for idx, file in enumerate(income_files):
            if file and file.filename:
                new_name = f"Income_{user_email}_{idx}_{file.filename}"
                upload(credentials, folder_id, file, new_name)

        for idx, file in enumerate(networth_files):
            if file and file.filename:
                new_name = f"NetWorth_{user_email}_{idx}_{file.filename}"
                upload(credentials, folder_id, file, new_name)

        if action == "save":
            return redirect(url_for("render_home_page"))

        return redirect(url_for("app_long_text"))

    return render_template("app/household.html")


@app.route("/app-long-text")
def app_long_text():
    return render_template("app/long-text.html")


@app.route("/app-questionnaire")
def app_questionnaire():
    return render_template("app/questionnaire.html")


@app.route("/app-reference")
def app_reference():
    return render_template("app/reference.html")


@app.route("/app-form-admin")
def app_form_admin():
    return render_template("app/form-admin.html")


@app.route("/admin/dashboard")
def render_admin_dashboard_page():
    """
    Renders the admin dashboard page from jinja2 template
    """
    return render_template("admin_dashboard.html")


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

missing_credentials = []

# Slack credentials
try:
    SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK"]
except KeyError:
    missing_credentials.append("SLACK_WEBHOOK")

# Square credentials
try:
    CONFIG_TYPE = os.environ["ENVIRONMENT"]
except KeyError:
    missing_credentials.append("ENVIRONMENT")
try:
    PAYMENT_FORM_URL = os.environ["PAYMENT_FORM_URL"]
except KeyError:
    missing_credentials.append("PAYMENT_FORM_URL")
try:
    APPLICATION_ID = os.environ["SQUARE_APPLICATION_ID"]
except KeyError:
    missing_credentials.append("SQUARE_APPLICATION_ID")
try:
    LOCATION_ID = os.environ["SQUARE_LOCATION_ID"]
except KeyError:
    missing_credentials.append("SQUARE_LOCATION_ID")
try:
    ACCESS_TOKEN = os.environ["SQUARE_ACCESS_TOKEN"]
except KeyError:
    missing_credentials.append("SQUARE_ACCESS_TOKEN")

if len(missing_credentials) > 0:
    missing_credentials_string = " ".join(missing_credentials)
    logger.warning(
        "The following credential(s) are missing: {credentials}".format(
            credentials=missing_credentials_string
        )
    )
else:
    if CONFIG_TYPE.lower() == "prod":
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
            "text": f"A new job has been posted to Techtonica! "
            f"Read the details below to see if you're a good fit!"
            f"\n\n JOB DETAILS \n Job Title: {data['jobTitle']} "
            f"\n Company: {data['company']} \n Type: {data['type']} "
            f"\n Education Requirement: {data['educationReq']} "
            f"\n Location: {data['location']} "
            f"\n Referral offered: {data['referral']} "
            f"\n Salary Range: {data['salaryRange']} "
            f"\n Description: {data['description']} "
            f"\n Application Link: {data['applicationLink']} "
            f"\n \n CONTACT INFO "
            f"\n Name: {data['firstName']} {data['lastName']} "
            f"\n Email: {data['email']}  \n "
        },
    )

    print(f"Message sent: {x.text}")
    return jsonify(
        {"message": "Data received successfully", "received_data": data}
    )


@app.route("/upload-household-files", methods=["POST"])
def upload_household_files():
    credentials = session["credentials"]
    user_email = request.form.get("user_email")

    folder_id = get_or_create_user_folder(credentials, user_email)

    income_files = request.files.getlist("income-verification-docs")
    networth_files = request.files.getlist("net-worth-docs")

    for idx, file in enumerate(income_files):
        if file and file.filename:
            upload(
                credentials,
                folder_id,
                file,
                f"Income_{user_email}_{idx}_{file.filename}",
            )

    for idx, file in enumerate(networth_files):
        if file and file.filename:
            upload(
                credentials,
                folder_id,
                file,
                f"NetWorth_{user_email}_{idx}_{file.filename}",
            )

    return jsonify({"success": True})


@app.route("/upload-additional-files", methods=["POST"])
def upload_additional_files():
    if "credentials" not in session:
        return (
            jsonify(
                {"success": False, "error": "Missing Google Drive credentials"}
            ),
            401,
        )

    credentials = session["credentials"]
    user_email = request.form.get("user_email")

    if not user_email:
        return (
            jsonify({"success": False, "error": "User email not found"}),
            400,
        )

    folder_id = get_or_create_user_folder(credentials, user_email)

    typing_file = request.files.get("typing-test-screenshot")
    fcc_file = request.files.get("FCC-screenshot")

    if typing_file and typing_file.filename:
        typing_new_name = f"TypingTest_{user_email}_{typing_file.filename}"
        upload(credentials, folder_id, typing_file, typing_new_name)

    if fcc_file and fcc_file.filename:
        fcc_new_name = f"FCC_{user_email}_{fcc_file.filename}"
        upload(credentials, folder_id, fcc_file, fcc_new_name)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
