"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""

import configparser
import os
import sys
import logging
from uuid import uuid4
import hmac
import hashlib
import time
import json
import pendulum
import requests
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
from flask_sslify import SSLify
from pydantic import BaseModel
from square.client import Client

from dates import generate_application_timeline
from db_connection import get_db_connection

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

# Connect to Database
engine = get_db_connection()

# Create a temporary storage for pending job postings
pending_job_postings = {}


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

# Square credentials
CONFIG_TYPE = config.get("default", "environment")
if CONFIG_TYPE == "production":
    PAYMENT_FORM_URL = "https://web.squarecdn.com/v1/square.js"
else:
    PAYMENT_FORM_URL = "https://sandbox.web.squarecdn.com/v1/square.js"

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
    try:
        missing_credentials = []
        if not APPLICATION_ID or not LOCATION_ID or not ACCESS_TOKEN:
            missing_credentials.append("Square credentials")
        
        if len(missing_credentials) > 0:
            return render_template("job-form.html", credentials=False)
        else:
            return render_template(
                "job-form.html",
                APPLICATION_ID=APPLICATION_ID,
                PAYMENT_FORM_URL=PAYMENT_FORM_URL,
                LOCATION_ID=LOCATION_ID,
                ACCOUNT_CURRENCY="USD",
                ACCOUNT_COUNTRY="US",
                idempotencyKey=str(uuid4()),
                credentials=True,
            )
    except Exception as e:
        logger.error(f"Error rendering job form: {e}")
        return render_template("job-form.html", credentials=False)


# Square payment api route
@app.route("/process-payment", methods=["POST"])
def create_payment():
    # Charge the customer's card
    account_currency = "USD"
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


# JOB POSTING APPROVAL WORKFLOW *****************************************************

@app.route("/process-job-posting", methods=["POST"])
def process_job_posting():
    """
    Processes a new job posting and sends it to staff for approval
    """
    data = request.json
    print(f"Received job posting data: {data}")
    
    # Generate a unique ID for this job posting
    posting_id = str(uuid4())
    
    # Store the job posting with its ID
    pending_job_postings[posting_id] = data
    
    # Send to staff channel for approval
    try:
        send_to_staff_channel(data, posting_id)
        return jsonify({
            "success": True,
            "message": "Job posting sent for staff approval",
            "postingId": posting_id
        })
    except Exception as e:
        print(f"Error sending job posting to staff channel: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to process job posting"
        }), 500


@app.route("/approve-job-post", methods=["GET"])
def approve_job_post():
    """
    Approves a job posting and sends it to graduates
    """
    posting_id = request.args.get('id')
    
    if not posting_id:
        return jsonify({
            "success": False,
            "error": "Missing posting ID"
        }), 400
    
    # Get the job posting data
    job_data = pending_job_postings.get(posting_id)
    
    if not job_data:
        return jsonify({
            "success": False,
            "error": "Job posting not found"
        }), 404
    
    # Send to graduates channel
    try:
        send_to_graduates_channel(job_data)
        
        # Remove from pending
        del pending_job_postings[posting_id]
        
        # Return a simple HTML response
        return """
        <html>
            <head>
                <title>Job Posting Approved</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                    .success { color: green; }
                </style>
            </head>
            <body>
                <h1 class="success">Job Posting Approved</h1>
                <p>The job posting has been approved and sent to the graduates channel.</p>
                <p>You can close this window now.</p>
            </body>
        </html>
        """
    except Exception as e:
        print(f"Error approving job posting: {e}")
        return jsonify({
            "success": False,
            "error": "Failed to approve job posting"
        }), 500


@app.route("/reject-job-post", methods=["GET"])
def reject_job_post():
    """
    Rejects a job posting
    """
    posting_id = request.args.get('id')
    
    if not posting_id:
        return jsonify({
            "success": False,
            "error": "Missing posting ID"
        }), 400
    
    # Check if the job posting exists
    if posting_id not in pending_job_postings:
        return jsonify({
            "success": False,
            "error": "Job posting not found"
        }), 404
    
    # Remove from pending
    del pending_job_postings[posting_id]
    
    # Return a simple HTML response
    return """
    <html>
        <head>
            <title>Job Posting Rejected</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .rejected { color: red; }
            </style>
        </head>
        <body>
            <h1 class="rejected">Job Posting Rejected</h1>
            <p>The job posting has been rejected and will not be sent to the graduates channel.</p>
            <p>You can close this window now.</p>
        </body>
    </html>
    """


