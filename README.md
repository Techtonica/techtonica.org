# Techtonica

This repo is for [the Techtonica website](http://techtonica.org), which is
currently hosted on DreamHost.

- [Who](#who)
- [What](#what)
- [How](#how)
- [Getting Started](#getting-started)
  - [Set Up Virtual Environment](#set-up-virtual-environment)
  - [Install pip Version 23](#install-pip-version-23)
  - [Install and Upgrade pip-tools](#install-and-upgrade-pip-tools)
  - [Install Pre-Commit Hooks](#install-pre-commit-hooks)
  - [Install Requirements](#install-requirements)
  - [Create Config.ini File](#create-configini-file)
  - [Running Locally](#running-locally)
  - [Using Docker to Run Locally](#using-docker-to-run-locally)
  - [CSS / SCSS](#css--scss)
  - [Square Testing](#square-testing)
  - [Updating Demographics Chart](#updating-the-demographics-chart-for-the-apply-section)
  - [Updating Dependencies](#updating-dependencies)
- [Deployment to DreamHost](#deployment-to-dreamhost)
  - [Initial Setup](#initial-setup)
  - [Updating the Site](#updating-the-site)

## Who

The audience of the website is made up of (potential) volunteers, sponsors, and program participants.

## What

We need to effectively communicate that Techtonica and its participants are worth supporting and share details of the program for potential applicants and volunteers.

## How

There should be a good understanding of how the program works with vetting, training, mentoring, and placements.

[Detailed instructions on how to update the website](https://docs.google.com/document/d/1oL3BaemFfUD7DfoFzhTSwcX4lPxYbWN3Dy9oZFfGP0Y/edit)

## Getting Started

You need Python version 3.8.10 and pip version 23 in order to properly update dependencies and replicate the production server environment locally.

Using Python 3.8.10 and pip 23 helps ensure compatibility and consistency between your local development environment and the server environment. This minimizes potential issues during deployment by keeping dependencies in sync with the versions expected by the servers and eliminates discrepancies caused by different versions, ensuring that code runs the same way on every developer's machine.

### Set Up Virtual Environment

It is recommended you use a virtual environment to keep dependencies
required by different projects separate. [Learn more about Python virtual
environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Set up virtual environment with Python 3.8.10 and Pip 23 using [pyenv](https://github.com/pyenv/pyenv) and [venv](https://docs.python.org/3/library/venv.html):

```
# Install pyenv using brew
brew install pyenv
# Use pyenv to install version python 3.8.10 
pyenv install 3.8.10
# Set your python version to 3.8.10
pyenv local 3.8.10
# Create a virtual environment using venv
python -m venv venv
# Activate your new virtual environment
source venv/bin/activate
```

**Note: if you are running into an error with running `python -m venv venv` you may need to instead use the full path to the python executable when creating your virual environment. An example is `/Users/yourPCName/.pyenv/versions/3.8.10/bin/python -m venv venv`**

### Install pip Version 23

Ensure you are running pip23 to match the version on the servers:

```
pip install --upgrade pip==23.0
```

### Install and Upgrade pip-tools

```
python -m pip install -U pip-tools
```

### Install Pre-Commit Hooks

This project uses various pre-commit hooks to ensure code quality and formatting
consistency.

1. [`Install pre-commit`](https://pre-commit.com/#install) globally.
1. Install the project pre-commit hooks:

```
pip install pre-commit
pre-commit install -f --install-hooks
```

### Install Requirements

```
pip install -r dev.txt
```

### Create Config.ini File

```
touch config.ini
```

And then copy and paste this code into your new file (note: For the actual values, please see [Updating Techtonica's Website](https://docs.google.com/document/d/1oL3BaemFfUD7DfoFzhTSwcX4lPxYbWN3Dy9oZFfGP0Y/edit?tab=t.0)):

```sh
   [default]
   # Acceptable values are sandbox or production
   environment = sandbox
   dev_password = dev_password

   [production]
   square_application_id = production_application_id
   square_access_token = production_access_token
   square_location_id = production_location_id

   [sandbox]
   square_application_id = <sandbox app id>
   square_access_token = <sandbox access token>
   square_location_id = <sandbox location id>

   [slack]
   slack_webhook =  <slack webhook>
```

### Running Locally

Each time you want to work on your code, you will need to activate your virtual environment and run the server locally. You do not need to do any of the setup instructions again (besides installing requirements, if those have changed). 

[If you prefer using Docker, see instructions](#using-docker-to-run-locally).

Activate your virtual environment:

```
source venv/bin/activate
```

Install any requirements if they've changed:

```
pip install -r dev.txt
```

Start the application's server:

```sh
FLASK_DEBUG=1 FLASK_APP=main_site.py flask run
```

Browse to <http://localhost:5000>.

### Run Locally as HTTPS using flask_run_cert

This is required for being able to render and test the Square payment elements.

```sh
pip install pyopenssl
FLASK_DEBUG=1 FLASK_APP=main_site.py FLASK_RUN_CERT=adhoc flask run
```

### Using Docker to Run Locally

#### First Time Using Docker?

1. Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
1. `cd` into the folder that holds your techtonica.org repo
1. Run your app: `docker-compose up`

⚠️ _When there are updates to `requirements.txt` or `Dockerfile`, you will have to
rebuild the Docker image in order for those changes to take effect._

#### For Docker Pros

- To run app: `docker-compose up`
- To rebuild Docker image: `docker build . -t techtonica/website --pull`
- To push latest image to Docker Hub: `docker push techtonica/website`

### CSS / SCSS

Styling changes should be made to the Sass (.scss) files and then compiled to
CSS using one of the following commands:

👷‍♀️ Install Sass using one of the following

Mac: `brew install sass/sass/sass`
Windows: `choco install sass`

```sh
sass static/sass/style.scss static/css/style.css
sass --watch static/sass/style.scss static/css/style.css
```

### Square Testing

There are features on the site that use Square for payments and will periodically need testing (especially if their libraries get updated). Currently this is only the "Post a Job" page.

#### Setup

1. Secrets required for the Square payment API and Slack webhook are stored in a config.ini file in the root directory of our repository.
2. This file is listed in our .gitignore file and will not be included when pushing or pulling updates.
3. You will need to manually add it into your local repository to test these features locally, and will also need to manually add it into whatever Dreamhost server (testing, staging, or production) that you are using as well, if it’s not already there.
4. BE CAREFUL ABOUT environment VALUE! If it’s set to production it will actually charge the cards you test with, so be sure to set it to sandbox when testing locally or on staging or testing.
5. Please see the "Updating Techtonica's Website" doc to get the keys and secrets.

**Running Locally**

Run your server using the following command, it will bypass any HTTPS cert errors.

```
FLASK_DEBUG=1 FLASK_APP=main_site.py FLASK_RUN_CERT=adhoc flask run
```

When navigating to the site, if your browser pops up an HTTPS insecure warning, click "Advanced" and "[Proceed to 127.0.0.1 (unsafe)](chrome-error://chromewebdata/#)"
<img width="720" alt="image" src="https://github.com/user-attachments/assets/20fe29d5-051d-44d4-9d05-6e797012d207" />

Navigate to one of the pages that uses Square, currently "Post a Job".

Follow the instructions on the page, and when instructed to enter a credit card number, use one of the following numbers found [here](https://developer.squareup.com/docs/devtools/sandbox/payments).

### Updating the Demographics Chart for the Apply Section

![This is an example of the chart that can be found on the full-time-program.html page.](static/img/2023-H1-Cohort-Demographics.jpg)

At the moment, we do not have styling in place that will enable us to have a coded, adequately sized piechart while still maintaining mobile responsiveness. Until that happens, here is how to update the piechart when numbers change.

1. Start the server.
2. Open the browser and navigate to the Apply page.
3. Update the `data` section in `static/js/piechart.js#L30`.
4. Uncomment out following in `full-time-program.html`.

```
  <!-- <div class="blue-background">
     <canvas id="myChart" width="700" height="350"></canvas>
  </div> -->
```

5. Take a screenshot of the piechart on the rendered page.
6. Add the screenshot to the `static/img` directory saved with YEAR-H#-Cohort-Demographics.jpg, ex. 2023-H1-Cohort-Demographics.jpg.
7. Update `full-time-program.html` to point to the new image you just added. Update the alt text if necessary.

```
 <img
     src="{{ url_for('static', filename='img/2023-H1-Cohort-Demographics.jpg') }}"
     alt="2023 Cohort Demographics."
     class="full-width-img"
  />
```

8. Re-comment the following.

```
  <!-- <div class="blue-background">
     <canvas id="myChart" width="700" height="350"></canvas>
  </div> -->
```

9. Stop the server
10. Commit your code and open a pull request

### Updating Dependencies

This project uses [pip-tools](https://github.com/jazzband/pip-tools) to manage
dependencies. If you need to add or remove a Python library dependency:
**If there are dependencies only needed for local development, these go in dev.in/dev.txt. Otherwise they go in requirements.in/requirements.txt**

1. Edit `requirements.in`
1. Generate `requirements.txt`:

   ```sh
   pip-compile -U
   ```

Once the new library is used in the code base, you'll need to update the
[isort](https://timothycrosley.github.io/isort/) config to reflect third party
library usage:

```sh
pre-commit run seed-isort-config -a --hook-stage manual
```

For development dependencies:

1. Edit `dev.in`
1. Generate `dev.txt`:

   ```sh
   pip-compile -U dev.in
   ```

## Deployment to DreamHost

The below instructions describe how to deploy your feature branch once it has been tested and your PR has been approved. Make sure your feature branch was branched off of develop.

a. push changes to new branch

b. merge new branch into develop

c. push develop to GitHub

d. delete new branch

e. deploy develop to staging

f. merge develop into main

g. push main to GitHub

h. deploy main to techtonica.org

i. tag the date after deployment

### Initial Setup

1. Follow the instructions in the [Setting up and deploying Python Flask to
   Dreamhost](https://mattcarrier.com/flask-dreamhost-setup/) blog post.

1. Update package tools, while you're still operating in the virtual
   environment:

   ```sh
   pip install -U pip setuptools pip-tools
   ```

1. Create a `config.ini` file in the root directory of the repo in whichever Dreamhost server if there isn't one already present, and populate it with the necessary keys.

   ```sh
   [default]
   # Acceptable values are sandbox or production
   environment = sandbox
   dev_password = dev_password

   [production]
   square_application_id = production_application_id
   square_access_token = production_access_token
   square_location_id = production_location_id

   [sandbox]
   square_application_id = <sandbox app id>
   square_access_token = <sandbox access token>
   square_location_id = <sandbox location id>

   [slack]
   slack_webhook =  <slack webhook>
   ```

### Updating the Site

Important: Only ever Pull from the server! There are currently 3 main servers in use: "staging", "techtonica.org" and "testing".

1. Log in via SSH using your SSH key.

1. Change directory to the appropriate domain:

   ```sh
   cd techtonica.org
   ```

   or

   ```sh
   cd staging.techtonica.org
   ```

1. Activate the virtual envrionment:

   ```sh
   . bin/activate
   ```

1. Change to the source directory:

   ```sh
   cd techtonica
   ```

1. Pull the latest code using

   ```sh
   git pull
   ```

1. Update requirements:

   ```sh
   pip-sync
   ```

1. "Restart" the server to showcase new changes

```sh

# staging.techtonica.org
systemctl --user stop gunicorn_staging
systemctl --user enable gunicorn_staging
systemctl --user restart gunicorn_staging
systemctl --user status gunicorn_staging

# testing.techtonica.org
systemctl --user stop gunicorn_testing
systemctl --user enable gunicorn_testing
systemctl --user restart gunicorn_testing
systemctl --user status gunicorn_testing

# techtonica.org
systemctl --user stop gunicorn_techtonica
systemctl --user enable gunicorn_techtonica
systemctl --user restart gunicorn_techtonica
systemctl --user status gunicorn_techtonica

```

1. Deactivate virtual environment and exit server:

   ```sh
   deactivate
   ```

   ```sh
   exit
   ```

[def]: static/img/2023-H1-Cohort-Demographics.jpg
