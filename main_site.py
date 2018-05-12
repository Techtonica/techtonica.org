"""
This is the main Python file that sets up rendering and templating
for Techtonica.org
"""
from flask import Flask, render_template, redirect, url_for
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)


# MAIN HANDLERS
@app.route('/')
def render_home_page():
    '''
    Renders the home page from jinja2 template
    '''
    return render_template('home.html')


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

@app.route('/openings/facilitator/')
def render_facilitator_page():
    '''
    Renders the openings page from jinja2 template
    '''
    return render_template('facilitator.html')

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

if __name__ == '__main__':
    app.debug = False
    # app.run(host='0.0.0.0', port=9999)
