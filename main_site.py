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
from flask import Flask, redirect, render_template, url_for
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


@app.route("/donate/")
def render_donate_page():
    """
    Renders the donate page from jinja2 template
    """
    return render_template("donate.html")


def generate_payment_html():
    html_content = (
        """<!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>Make Payment</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- link to the Web SDK library -->
        <script type="text/javascript" src="""
        + PAYMENT_FORM_URL
        + """></script>

        <script type="application/javascript">
            window.applicationId = '"""
        + APPLICATION_ID
        + """';
            window.locationId = '"""
        + LOCATION_ID
        + """';
            window.currency = '"""
        + ACCOUNT_CURRENCY
        + """';
            window.country = '"""
        + ACCOUNT_COUNTRY
        + """';
            window.idempotencyKey = '"""
        + str(uuid.uuid4())
        + """';
        </script>

        <!-- link to the custom styles for Web SDK -->
        <link rel='stylesheet', href='/static/stylesheets/sq-payment.css' />
        <link rel='stylesheet', href='/static/stylesheets/style.css' />
      </head>

      <body>
        <form class="payment-form" id="fast-checkout">
          <div class="wrapper">
            <div id="apple-pay-button" alt="apple-pay" type="button"></div>
            <div id="google-pay-button" alt="google-pay" type="button"></div>
            <div class="border">
              <span>OR</span>
            </div>

            <div id="ach-wrapper">
              <label for="ach-account-holder-name">Full Name</label>
              <input
                id="ach-account-holder-name"
                type="text"
                placeholder="Jane Doe"
                name="ach-account-holder-name"
                autocomplete="name"
              />
              <span id="ach-message"></span>
              <button id="ach-button" type="button">
                Pay with Bank Account
              </button>
              <div class="border">
                <span>OR</span>
              </div>
            </div>

            <div id="card-container"></div>
            <button id="card-button" type="button">
              Pay with Card
            </button>
            <span id="payment-flow-message">
          </div>
        </form>
        <script type="text/javascript" src="/static/js/sq-ach.js"></script>
        <script type="text/javascript" src="/static/js/sq-apple-pay.js"></script>
        <script type="text/javascript" src="/static/js/sq-google-pay.js"></script>
        <script type="text/javascript" src="/static/js/sq-card-pay.js"></script>
      </body>

      <!-- link to the local Web SDK initialization -->
      <script type="text/javascript" src="/static/js/sq-payment-flow.js"></script>
    </html>
    """
    )
    return HTMLResponse(content=html_content, status_code=200)

class Payment(BaseModel):
    token: str
    idempotencyKey: str

app2 = FastAPI()
app2.mount("/static", StaticFiles(directory="static"), name="static")

@app.route("/donation-form")
def render_donation_form():
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
