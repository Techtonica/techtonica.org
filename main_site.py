"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""
import os
import sys

import pendulum
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, redirect, render_template, url_for
from flask_sslify import SSLify

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


@app.route("/openings/stem/")
def render_stem_page():
    """
    Renders the STEM page from jinja2 template
    """
    return render_template("stem.html")


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
