# Techtonica

This repo is for [the Techtonica website](http://techtonica.org), which is
currently hosted on DreamHost.

- [Who](#who)
- [What](#what)
- [How](#how)
- [Getting Started](#getting-started)
  - [Install Pre-Commit Hooks](#install-pre-commit-hooks)
  - [Running Locally](#running-locally)
  - [Using Docker to Run Locally](#using-docker-to-run-locally)
  - [CSS / SCSS](#css--scss)
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

Detailed instructions on how to update the website:
https://docs.google.com/document/d/1oL3BaemFfUD7DfoFzhTSwcX4lPxYbWN3Dy9oZFfGP0Y/edit

## Getting Started

This app uses Python 3.6; please stick to this version when doing development.

### Install Pre-Commit Hooks

This project uses various pre-commit hooks to ensure code quality and formatting
consistency.

1. [`Install pre-commit`](https://pre-commit.com/#install) globally.
1. Install the project pre-commit hooks:

   ```sh
   pre-commit install -f --install-hooks
   ```

### Running Locally

[If you prefer using Docker, see instructions](#using-docker-to-run-locally).

It is recommended you use a virtual environment tool to keep dependencies
required by different projects separate. [Learn more about Python virtual
environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install the project dependencies. In the project root run:

```sh
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

Styling changes should be made to the Sass (.scss) files and then compiled to
CSS using one of the following commands:

👷‍♀️ Install Sass using one of the following

Mac: `brew install sass/sass/sass`
Windows: `choco install sass`

```sh
sass static/sass/style.scss static/css/style.css
sass --watch static/sass/style.scss static/css/style.css
```

### Updating Dependencies

This project uses [pip-tools](https://github.com/jazzband/pip-tools) to manage
dependencies. If you need to add or remove a Python library dependency:

1. Edit `requirement.in`
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

Make sure you branch off develop, if you want to make changes.

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

### Updating the Site

Important: Only ever Pull form the server!

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

1. "Restart" the passenger process:

   ```sh
   cd .. && touch tmp/restart.txt
   ```

1. Deactivate virtual envirement and exit server:

   ```sh
   deactivate
   ```

   ```sh
   exit
   ```
