""" This file generates the application timeline variables
to dynamically render relevant dates and information """

import os
from datetime import datetime, timedelta

import pytz
from dotenv import load_dotenv

load_dotenv()

# confirms timezone is set to pacific standard time (PST)
pst = pytz.timezone("America/Los_Angeles")


# checks for dates in dot env file
def parse_env_date(env_var, calculated_date):
    env_value = os.getenv(env_var, "").strip()
    if not env_value:
        return calculated_date

    # handles several date formats
    formats = ["%m/%d/%y %H:%M:%S", "%m/%d/%y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            return pst.localize(datetime.strptime(env_value, fmt))
        except ValueError:
            continue

    print(f"Warning: Invalid {env_var} format ({env_value}).")
    return calculated_date


def generate_application_timeline():
    # determine if hard code dates are set in dot env
    hardcoded = os.getenv("HARD_CODED_DATES", "false").lower()
    use_hardcoded = hardcoded == "true"

    app_open_date_str = os.getenv("APP_OPEN_DATE")
    app_extended = os.getenv("APP_EXTENDED", "false").lower() == "true"

    if app_open_date_str:
        try:
            app_open_datetime = pst.localize(
                datetime.strptime(app_open_date_str, "%m/%d/%y %H:%M:%S")
            )
        except ValueError:
            print(
                f"Error: Invalid APP_OPEN_DATE format ({app_open_date_str})!"
            )  # noqa: E501
            app_open_datetime = None
    else:
        print("Warning: APP_OPEN_DATE is not set.")
        app_open_datetime = None

    if app_open_datetime:
        app_close_datetime = app_open_datetime + timedelta(
            days=25 + (10 if app_extended else 0)
        )
    else:
        app_close_datetime = None

    today = datetime.now(pst)
    app_open = app_open_datetime and (
        app_open_datetime <= today <= app_close_datetime
    )  # noqa: E501

    if use_hardcoded:
        info_session = parse_env_date(
            "INFO_SESSION", app_open_datetime + timedelta(weeks=3)
        )
        application_workshop = parse_env_date(
            "APPLICATION_WORKSHOP", app_close_datetime + timedelta(weeks=1)
        )
        pair_programming = parse_env_date(
            "PAIR_PROGRAMMING_WITH_STAFF",
            application_workshop + timedelta(weeks=1),  # noqa: E501
        )
        take_home = parse_env_date(
            "TAKE_HOME_CODE_CHALLENGE", pair_programming + timedelta(weeks=1)
        )
        interview = parse_env_date(
            "INTERVIEW_FINANCIAL_CONVOS", take_home + timedelta(weeks=1)
        )
        notification_day = parse_env_date(
            "NOTIFICATION_DAY", interview + timedelta(weeks=1)
        )
        onboarding_day = parse_env_date(
            "ONBOARDING_DAY", notification_day + timedelta(weeks=1)
        )
        pre_work_start = parse_env_date(
            "PRE_WORK_START", onboarding_day + timedelta(days=1)
        )
        cohort_start_day = parse_env_date(
            "COHORT_START_DAY", pre_work_start + timedelta(weeks=4.5)
        )
    else:
        info_session = (
            app_open_datetime + timedelta(weeks=3)
            if app_open_datetime
            else None  # noqa: E501
        )
        application_workshop = (
            app_close_datetime + timedelta(weeks=1)
            if app_close_datetime
            else None  # noqa: E501
        )
        pair_programming = (
            application_workshop + timedelta(weeks=1)
            if application_workshop
            else None  # noqa: E501
        )
        take_home = (
            pair_programming + timedelta(weeks=1) if pair_programming else None
        )  # noqa: E501
        interview = take_home + timedelta(weeks=1) if take_home else None
        notification_day = (
            interview + timedelta(weeks=1) if interview else None
        )  # noqa: E501
        onboarding_day = (
            notification_day + timedelta(weeks=1) if notification_day else None
        )
        pre_work_start = (
            onboarding_day + timedelta(days=1) if onboarding_day else None
        )  # noqa: E501
        cohort_start_day = (
            pre_work_start + timedelta(weeks=4.5) if pre_work_start else None
        )

    start_year = cohort_start_day.strftime("%Y") if cohort_start_day else None
    start_month = cohort_start_day.strftime("%B") if cohort_start_day else None
    cohort_half = (
        "H1" if start_month == "January" else "H2" if start_month else None
    )  # noqa: E501

    training_end = (
        cohort_start_day + timedelta(weeks=24) if cohort_start_day else None
    )  # noqa: E501
    job_search_end = (
        cohort_start_day + timedelta(weeks=48) if cohort_start_day else None
    )

    return {
        "APP_OPEN_DATE": (
            app_open_datetime.strftime("%B %d, %Y")
            if app_open_datetime
            else None  # noqa: E501
        ),
        "APP_EXTENDED": app_extended,
        "HARD_CODED_DATES": hardcoded,
        "APP_CLOSE_DATE": (
            app_close_datetime.strftime("%B %d, %Y")
            if app_close_datetime
            else None  # noqa: E501
        ),
        "INFO_SESSION": (
            info_session.strftime("%B %d, %Y") if info_session else None
        ),  # noqa: E501
        "APPLICATION_WORKSHOP": (
            application_workshop.strftime("%B %d, %Y")
            if application_workshop
            else None  # noqa: E501
        ),
        "PAIR_PROGRAMMING_WITH_STAFF": (
            pair_programming.strftime("%B %d, %Y")
            if pair_programming
            else None  # noqa: E501
        ),
        "TAKE_HOME_CODE_CHALLENGE": (
            take_home.strftime("%B %d, %Y") if take_home else None
        ),
        "INTERVIEW_FINANCIAL_CONVOS": (
            interview.strftime("%B %d, %Y") if interview else None
        ),
        "NOTIFICATION_DAY": (
            notification_day.strftime("%B %d, %Y")
            if notification_day
            else None  # noqa: E501
        ),
        "ONBOARDING_DAY": (
            onboarding_day.strftime("%B %d, %Y") if onboarding_day else None
        ),
        "PRE_WORK_START": (
            pre_work_start.strftime("%B %d, %Y") if pre_work_start else None
        ),
        "COHORT_START_DAY": (
            cohort_start_day.strftime("%B %d, %Y")
            if cohort_start_day
            else None  # noqa: E501
        ),
        "START_MONTH": start_month,
        "START_YEAR": start_year,
        "COHORT_HALF": cohort_half,
        "TRAINING_END": (
            training_end.strftime("%B %d, %Y") if training_end else None
        ),  # noqa: E501
        "TRAINING_END_MONTH_YEAR": (
            training_end.strftime("%B %Y") if training_end else None
        ),
        "JOB_SEARCH_START_MONTH_YEAR": (
            training_end.strftime("%B %Y") if training_end else None
        ),
        "JOB_SEARCH_END_MONTH_YEAR": (
            job_search_end.strftime("%B %Y") if job_search_end else None
        ),
        "APP_OPEN": app_open,
        "TEXT": (
            "Apply Now!"
            if not app_open
            else f"Apply by {app_close_datetime.strftime('%B %d')} (12pm PT)!"
        ),
    }


# below will be removed
# left here for testing during pr review
# timeline = generate_application_timeline()


# for key, value in timeline.items():
#     print(f"{key}: {value}")