@app.route("/verify-slack-request", methods=["POST"])
def verify_slack_request():
    """
    Verifies that a request is coming from Slack
    """
    # Get the Slack signing secret from environment variables
    slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
    
    if not slack_signing_secret:
        print("SLACK_SIGNING_SECRET is not set")
        return jsonify({"error": "Server configuration error"}), 500
    
    # Get the Slack signature and timestamp from headers
    slack_signature = request.headers.get("X-Slack-Signature")
    slack_timestamp = request.headers.get("X-Slack-Request-Timestamp")
    
    if not slack_signature or not slack_timestamp:
        return jsonify({"error": "Missing Slack signature headers"}), 400
    
    # Check if the request is older than 5 minutes
    current_time = int(time.time())
    if abs(current_time - int(slack_timestamp)) > 300:
        return jsonify({"error": "Request timestamp is too old"}), 400
    
    # Get the request body as text
    request_body = request.get_data().decode("utf-8")
    
    # Create the signature base string
    base_string = f"v0:{slack_timestamp}:{request_body}"
    
    # Create the signature to compare with the one from Slack
    my_signature = "v0=" + hmac.new(
        slack_signing_secret.encode("utf-8"),
        base_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    # Check if the signatures match
    if hmac.compare_digest(my_signature, slack_signature):
        # Signatures match, request is from Slack
        return jsonify({"success": True})
    else:
        # Signatures don't match
        return jsonify({"error": "Invalid signature"}), 401


def send_to_staff_channel(job_data, posting_id):
    """
    Sends a job posting to the staff channel for approval
    """
    staff_webhook = os.environ.get("SLACK_STAFF_WEBHOOK")
    
    if not staff_webhook:
        raise Exception("SLACK_STAFF_WEBHOOK environment variable is not set")
    
    # Create approval buttons with the posting ID
    base_url = request.host_url.rstrip('/')
    approve_url = f"{base_url}/approve-job-post?id={posting_id}"
    reject_url = f"{base_url}/reject-job-post?id={posting_id}"
    
    message = {
        "text": "A new job posting requires approval",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Job Posting Requires Approval",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Job Title:* {job_data.get('jobTitle')}\n*Company:* {job_data.get('company')}\n*Type:* {job_data.get('type', 'Not specified')}\n*Education Requirement:* {job_data.get('educationReq', 'Not specified')}\n*Location:* {job_data.get('location')}\n*Referral offered:* {job_data.get('referral')}\n*Salary Range:* {job_data.get('salaryRange', 'Not specified')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{job_data.get('description', 'No description provided')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Application Link:*\n{job_data.get('applicationLink', 'No link provided')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Contact:*\n{job_data.get('firstName')} {job_data.get('lastName')} ({job_data.get('email')})"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Approve",
                            "emoji": True
                        },
                        "style": "primary",
                        "url": approve_url
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject",
                            "emoji": True
                        },
                        "style": "danger",
                        "url": reject_url
                    }
                ]
            }
        ]
    }
    
    response = requests.post(
        staff_webhook,
        json=message
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to send to staff channel: {response.text}")
    
    return response


def send_to_graduates_channel(job_data):
    """
    Sends an approved job posting to the graduates channel
    """
    graduates_webhook = os.environ.get("SLACK_GRADUATES_WEBHOOK")
    
    if not graduates_webhook:
        raise Exception("SLACK_GRADUATES_WEBHOOK environment variable is not set")
    
    message = {
        "text": "A new job has been posted to Techtonica! Read the details below to see if you're a good fit!",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Job Opportunity",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Job Title:* {job_data.get('jobTitle')}\n*Company:* {job_data.get('company')}\n*Type:* {job_data.get('type', 'Not specified')}\n*Education Requirement:* {job_data.get('educationReq', 'Not specified')}\n*Location:* {job_data.get('location')}\n*Referral offered:* {job_data.get('referral')}\n*Salary Range:* {job_data.get('salaryRange', 'Not specified')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{job_data.get('description', 'No description provided')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Application Link:*\n{job_data.get('applicationLink', 'No link provided')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Contact:*\n{job_data.get('firstName')} {job_data.get('lastName')} ({job_data.get('email')})"
                }
            }
        ]
    }
    
    response = requests.post(
        graduates_webhook,
        json=message
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to send to graduates channel: {response.text}")
    
    return response


if __name__ == "__main__":
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
