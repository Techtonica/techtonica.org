# Techtonica
This repo is for [the Techtonica website](http://techtonica.org), which is currently hosted on Bluehost.

### Who
The main audience of the website is made up of (potential) volunteers and sponsors. (Students will be contacted via local organizations.)

### What
We need to effectively communicate that Techtonica and its students are worth supporting.

### How
There should be a good understanding of how the program works with vetting, training, mentoring, and hiring.

## Getting Started
----------------------

This app uses Python 2.7; please stick to this version.

#### Running Locally

It is recommended you use a Virtual Environment tool to keep dependencies required by different projects separate. Learn more about Virtual Environments and Python [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Install the project dependencies. In the project root run:

```
$ pip install -r requirements.txt
```

Start the application's server:

```
$ FLASK_APP=main_site.py flask run
```

Browse to `localhost:5000`



## DEPLOYMENT / UPDATE NOTES
-----------------------------

8-25-2016 19:00 CST

Installed Python 2.7.12

Submitted a ticket to Python so that the symlink would would work correctly when installed from source.

Installed Virtualenv

Installed Flask

Installed Pip

Installed Flup

Tested the site on techtonica.org/test/ for basic functionality.

Article used to get through the BlueHost wierdness linked below:    
[Flask on BlueHost](http://willhaley.com/blog/flask-on-bluehost/)

8-26-016 10:30 CST

## UPDATING THE SITE
------------------------

Log in via SSH using your SSH key

Navigate to your public html folder using: cd public_html

Submit pull request from github using: git pull
