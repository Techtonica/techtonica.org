"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""
import os

from flask import Flask, render_template, redirect, url_for, request
from flask_sslify import SSLify
#import pusher

# We fetch our constants by taking them from environment variables
#   defined in the .env file.
# EVENTBRITE_EVENT_ID = os.environ['EVENTBRITE_EVENT_ID']
# EVENTBRITE_OAUTH_TOKEN= os.environ['EVENTBRITE_OAUTH_TOKEN']
# PUSHER_APP_ID = os.environ['PUSHER_APP_ID']
# PUSHER_KEY = os.environ['PUSHER_KEY']
# PUSHER_SECRET = os.environ['PUSHER_SECRET']

# Instantiate the Eventbrite API client.
# eventbrite = eventbrite.Eventbrite(EVENTBRITE_OAUTH_TOKEN)

# Instantiate the pusher object. This library is used to push actions
#   to the browser when they occur.

# p = pusher.Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)

app = Flask(__name__)
sslify = SSLify(app)


# MAIN HANDLERS
@app.route('/')
def render_home_page():
    # # Get Eventbrite details
    # event = eventbrite.get_event(EVENTBRITE_EVENT_ID)

    # # Get the attendee list
    # attendees = eventbrite.get_event_attendees(EVENTBRITE_EVENT_ID)

    # # Reverse so latest to sign up is at the top
    # attendees['attendees'].reverse()


    '''
    Renders the home page from jinja2 template
    '''
    return render_template(
        'home.html',
        # settings={'PUSHER_KEY': PUSHER_KEY},
        # event=event,
        # attendees=attendees
    )


@app.route('/team/')
def render_team_page():
    '''
    Renders the team page from jinja2 template
    '''
    return render_template('team.html')


@app.route('/careers/')
def render_careers_page():
    '''
    Renders the careers page from jinja2 template
    '''
    return redirect(url_for('render_openings_page'))


@app.route('/conduct/')
def render_conduct_page():
    '''
    Renders the conduct page from jinja2 template
    '''
    return render_template('conduct.html')


@app.route('/thankyou/')
def render_thankyou_page():
    '''
    Renders the newsletter signup's thank you page from jinja2 template.
    '''
    return render_template('thankyou.html')


@app.route('/sponsor/')
def render_sponsor_page():
    '''
    Renders the sponsor page from jinja2 template
    '''
    return render_template('sponsor.html')


@app.route('/faqs/')
def render_faqs_page():
    '''
    Renders the FAQs page from jinja2 template
    '''
    return render_template('faqs.html')


@app.route('/openings/')
def render_openings_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('openings.html')

@app.route('/openings/tapm/')
def render_tapm_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('tapm.html')

@app.route('/openings/curriculumdev/')
def render_curriculumdev_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('curriculumdev.html')

@app.route('/openings/businessdev/')
def render_businessdev_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('businessdev.html')

@app.route('/openings/board/')
def render_board_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('board.html')

@app.route('/mentor/')
def render_mentor_page():
    '''
    Renders the mentor page from jinja2 template
    '''
    return render_template('mentor.html')

@app.route('/apprenticeship/')
def render_apprenticeship_page():
    '''
    Renders the apprenticeship page from jinja2 template
    '''
    return render_template('apprenticeship.html')

@app.route('/donate/')
def render_donate_page():
    '''
    Renders the donate page from jinja2 template
    '''
    return render_template('donate.html')

@app.route('/volunteer/')
def render_volunteer_page():
    '''
    Renders the volunteer page from jinja2 template
    '''
    return render_template('volunteer.html')

# @app.route('/webhook/', methods=['POST'])
# def webhook():
#     # Use the API client to convert from a webhook to an API object (a Python dict with some extra methods).
#     api_object = eventbrite.webhook_to_object(request)

#     # Use pusher to add content to to the HTML page.
#     p.trigger(u'webhooks', u'Attendee', api_object)
#     return ""

if __name__ == '__main__':
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
