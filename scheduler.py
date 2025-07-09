from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import uuid

# In-memory store; replace with Redis for production
scheduled_jobs = {}

scheduler = BackgroundScheduler()
scheduler.start()


def schedule_email(time: str, route: str, email_data: dict):
    dt = datetime.fromisoformat(time)
    job_id = f"{dt.isoformat()}::{uuid.uuid4()}"

    def job_function():
        try:
            print(f"Sending to: {route}")
            response = requests.post(
                f"https://mailassist.abusha.tech/api{route}",
                json=email_data,
                timeout=10
            )
            print(f"Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error sending scheduled email: {e}")

        # Clean up job from memory
        scheduled_jobs.pop(job_id, None)

    scheduler.add_job(job_function, 'date', run_date=dt, id=job_id)
    scheduled_jobs[job_id] = {
        "time": dt,
        "route": route,
        "emailData": email_data
    }

    return job_id
