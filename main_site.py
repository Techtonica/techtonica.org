"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""

import os
import sys
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

# Load environment variables
load_dotenv()

# Get environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "sandbox")
IS_PRODUCTION = ENVIRONMENT == "production"

# Square credentials
PAYMENT_FORM_URL = "https://web.squarecdn.com/v1/square.js" if IS_PRODUCTION else "https://sandbox.web.squarecdn.com/v1/square.js"
APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID")
LOCATION_ID = os.getenv("SQUARE_LOCATION_ID")
ACCESS_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")

# Slack credentials
SLACK_STAFF_WEBHOOK = os.getenv("SLACK_STAFF_WEBHOOK")
SLACK_GRADUATES_WEBHOOK = os.getenv("SLACK_GRADUATES_WEBHOOK")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

# Initialize Square client
client = Client(
    access_token=ACCESS_TOKEN,
    environment=ENVIRONMENT,
    user_agent_detail="techtonica_payment",
)

# Create a temporary storage for pending job postings
pending_job_postings = {}

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
        ACCOUNT_COUNTRY="US",
        idempotencyKey=str(uuid4()),
    )

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


# Slack webhook route
@app.route("/send-posting", methods=["POST"])
def send_posting():
    data = request.json
    print(f"Received data: {data}")
    
    # Generate a unique ID for this job posting
    posting_id = str(uuid4())
    
    # Store the job posting data for later approval
    pending_job_postings[posting_id] = data
    
    # Create the job posting message
    job_details = (
        f"*A new job posting requires approval:*\n\n"
        f"*JOB DETAILS*\n"
        f"*Job Title:* {data['jobTitle']}\n"
        f"*Company:* {data['company']}\n"
        f"*Type:* {data['type']}\n"
        f"*Education Requirement:* {data['educationReq']}\n"
        f"*Location:* {data['location']}\n"
        f"*Referral offered:* {data['referral']}\n"
        f"*Salary Range:* {data['salaryRange']}\n"
        f"*Description:* {data['description']}\n"
        f"*Application Link:* {data['applicationLink']}\n\n"
        f"*CONTACT INFO*\n"
        f"*Name:* {data['firstName']} {data['lastName']}\n"
        f"*Email:* {data['email']}\n"
    )
    
    # Create interactive message with approval buttons for staff channel
    staff_message = {
        "text": "New job posting requires approval",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": job_details
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
                        "value": posting_id,
                        "action_id": "approve_job"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject",
                            "emoji": True
                        },
                        "style": "danger",
                        "value": posting_id,
                        "action_id": "reject_job"
                    }
                ]
            }
        ]
    }
    
    # Send to staff channel for approval
    response = requests.post(SLACK_STAFF_WEBHOOK, json=staff_message)
    
    if response.status_code != 200:
        print(f"Error sending to staff channel: {response.text}")
        return jsonify({"error": "Failed to send job posting for approval"}), 500
    
    print(f"Job posting sent to staff for approval: {posting_id}")
    return jsonify({"message": "Job posting sent for approval", "posting_id": posting_id})


# Handle Slack interactive messages (approval/rejection)
@app.route("/slack/actions", methods=["POST"])
def handle_slack_actions():
    # Verify the request is from Slack
    if not verify_slack_request(request):
        abort(403)
    
    # Parse the payload
    payload = json.loads(request.form.get("payload", "{}"))
    action = payload.get("actions", [{}])[0]
    action_id = action.get("action_id")
    posting_id = action.get("value")
    
    # Get the job posting data
    job_data = pending_job_postings.get(posting_id)
    if not job_data:
        return jsonify({"text": "Error: Job posting not found"})
    
    user = payload.get("user", {}).get("name", "A staff member")
    
    if action_id == "approve_job":
        # Post to graduates channel
        graduate_message = {
            "text": f"A new job has been posted to Techtonica! Read the details below to see if you're a good fit!  \n\n JOB DETAILS \n Job Title: {job_data['jobTitle']} \n Company: {job_data['company']} \n Type: {job_data['type']} \n Education Requirement: {job_data['educationReq']} \n Location: {job_data['location']} \n Referral offered: {job_data['referral']} \n Salary Range: {job_data['salaryRange']} \n Description: {job_data['description']} \n Application Link: {job_data['applicationLink']} \n \n CONTACT INFO \n Name: {job_data['firstName']} {job_data['lastName']}  \n Email: {job_data['email']}  \n "
        }
        
        response = requests.post(SLACK_GRADUATES_WEBHOOK, json=graduate_message)
        
        if response.status_code != 200:
            return jsonify({"text": f"Error posting to graduates channel: {response.text}"})
        
        # Clean up the pending job posting
        del pending_job_postings[posting_id]
        
        return jsonify({
            "text": f"✅ Job posting approved by {user} and shared with graduates!"
        })
    
    elif action_id == "reject_job":
        # Clean up the pending job posting
        del pending_job_postings[posting_id]
        
        return jsonify({
            "text": f"❌ Job posting rejected by {user} and will not be shared."
        })
    
    return jsonify({"text": "Unknown action"})


# Function to verify Slack requests
def verify_slack_request(request):
    # Skip verification in development
    if app.debug:
        return True
        
    # Get the signature from the request headers
    slack_signature = request.headers.get("X-Slack-Signature", "")
    slack_request_timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    
    # Check if the timestamp is too old (prevent replay attacks)
    if abs(time.time() - int(slack_request_timestamp)) > 60 * 5:
        return False
    
    # Create the signature base string
    req_body = request.get_data().decode()
    base_string = f"v0:{slack_request_timestamp}:{req_body}"
    
    # Create the signature to compare
    my_signature = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        base_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return hmac.compare_digest(my_signature, slack_signature)

if __name__ == "__main__":
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
