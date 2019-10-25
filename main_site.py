"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""
import os

from dateutil.parser import parse
from dotenv import find_dotenv, load_dotenv
from eventbrite import Eventbrite
from flask import Flask, redirect, render_template, url_for
from flask_sslify import SSLify

load_dotenv(find_dotenv(usecwd=True))

# We fetch our constants by taking them from environment variables
#   defined in the .env file.
EVENTBRITE_OAUTH_TOKEN = os.environ["EVENTBRITE_OAUTH_TOKEN"]

# Instantiate the Eventbrite API client.
eb = Eventbrite(EVENTBRITE_OAUTH_TOKEN)

app = Flask(__name__)
sslify = SSLify(app)


class Event(object):
    def __init__(self, event_dict):
        self.title = event_dict["name"]["text"]
        self.url = event_dict["url"]
        self.location_title = event_dict["venue"]["name"]
        self.address = event_dict["venue"]["address"][
            "localized_multi_line_address_display"
        ]
        self.date = parse(event_dict["start"]["local"]).strftime(
            "%B %-d, %Y, %-I:%M%p PDT"
        )


# MAIN HANDLERS
@app.route("/")
def render_home_page():
    """
    Renders the home page from jinja2 template
    """

    # Get Eventbrite details
    user = eb.get_user()
    search_params = {"user.id": user["id"], "sort_by": "date", "expand": "venue"}
    try:
        events = eb.event_search(**search_params)
    # A problem was happening on 2019-09-21 wherein Eventbrite was giving back
    # an HTML-based (instead of JSON-enabled) 403 page -- which said, among
    # other things, "The Team is currently working to return you to the service
    # as quickly as possible.".  Hopefully this is exceedingly rare in most
    # cases, but if and when it does happen, we still want to fail gracefully.

    # In theory this will be a ValueError, with a .message value of "No JSON
    # object could be decoded", and we could have a specialized except-handler
    # for that.  However, it seems to me that we want _all_ exceptions to still
    # fail gracefully, so just doing a catch-all:
    except:
        events = { "events": [] }
        pass

    formatted_events = []
    for e in events["events"]:
        formatted_events.append(Event(e))
    return render_template("home.html", events=formatted_events[0:3])

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


@app.route('/openings/tapm/')
def render_tapm_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('tapm.html')


@app.route("/openings/curriculumdev/")
def render_curriculumdev_page():
    """
    Renders the openings page from jinja2 template
    """
    return render_template("curriculumdev.html")


@app.route("/openings/board/")
def render_board_page():
    """
    Renders the openings page from jinja2 template
    """
    return render_template("board.html")


@app.route("/mentor/")
def render_mentor_page():
    """
    Renders the mentor page from jinja2 template
    """
    return render_template("mentor.html")


@app.route("/apprenticeship/")
def render_apprenticeship_page():
    """
    Renders the apprenticeship page from jinja2 template
    """
    return render_template("apprenticeship.html")


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


if __name__ == "__main__":
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
