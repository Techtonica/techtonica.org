"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""
import os
import sys

import configparser
import pendulum
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, redirect, render_template, url_for, request, jsonify
from flask_sslify import SSLify

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from square.client import Client
from uuid import uuid4

load_dotenv(find_dotenv(usecwd=True))

# (Square) credentials
client = Client(
    access_token='EAAAl_0QhSnq0KtkiiftPFciQnKzncpiOrxnvLC-cYWs7gAkHmlWUvrwh6Y7gNgy',
    #os.environ['SQUARE_ACCESS_TOKEN'],
    environment='sandbox')

result = client.locations.list_locations()

if result.is_success():
    for location in result.body['locations']:
        print(f"{location['id']}: ", end="")
        print(f"{location['name']}, ", end="")
        print(f"{location['address']['address_line_1']}, ", end="")
        print(f"{location['address']['locality']}")

elif result.is_error():
    for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail'])


# To read your secret credentials
config = configparser.ConfigParser()
config.read("config.ini")

# Retrieve developer password
dev_password = config.get("DEFAULT", "dev_password")

# Retrieve credentials based on is_prod
CONFIG_TYPE = config.get("DEFAULT", "environment").upper()
PAYMENT_FORM_URL = (
    "https://web.squarecdn.com/v1/square.js"
    if CONFIG_TYPE == "PRODUCTION"
    else "https://sandbox.web.squarecdn.com/v1/square.js"
)
APPLICATION_ID = config.get(CONFIG_TYPE, "square_application_id")
LOCATION_ID = config.get(CONFIG_TYPE, "square_location_id")
ACCESS_TOKEN = config.get(CONFIG_TYPE, "square_access_token")

location = client.locations.retrieve_location(location_id=LOCATION_ID).body["location"]
ACCOUNT_CURRENCY = location["currency"]
ACCOUNT_COUNTRY = location["country"]


# Gracefully handle running locally without eventbrite token
try:
    eventbrite = Eventbrite(os.environ["EVENTBRITE_OAUTH_TOKEN"])
except BaseException:
    print("Not able to authenticate to Eventbrite")

app = Flask(__name__)
sslify = SSLify(app)

# DEVELOPER PASSWORD
@app.route("/check-dev-password", methods=['GET','POST'])
def check_dev_password():
    """
    Checks for developer password before rendering the requested page,
    returns error if password is incorrect or there is no redirect url
    """
    print("Dev access requested")
    dev_redirect = request.form.get('devredirect')
    nondev_redirect = request.form.get('nondevredirect')
    input_password = request.form.get('devpwd')
    print("Requested route: " + str(dev_redirect))

    if input_password is not None and input_password == dev_password:
        print("dev password validated!")
        if dev_redirect is not None:
            return redirect(url_for(dev_redirect, pwd=input_password))
        elif nondev_redirect is not None:
            return redirect(url_for(nondev_redirect))
        else:
            return "Error: No redirect found", 404
    else:
        print("ERROR: Incorrect dev password")
        return "Error: Access denied", 400


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


@app.route("/openings/tapm/")
def render_tapm_page():
    """
    Renders the TAPM page from jinja2 template
    """
    return render_template("tapm.html")

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

@app.route("/openings/curriculumdev/")
def render_curriculumdev_page():
    """
    Renders the curriculum dev page from jinja2 template
    """
    return render_template("curriculumdev.html")


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


@app.route("/donate/", methods=['GET', 'POST'])
def render_donate_page():
    """
    Renders the donate page from jinja2 template
    """
    return render_template("donate.html")


class Payment(BaseModel):
    token: str
    idempotencyKey: str

app2 = FastAPI()
app2.mount("/static", StaticFiles(directory="static"), name="static")

@app.route("/donation-form")
def render_donation_form():
    if request.args['pwd'] != dev_password:
        return "Access denied", 400
    else:
        context = {
            PAYMENT_FORM_URL: PAYMENT_FORM_URL,
            APPLICATION_ID: APPLICATION_ID,
            LOCATION_ID: LOCATION_ID,
            ACCOUNT_CURRENCY: ACCOUNT_CURRENCY,
            ACCOUNT_COUNTRY: ACCOUNT_COUNTRY
        }
        return render_template("donation-form.html", PAYMENT_FORM_URL= PAYMENT_FORM_URL,
            APPLICATION_ID= APPLICATION_ID,
            LOCATION_ID= LOCATION_ID,
            ACCOUNT_CURRENCY= ACCOUNT_CURRENCY,
            ACCOUNT_COUNTRY= ACCOUNT_COUNTRY,
            idempotencyKey= str( uuid4() ))

# (Square) payment route
@app2.route("/process-payment", methods=['POST'])
def create_payment(payment: Payment):
    logging.info("Creating payment")
    # Charge the customer's card
    create_payment_response = client.payments.create_payment(
        body={
            "source_id": payment.token,
            "idempotency_key": str(uuid.uuid4()),
            "amount_money": {
                "amount": 100,  # $1.00 charge
                "currency": ACCOUNT_CURRENCY,
            },
        }
    )

    logging.info("Payment created")
    if create_payment_response.is_success():
        return create_payment_response.body
    elif create_payment_response.is_error():
        return create_payment_response

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


if __name__ == "__main__":
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
