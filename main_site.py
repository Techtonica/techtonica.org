"""
This is the main python file that sets up rendering and templating
for Techtonica.com
"""
from flask import Flask, render_template

__author__ = "Harry Staley <staleyh@gmail.com>"
__version__ = "1.0"

app = Flask(__name__)


# MAIN HANDLERS
@app.route('/')
def render_home_page():
    '''
    Renders the home page from jinja2 template
    '''
    return render_template('home.html')


@app.route('/about/')
def render_about_page():
    '''
    Renders the about page from jinja2 template
    '''
    return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=9999)
