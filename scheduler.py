from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import requests
import uuid

scheduler = BackgroundScheduler()
scheduler.start()


def schedule_email(time_str: str, route: str, email_data: dict) -> str:
    try:
        run_time = datetime.fromisoformat(time_str)
    except ValueError:
        raise ValueError("Invalid ISO format")

    job_id = str(uuid.uuid4())

    scheduler.add_job(
        send_email_job,
        trigger=DateTrigger(run_date=run_time),
        args=[route, email_data],
        id=job_id,
        replace_existing=True,
    )

    return job_id


def send_email_job(route: str, email_data: dict):
    print(f"Sending email to {email_data.get('to')} via route {route}")
    url = f"https://mailassist.abusha.tech/{route}"  # change if needed
    print(f"Email data: {email_data}")
    print(f"URL: {url}")
    try:
        response = requests.post(url, json=email_data)
        print(f"Email sent to {email_data.get('to')}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")
