""" This file generates the application timeline variables
to dynamically render relevant dates and information """

import logging
import os
from datetime import datetime, timedelta

import pytz
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# confirms timezone is set to pacific standard time (PST)
pst = pytz.timezone("America/Los_Angeles")


# checks for dates in dot env file
def parse_env_date(env_var, calculated_date):
    env_value = os.getenv(env_var, "").strip()
    if not env_value:
        logger.info(
            f"{env_var} not found in .env, using calculated date: {calculated_date}"  # noqa: E501
        )
        return calculated_date

    # handles several date formats
    formats = [
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%y %H:%M:%S",
        "%m/%d/%y",
        "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            parsed_date = pst.localize(datetime.strptime(env_value, fmt))
            logger.info(f"{env_var} found in .env: {parsed_date}")
            return parsed_date
        except ValueError:
            continue

    logger.warning(
        f"Invalid {env_var} format in .env ({env_value}), using calculated date: {calculated_date}"  # noqa: E501
    )
    return calculated_date


# functions to format dates, if available
def format_date(date):
    return date.strftime("%B %d, %Y") if date else None


def format_month_year(date):
    return date.strftime("%B %Y") if date else None


def generate_application_timeline():
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

    info_session = parse_env_date(
        "INFO_SESSION",
        app_open_datetime + timedelta(weeks=3) if app_open_datetime else None,
    )
    application_workshop = parse_env_date(
        "APPLICATION_WORKSHOP",
        (
            app_close_datetime + timedelta(weeks=1)
            if app_close_datetime
            else None  # noqa: E501
        ),
    )
    pair_programming = parse_env_date(
        "PAIR_PROGRAMMING_WITH_STAFF",
        (
            application_workshop + timedelta(weeks=1)
            if application_workshop
            else None  # noqa: E501
        ),
    )
    take_home = parse_env_date(
        "TAKE_HOME_CODE_CHALLENGE",
        pair_programming + timedelta(weeks=1) if pair_programming else None,
    )
    interview = parse_env_date(
        "INTERVIEW_FINANCIAL_CONVOS",
        take_home + timedelta(weeks=1) if take_home else None,
    )
    notification_day = parse_env_date(
        "NOTIFICATION_DAY",
        interview + timedelta(weeks=1) if interview else None,  # noqa: E501
    )
    onboarding_day = parse_env_date(
        "ONBOARDING_DAY",
        notification_day + timedelta(weeks=1) if notification_day else None,
    )
    pre_work_start = parse_env_date(
        "PRE_WORK_START",
        onboarding_day + timedelta(days=1) if onboarding_day else None,  # noqa: E501
    )
    cohort_start_day = parse_env_date(
        "COHORT_START_DAY",
        pre_work_start + timedelta(weeks=4.5) if pre_work_start else None,
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
        "APP_OPEN_DATE": format_date(app_open_datetime),
        "APP_EXTENDED": app_extended,
        "APP_CLOSE_DATE": format_date(app_close_datetime),
        "INFO_SESSION": format_date(info_session),
        "APPLICATION_WORKSHOP": format_date(application_workshop),
        "PAIR_PROGRAMMING_WITH_STAFF": format_date(pair_programming),
        "TAKE_HOME_CODE_CHALLENGE": format_date(take_home),
        "INTERVIEW_FINANCIAL_CONVOS": format_date(interview),
        "NOTIFICATION_DAY": format_date(notification_day),
        "ONBOARDING_DAY": format_date(onboarding_day),
        "PRE_WORK_START": format_date(pre_work_start),
        "COHORT_START_DAY": format_date(cohort_start_day),
        "START_MONTH": start_month,
        "START_YEAR": start_year,
        "COHORT_HALF": cohort_half,
        "TRAINING_END": format_date(training_end),
        "TRAINING_END_MONTH_YEAR": format_month_year(training_end),
        "JOB_SEARCH_START_MONTH_YEAR": format_month_year(training_end),
        "JOB_SEARCH_END_MONTH_YEAR": format_month_year(job_search_end),
        "APP_OPEN": app_open,
        "TEXT": (
            "Apply Now!"
            if not app_open
            else f"Apply by {app_close_datetime.strftime('%B %d')} (12pm PT)!"
        ),
    }
