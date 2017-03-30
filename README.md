# Techtonica

This repo is for [the Techtonica website](http://techtonica.org), which is
currently hosted on Bluehost.

### Who

The main audience of the website is made up of (potential) volunteers and
sponsors. (Students will be contacted via local organizations.)

### What

We need to effectively communicate that Techtonica and its students are worth
supporting.

### How

There should be a good understanding of how the program works with vetting,
training, mentoring, and hiring.


## Getting Started

This app uses Python 2.7; please stick to this version.

### Running Locally

It is recommended you use a virtual environment tool to keep dependencies
required by different projects separate. [Learn more about Python virtual
environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Install the project dependencies. In the project root run:

```sh
pip install -r requirements.txt
```

Start the application's server:

```sh
FLASK_APP=main_site.py flask run
```

Browse to <http://localhost:5000>.


## Deployment to DreamHost

## Initial Setup

Follow the instructions in the [Setting up and deploying Python Flask to
Dreamhost](https://mattcarrier.com/flask-dreamhost-setup/) blog post.

## Updating the Site

1.  Log in via SSH using your SSH key.
2.  Change directory to the appropriate domain, either `techtonica.org` or
    `staging.techtonica.org`.
3.  Change to the source directory:

    ```sh
    cd techtonica
    ```
4.  Use the usual `git` commands to get the latest code or check out another
    branch.
5.  "Restart" the passenger process:

    ```sh
    cd .. && touch tmp/restart.txt
    ```
