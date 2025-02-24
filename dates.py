""" This file generates the application timeline
to dynamically render relevant dates and information """

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()


def generate_application_timeline():
    # Get application open date from .env
    app_open_date_str = os.getenv("APP_OPEN_DATE")
    app_extended = os.getenv("APP_EXTENDED", "false").lower() == "true"

    # Error handling: Ensure APP_OPEN_DATE is set
    if not app_open_date_str:
        print("Warning: APP_OPEN_DATE is not set.")
        app_open_datetime = None
    else:
        try:
            app_open_datetime = datetime.strptime(
                app_open_date_str, "%m/%d/%y %H:%M:%S"
            )
            app_open_datetime = app_open_datetime.replace(tzinfo=timezone.utc)
        except ValueError:
            print(
                f"""Error: Unexpected APP_OPEN_DATE format!" f"({app_open_date_str})"""
            )
            app_open_datetime = None

    # Determine application close date
    if app_open_datetime:
        app_close_datetime = app_open_datetime + timedelta(
            weeks=6 if app_extended else 4
        )
        app_close_datetime = app_close_datetime.replace(tzinfo=timezone.utc)
    else:
        app_close_datetime = None

    # Today's date
    today = datetime.now(timezone.utc)

    # Application status logic
    app_open = "false"
    text = "Apply Now!"

    if app_open_datetime is None or app_close_datetime is None:
        app_open = True  # Default to true if APP_OPEN_DATE is missing
        text = "Apply Now!"
    elif app_open_datetime <= today <= app_close_datetime:
        app_open = True
        if app_extended:
            text = (
                "Extended!\nApply by "
                f"{app_close_datetime.strftime('%B')} "
                f"{app_close_datetime.day} (12pm PT)!"
            )
        else:
            text = (
                "Apply by "
                f"{app_close_datetime.strftime('%B')} "
                f"{app_close_datetime.day} (12pm PT)!"
            )

    # Generate event dates if APP_OPEN_DATE is valid
    if app_open_datetime:
        info_session = app_open_datetime + timedelta(weeks=3)
        application_workshop = app_close_datetime + timedelta(weeks=1)
        pair_programming_with_staff = application_workshop + timedelta(weeks=1)
        take_home_code_challenge = pair_programming_with_staff + timedelta(weeks=1)
        interview_financial_convos = take_home_code_challenge + timedelta(weeks=1)
        notification_day = interview_financial_convos + timedelta(weeks=1)
        onboarding_day = notification_day + timedelta(weeks=1)
        pre_work_start = onboarding_day + timedelta(days=1)
        cohort_start_day = pre_work_start + timedelta(weeks=4.5)

        start_month = cohort_start_day.strftime("%B")
        cohort_half = "H1" if start_month == "January" else "H2"

        training_end = cohort_start_day + timedelta(weeks=24)
        job_search_end = cohort_start_day + timedelta(weeks=48)
    else:
        # If no APP_OPEN_DATE, keep all dates as None
        info_session = None
        application_workshop = None
        pair_programming_with_staff = None
        take_home_code_challenge = None
        interview_financial_convos = None
        notification_day = None
        onboarding_day = None
        pre_work_start = None
        cohort_start_day = None
        start_month = None
        cohort_half = None
        training_end = None
        job_search_end = None

    return {
        "APP_OPEN_DATE": app_open_datetime,
        "APP_EXTENDED": app_extended,
        "APP_CLOSE_DATE": app_close_datetime,
        "INFO_SESSION": info_session,
        "APPLICATION_WORKSHOP": application_workshop,
        "PAIR_PROGRAMMING_WITH_STAFF": pair_programming_with_staff,
        "TAKE_HOME_CODE_CHALLENGE": take_home_code_challenge,
        "INTERVIEW_FINANCIAL_CONVOS": interview_financial_convos,
        "NOTIFICATION_DAY": notification_day,
        "ONBOARDING_DAY": onboarding_day,
        "PRE_WORK_START": pre_work_start,
        "COHORT_START_DAY": cohort_start_day,
        "START_MONTH": start_month,
        "COHORT_HALF": cohort_half,
        "TRAINING_END": training_end,
        "JOB_SEARCH_END": job_search_end,
        "TRAINING_END_MONTH": (training_end.strftime("%B") if training_end else None),
        "JOB_SEARCH_START_MONTH": (
            training_end.strftime("%B") if training_end else None
        ),
        "JOB_SEARCH_END_MONTH": (
            job_search_end.strftime("%B") if job_search_end else None
        ),
        "TEXT": text,
        "APP_OPEN": app_open,
    }


# timeline = generate_application_timeline()
