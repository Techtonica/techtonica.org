"""for rendering dates, related to application timeline
, dynamically throughout this website"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

APP_OPEN_DATE = datetime.strptime(os.getenv("APP_OPEN_DATE"), "%x %X")
APP_EXTENDED = os.getenv("APP_EXTENDED", "false").lower() == "true"


if APP_EXTENDED:
    APP_CLOSE_DATE = APP_OPEN_DATE + timedelta(weeks=6)
else:
    APP_CLOSE_DATE = APP_OPEN_DATE + timedelta(weeks=4)

TODAY = datetime.today()
print("Today's date is: ", TODAY)

DATE_STRING = APP_CLOSE_DATE.strftime("%B %-d")

APP_OPEN = False

TEXT = ""
if APP_OPEN_DATE is None:
    APP_OPEN = True
elif APP_OPEN_DATE <= TODAY <= APP_CLOSE_DATE and APP_EXTENDED:
    APP_OPEN = True
    TEXT = """Extended!
            Apply by {date} (12pm PT)!""".format(
        date=DATE_STRING
    )
    print(TEXT)
elif APP_OPEN_DATE <= TODAY <= APP_CLOSE_DATE:
    APP_OPEN = True
    TEXT = "Apply Now!"
    print(TEXT)
else:
    APP_OPEN = False

print("APP_OPEN value:", APP_OPEN)

if APP_OPEN:
    print("Applications are currently open!")
else:
    print("Applications are currently closed.")


INFO_SESSION = APP_OPEN_DATE + timedelta(weeks=3)
APPLICATION_WORKSHOP = APP_CLOSE_DATE + timedelta(weeks=1)
PAIR_PROGRAMMING_WITH_STAFF = APPLICATION_WORKSHOP + timedelta(weeks=1)
TAKE_HOME_CODE_CHALLENGE = PAIR_PROGRAMMING_WITH_STAFF + timedelta(weeks=1)
INTERVIEW_FINANCIAL_CONVOS = TAKE_HOME_CODE_CHALLENGE + timedelta(weeks=1)
NOTIFICATION_DAY = INTERVIEW_FINANCIAL_CONVOS + timedelta(weeks=1)
ONBOARDING_DAY = NOTIFICATION_DAY + timedelta(weeks=1)
PRE_WORK_START = ONBOARDING_DAY + timedelta(days=1)
COHORT_START_DAY = PRE_WORK_START + timedelta(weeks=4.5)

START_MONTH = COHORT_START_DAY.strftime("%B")
COHORT_HALF = "H1" if START_MONTH == "January" else "H2"

TRAINING_END = COHORT_START_DAY + timedelta(weeks=24)
JOB_SEARCH_END = COHORT_START_DAY + timedelta(weeks=48)

DATES = {
    "APP_OPEN_DATE": APP_OPEN_DATE,
    "APP_EXTENDED": APP_EXTENDED,
    "APP_CLOSE_DATE": APP_CLOSE_DATE,
    "INFO_SESSION": INFO_SESSION,
    "APPLICATION_WORKSHOP": APPLICATION_WORKSHOP,
    "PAIR_PROGRAMMING_WITH_STAFF": PAIR_PROGRAMMING_WITH_STAFF,
    "TAKE_HOME_CODE_CHALLENGE": TAKE_HOME_CODE_CHALLENGE,
    "INTERVIEW_FINANCIAL_CONVOS": INTERVIEW_FINANCIAL_CONVOS,
    "NOTIFICATION_DAY": NOTIFICATION_DAY,
    "ONBOARDING_DAY": ONBOARDING_DAY,
    "PRE_WORK_START": PRE_WORK_START,
    "COHORT_START_DAY": COHORT_START_DAY,
    "START_MONTH": START_MONTH,
    "COHORT_HALF": COHORT_HALF,
    "TRAINING_END": TRAINING_END,
    "JOB_SEARCH_END": JOB_SEARCH_END,
    "TRAINING_END_MONTH": TRAINING_END.strftime("%B"),
    "JOB_SEARCH_START_MONTH": TRAINING_END.strftime("%B"),
    "JOB_SEARCH_END_MONTH": JOB_SEARCH_END.strftime("%B"),
    "TEXT": TEXT,
}

for key, value in DATES.items():
    print(f"{key}:{value}")
