from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scheduler import schedule_email
from models import SchedulePayload
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

valid_routes = {"/send", "/send-batch", "/custom-mail"}


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/{route}")
async def handle_schedule(route: str, payload: SchedulePayload, request: Request):
    path = f"/{route.strip()}"
    if path not in valid_routes:
        raise HTTPException(status_code=400, detail="Invalid route")

    try:
        job_id = schedule_email(payload.time, path, payload.emailData)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ISO date format")

    return {"status": "Scheduled", "job_id": job_id}


# For local dev and Render compatibility
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
