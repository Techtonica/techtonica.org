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

The audience of the website is made up of (potential) volunteers and sponsors.
(Participants will be contacted via local organizations.)

## What

We need to effectively communicate that Techtonica and its participants are
worth supporting.

## How

There should be a good understanding of how the program works with vetting,
training, mentoring, and hiring.

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
2. `cd` into the folder that holds your techtonica.org repo
3. Build your app: `docker-compose build --pull`
4. Run your app: `docker-compose up`

_When there are updates to the Dockerfile, you will have to rebuild your app in order for those changes to take effect_

#### For Docker Pros

To run app: `docker-compose build --pull`

To rebuild app: `docker-compose up`

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

### Initial Setup

1. Follow the instructions in the [Setting up and deploying Python Flask to
   Dreamhost](https://mattcarrier.com/flask-dreamhost-setup/) blog post.

1. Update package tools, while you're still operating in the virtual
   environment:

   ```sh
   pip install -U pip setuptools pip-tools
   ```

### Updating the Site

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

1. Use the usual `git` commands to get the latest code or check out another
   branch.

1. Update requirements:

   ```sh
   pip-sync
   ```

1. "Restart" the passenger process:

   ```sh
   cd .. && touch tmp/restart.txt
   ```
