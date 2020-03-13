# Techtonica

This repo is for [the Techtonica website](http://techtonica.org), which is
currently hosted on DreamHost.

### Who

The audience of the website is made up of (potential) volunteers and sponsors.
(Apprentices will be contacted via local organizations.)

### What

We need to effectively communicate that Techtonica and its apprentices are
worth supporting.

### How

There should be a good understanding of how the program works with vetting,
training, mentoring, and hiring.

## Getting Started

This app uses Python 3.6; please stick to this version.

### Running Locally

It is recommended you use a virtual environment tool to keep dependencies
required by different projects separate. [Learn more about Python virtual
environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

Install the project dependencies. In the project root run:

```sh
pip install -r requirements.txt
```

Start the application's server:

```sh
FLASK_DEBUG=1 FLASK_APP=main_site.py flask run
```

Browse to <http://localhost:5000>.

### CSS / SCSS

Styling changes should be made to the Sass (.scss) files and then compiled to
CSS using one of the following commands:

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

## Deployment to DreamHost

## Initial Setup

1. Follow the instructions in the [Setting up and deploying Python Flask to
   Dreamhost](https://mattcarrier.com/flask-dreamhost-setup/) blog post.

1. Update package tools, while you're still operating in the virtual
   environment:

   ```sh
   pip install -U pip setuptools pip-tools
   ```

## Updating the Site

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
