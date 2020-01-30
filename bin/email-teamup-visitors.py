#!/usr/bin/env python
import ast
import os
import sys
from datetime import date, timedelta

import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail

load_dotenv()

"""
Send a list of upcoming Teamup visitors to designated emails.

1. Fetch a list of next weekday's visitors.
1. If there are any, email them to designated recipients.

The script relies on several environment variables, they must be present in the
runtime environment already, or be present in a `.env` file that's readable by
the script (using `python-dotenv`):

* SENDGRID_API_KEY: SendGrid API access key
* TEAMUP_API_KEY: Teamup API access key
* TEAMUP_CALENDAR_ID: Teamup calendar ID, present in the URL of the calendar
* TEAMUP_SUBCALENDARS = Only show events from this list of sub calendars
* VISITOR_EMAIL_FROM = Tuple in the format of (email, name)
* VISITOR_EMAIL_TO = List of recipient emails
* VISITOR_EMAIL_CC = List of cc emails

Example .env:

```
SENDGRID_API_KEY=top_secret
TEAMUP_API_KEY=more_top_secret
TEAMUP_CALENDAR_ID=get_from_browser_url
TEAMUP_SUBCALENDARS=['Other help/visitors', 'Technical help/visitors']
VISITOR_EMAIL_FROM=('me@example.com', 'Example Person')
VISITOR_EMAIL_TO=['joe@example.com', 'jane@example.com']
VISITOR_EMAIL_CC=['doe@example.com']
```

Currently the script is run via a cron job, where the website is hosted
(DreamHost):

```sh
$ crontab -l
MAILTO="info@techtonica.org"
0 15 * * 1-5 ${HOME}/techtonica.org/bin/python ${HOME}/techtonica.org/techtonica/bin/email-teamup-visitors.py # noqa
```
"""

TEAMUP_API_KEY = os.getenv("TEAMUP_API_KEY")
TEAMUP_CALENDAR_ID = os.getenv("TEAMUP_CALENDAR_ID")
TEAMUP_SUBCALENDARS = [
    c.lower() for c in ast.literal_eval(os.getenv("TEAMUP_SUBCALENDARS"))
]
VISITOR_EMAIL_FROM = From(*(ast.literal_eval(os.getenv("VISITOR_EMAIL_FROM"))))
VISITOR_EMAIL_TO = ast.literal_eval(os.getenv("VISITOR_EMAIL_TO"))
VISITOR_EMAIL_CC = ast.literal_eval(os.getenv("VISITOR_EMAIL_CC"))

TEAMUP_API_URL = "https://api.teamup.com"


def get_visitors():
    next_weekday = get_next_weekday().isoformat()

    visitor_calendars = [
        c["id"]
        for c in get_teamup_subcalendars(TEAMUP_CALENDAR_ID, TEAMUP_SUBCALENDARS)
    ]
    events = get_teampup_events(
        TEAMUP_CALENDAR_ID, next_weekday, next_weekday, visitor_calendars
    )
    return get_teamup_visitors(events)


def send_email(sender, recipients, cc, visitors):
    next_weekday = get_next_weekday().strftime("%a, %b %-d, %Y")

    visitor_markup = "".join([f"<li>{v}</li>" for v in visitors])
    visitor_label = "visitor" if len(visitors) == 1 else "visitors"

    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=f"Techtonica {visitor_label.title()} for {next_weekday}",
        html_content=f"""\
<p>Hi Indeed,</p>

<p>
  Please add the following Techtonica {visitor_label} to the building list for
  {next_weekday}:
</p>

<ul>
{visitor_markup}
</ul>

<p>Thanks!</p>

<p>Techtonica</p>
        """,
    )
    message.cc = cc
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)


# Teamup API client
def get_teamup_subcalendars(calendar_id, subcalendar_name_filters=None):
    response = make_teamup_request(calendar_id, "subcalendars")
    subcalendars = response["subcalendars"]
    if subcalendar_name_filters:
        visitor_subcalendars = [
            c for c in subcalendars if c["name"].lower() in subcalendar_name_filters
        ]
    else:
        visitor_subcalendars = subcalendars
    return visitor_subcalendars


def get_teampup_events(calendar_id, start_date, end_date, subcalendars=None):
    params = {"startDate": start_date, "endDate": end_date}
    if subcalendars:
        params["subcalendarId[]"] = subcalendars

    response = make_teamup_request(calendar_id, "events", params=params)
    return response["events"]


def get_teamup_visitors(events):
    return [e["who"] for e in events if e["who"]]


def make_teamup_request(calendar_id, url_path, params=None):
    headers = {"Teamup-Token": TEAMUP_API_KEY}
    response = requests.get(
        f"{TEAMUP_API_URL}/{calendar_id}/{url_path}", headers=headers, params=params
    )
    return response.json()


def get_next_weekday():
    today = date.today()
    day_of_week = today.isoweekday()
    if day_of_week == 5:  # Friday
        next_weekday = today + timedelta(days=3)
    elif day_of_week == 6:  # Saturday
        next_weekday = today + timedelta(days=2)
    else:
        next_weekday = today + timedelta(days=1)
    return next_weekday


if __name__ == "__main__":
    visitors = get_visitors()
    if len(sys.argv) > 1 and sys.argv[1] == "dry-run":
        if visitors:
            print(f"Next visitors: {', '.join(visitors)}")
        else:
            print("No visitors")
    elif visitors:
        send_email(VISITOR_EMAIL_FROM, VISITOR_EMAIL_TO, VISITOR_EMAIL_CC, visitors)
