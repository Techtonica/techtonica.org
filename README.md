# Techtonica

This repo is for [the Techtonica website](http://techtonica.org), which is
currently hosted on DreamHost.

- [Techtonica](#techtonica)
  - [Who](#who)
  - [What](#what)
  - [How](#how)
  - [Getting Started](#getting-started)
    - [Set Up Virtual Environment](#set-up-virtual-environment)
    - [Install and Upgrade pip-tools](#install-and-upgrade-pip-tools)
    - [Install Pre-Commit Hooks](#install-pre-commit-hooks)
    - [Install Requirements](#install-requirements)
    - [Create .env File](#create-env-file)
    - [Pre-Commit Hooks Guide](#pre-commit-hooks-guide)
    - [Optional: Installing Prettier Plug-in Locally](#optional-installing-prettier-plug-in-locally)
    - [Running Locally](#running-locally)
    - [Using Docker to Run Locally](#using-docker-to-run-locally)
      - [First Time Using Docker?](#first-time-using-docker)
      - [For Docker Pros](#for-docker-pros)
    - [CSS / SCSS](#css--scss)
    - [Alt-Text Guidelines](#alt-text-guidelines)
    - [Square Testing](#square-testing)
      - [Setup](#setup)
      - [Running Locally](#running-locally-1)
    - [Updating the Demographics Chart for the Apply Section](#updating-the-demographics-chart-for-the-apply-section)
    - [Updating Testimonials](#updating-testimonials)
    - [Updating Dependencies](#updating-dependencies)
    - [Connecting to the Database](#connecting-to-the-database)
  - [Deployment to DreamHost](#deployment-to-dreamhost)
    - [Initial Setup](#initial-setup)
    - [Deploy Feature Branch](#deploy-feature-branch)
    - [Updating the Site](#updating-the-site)

## Who

The audience of the website is made up of (potential) volunteers, sponsors, and program participants.

## What

We need to effectively communicate that Techtonica and its participants are worth supporting and share details of the program for potential applicants and volunteers.

## How

There should be a good understanding of how the program works with vetting, training, mentoring, and placements.

[Detailed instructions on how to update the website](https://docs.google.com/document/d/1oL3BaemFfUD7DfoFzhTSwcX4lPxYbWN3Dy9oZFfGP0Y/edit)

## Getting Started

You need Python version 3.13.2 and Pip version 25.0.1 in order to properly update dependencies and replicate the production server environment locally.

Using Python 3.13.2 and pip 25.0.1 helps ensure compatibility and consistency between your local development environment and the server environment. This minimizes potential issues during deployment by keeping dependencies in sync with the versions expected by the servers and eliminates discrepancies caused by different versions, ensuring that code runs the same way on every developer's machine.

### Set Up Virtual Environment

It is recommended you use a virtual environment to keep dependencies
required by different projects separate. [Learn more about Python virtual
environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Set up virtual environment with Python 3.13.2 and Pip 25.0.1 using [pyenv](https://github.com/pyenv/pyenv) and [venv](https://docs.python.org/3/library/venv.html):

- Install pyenv using brew

```bash
brew install pyenv
```

- Use pyenv to install version python 3.13.2

```bash
pyenv install 3.13.2
```

- Set your python version to 3.13.2

```bash
pyenv local 3.13.2
```

- Ensure correct version of python

```bash
python --version
# If not 3.13.2, try
eval "$(pyenv init -)"
```

- Upgrade global pip and virtualenv to ensure latest version

```bash
pip install --upgrade pip
pip install --upgrade virtualenv
```

- Create a virtual environment using venv

```bash
python -m venv venv
```

- Activate your new virtual environment

```bash
source venv/bin/activate
```

- Verify pip version and upgrade if needed

```bash
pip --version
# If it is not the latest version 25.0.1, upgrade pip
pip install --upgrade pip
```

**Note: if you are running into an error with running `python -m venv venv` you may need to instead use the full path to the python executable when creating your virual environment. An example is `/Users/yourPCName/.pyenv/versions/3.13.2/bin/python -m venv venv`**

### Install and Upgrade pip-tools

```
python -m pip install -U pip-tools
```

### Install Pre-Commit Hooks

This project uses various pre-commit hooks to ensure code quality and formatting
consistency.

1. [`Install pre-commit`](https://pre-commit.com/#install) globally.
1. Install the project pre-commit hooks:

```bash
pip install pre-commit
pre-commit install -f --install-hooks
```

### Install Requirements

```
pip install -r dev.txt
```

If you get an error installing mysqlclient, deactivate your virtual environment and make sure mysql is installed on your computer by doing the following:

```bash
mysql --version
# If command not found, do the following
brew install mysql
```

### Create .env File

```
touch .env
```

And then copy and paste this code into your new file. There is a sample in .env.example for you to use as well. Please contact a Techtonica Staff member for `.env` file contents. Staff members can be reached through the Techtonica Slack workspace, or you can fill out [this form](https://docs.google.com/forms/d/e/1FAIpQLScjCF6_xzIn-Uht3MDOr1__3YpIYDCTzx80cIE0KVCsPqcYKQ/viewform).

```sh
# Your environment, either "local", "prod", "staging", or "testing"
ENVIRONMENT="local"
# Square credentials for the job posting feature
SQUARE_APPLICATION_ID="id"
SQUARE_ACCESS_TOKEN="token"
SQUARE_LOCATION_ID="location"
SLACK_WEBHOOK="webhook"
PAYMENT_FORM_URL="url"
# Application open date in format "MM/DD/YYYY HH:MM:SS" in UTC
APP_OPEN_DATE="date"
APP_EXTENDED="boolean"
# Database credentials - more extensive explanation in the database section
DB_USERNAME="username"
DB_PASSWORD="password"
DB_HOST="host"
DB_NAME="name"

### Pre-Commit Hooks Guide

To manually run, test, and upgrade pre-commit hooks locally, follow these steps:

To run hooks on specific files, use the command:

```

pre-commit run --files <file1> <file2>

```

For example, if you want to test a single file, you can use

```

pre-commit run --files main_site.py

```

To run all hooks on every file in the repository, use the
command

```

pre-commit run --all-files

```

If you need to upgrade your hooks to their latest versions, run

```

pre-commit autoupdate

```

After upgrading, ensure you reinstall the hooks by running

```

pre-commit install

```

### Optional: Installing Prettier Plug-in Locally

#### Managing Prettier Commit Behavior

When using Prettier in your project, you may encounter unexpected behavior with the **Prettier pre-commit hook**. This guide provides context on what’s happening, why, and how to address it effectively.

#### Context

The Prettier pre-commit hook automatically formats code when you attempt to commit changes. However, in some cases, this hook may lead to **unstaged changes** after formatting your files. This can occur if the local code is not already formatted according to the Prettier configuration. This behavior might feel confusing or disruptive to users unfamiliar with the tool.

#### What to Expect

1. **Scenario:**
   During `git commit`, the Prettier pre-commit hook runs and identifies formatting issues.

   - If applicable, Prettier will fix these issues but may leave **unstaged changes** in your working directory.

2. **Outcome:**
   You will need to stage these changes again (`git add`) before committing and pushing your changes to the remote repository.

#### Why This Happens

The Prettier pre-commit hook is designed to ensure consistent code formatting across the repository. When code is committed without being properly formatted, Prettier intervenes by reformatting the code. If these changes are not staged, they remain as unstaged changes in your working directory.

#### Solution: Installing Prettier Plug-in Locally

To avoid this behavior and streamline your workflow, you can install a Prettier plug-in in your local IDE. The plug-in will format your code **on-save**, ensuring it adheres to the Prettier configuration before you attempt to commit.

#### Steps:

1. Install the Prettier plug-in in your IDE (e.g., VS Code).
   ![Prettier Plug-in in VS Code](static/img/Prettier-Plug-In.png)

2. Enable the "Format on Save" setting:

   - Go to **Settings** > **Text Editor** > **Formatting** > Enable **Format on Save**.

3. Ensure your file is saved before running `git commit`.

#### Optional: If You Don’t Want to Use the Plug-in

If you would rather not install the Prettier plug-in, you can still manage the behavior manually:

1. After committing, check for **unstaged changes** caused by Prettier.
2. Use `git add` to stage the changes and then commit again.

#### Expected Result

With the Prettier plug-in installed and enabled:

- Your code will automatically be formatted before saving, ensuring the pre-commit hook finds no issues.
- The pre-commit hook will not create new **unstaged changes**, making your workflow smoother.

If you opt to manage this manually, be aware of the additional step of staging unstaged changes before pushing to remote.

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

The Techtonica website uses Sass to manage its CSS.

Styling changes should **only** be made to the Sass (.scss) files and then compiled to
CSS using one of the following commands:

Compile once:

`sass static/sass/style.scss static/css/style.css`

OR

Watch for changes using `--watch`:

```sh
sass --watch static/sass/style.scss:static/css/style.css
```

By running the `--watch` command, any modifications made to the CSS files are instantly reflected, saving you time and ensuring your styles are always up-to-date.

For installation help and more details, see the [CSS/SCSS Styling Instructions Wiki](https://github.com/Techtonica/techtonica.org/wiki/CSS-SCSS-Styling-Instructions-Wiki)

### Alt-Text Guidelines

To ensure accessibility for all users, alt-text on our site should follow these best practices:

- Avoid line breaks, as they disrupt screen readers and negatively impact user experience.
- Keep alt-text under 125 characters to ensure full readability.
- Refrain from using emojis, as their descriptions can vary across platforms and may confuse screen reader users.
- Similarly, avoid special characters unless essential, as they can be misinterpreted or skipped by assistive technologies.
- Alt-text should be descriptive, concise, and context-aware, avoiding redundancy with nearby text.

For more detailed guidelines and examples, refer to the [Alt-Text Wiki](https://github.com/Techtonica/techtonica.org/wiki/Alt%E2%80%90Text-Guidelines).

### Square Testing

There are features on the site that use Square for payments and will periodically need testing (especially if their libraries get updated). Currently this is only the "Post a Job" page.

#### Setup

1. Secrets required for the Square payment API and Slack webhook are stored in a .env file in the root directory of our repository.
2. This file is listed in our .gitignore file and will not be included when pushing or pulling updates.
3. You will need to manually add it into your local repository to test these features locally, and will also need to manually add it into whatever Dreamhost server (testing, staging, or production) that you are using as well, if it’s not already there.
4. BE CAREFUL ABOUT environment VALUE! If it’s set to production it will actually charge the cards you test with, so be sure to set it to sandbox when testing locally or on staging or testing.
5. Please contact a member of Techtonica staff to get the keys and secrets.

#### Running Locally

Run your server using the following command, it will bypass any HTTPS cert errors.

```sh
pip install pyopenssl
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

### Updating Testimonials

To update and add testimonial images, follow these steps:

1. Upload your testimonial image to Canva, crop it as needed, and download it as a `.png`.
2. The image name should follow this format: `Platform-FirstName-Topic-Year-min.png` (e.g., `Linkedin-Daamiah-Techtonica-2025-min.png`).
3. Use [ImageOptim](https://imageoptim.com/mac) to compress the image for better web performance.
4. Save the optimized image in the `techtonica.org/static/img/testimonials` folder within the repository to maintain consistency and easy access.

For detailed instructions, visit the [full guide on the Wiki](https://github.com/Techtonica/techtonica.org/wiki/How-to-Add-and-Optimize-Testimonial-Images).

### Updating Dependencies

This project uses [pip-tools](https://github.com/jazzband/pip-tools) to manage
dependencies. _If there are dependencies only needed for local development, these go in dev.in/dev.txt. Otherwise, they go in requirements.in/requirements.txt_. If you need to add or remove a Python library dependency:

1. Edit `requirements.in` or `dev.in` (referred to below as `file_name.in`). If you update requirements.in, you must also re-compile dev.in after.
1. Generate the .txt file

   ```sh
   pip-compile -U <file_name.in>
   pip install -r <file_name.txt>
   ```

### Connecting to the Database

There are 3 MySQL databases for this repo, one for each environment: **prod, testing & staging.**

The credentials for these are stored in .env (each environment has its own .env). When developing locally, use the "testing" credentials.

To connect these locally, you can use a GUI tool such as [Sequel Pro](https://sequelpro.com/) or [MySQL Workbench](https://www.mysql.com/products/workbench/).

Enter the credentials into the connection window with the following:

- **Name:** Anything, but should indicate which environment it points to
- **Host:** DB_HOST from credentials
- **Username:** DB_USERNAME from credentials
- **Password:** DB_PASSWORD from credentials
- **Database:** DB_NAME from credentials
- **Port:** 3306

![This is a sample screenshot of a Sequel Pro connection.](static/img/database_connection.png)

## Deployment to DreamHost

### Initial Setup

The below instructions are for setting up a new server in DreamHost.

1. Follow the instructions in the [Setting up and deploying Python Flask to
   Dreamhost](https://mattcarrier.com/flask-dreamhost-setup/) blog post.

1. Update package tools, while you're still operating in the virtual
   environment:

   ```sh
   pip install -U pip setuptools pip-tools
   ```

1. Create a `.env` file in the root directory of the repo in whichever Dreamhost server if there isn't one already present, and populate it with the necessary keys.

```sh
ENVIRONMENT="local"
SQUARE_APPLICATION_ID="id"
SQUARE_ACCESS_TOKEN="token"
SQUARE_LOCATION_ID="location"
SLACK_WEBHOOK="webhook"
PAYMENT_FORM_URL="url"
APP_OPEN_DATE="date"
APP_EXTENDED="boolean"
DB_USERNAME="username"
DB_PASSWORD="password"
DB_HOST="host"
DB_NAME="name"
```

### Deploy Feature Branch

The below instructions describe how to deploy your feature branch once it has been tested and your PR has been approved. Make sure your feature branch was branched off of develop.

1. Push changes to feature branch

1. Merge feature branch into develop

1. Push develop to GitHub

1. Delete feature branch

1. Deploy develop to staging

1. Merge develop into main

1. Push main to GitHub

1. Deploy main to techtonica.org

1. Tag the date after deployment

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
