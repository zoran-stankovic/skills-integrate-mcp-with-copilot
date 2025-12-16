"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from sqlmodel import select

# DB
from db import init_db, seed_default_data, get_session, Activity, Participant

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

@app.on_event("startup")
def on_startup():
    # Initialize DB and seed default activities if needed
    init_db()
    seed_default_data()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """Return all activities with their details and participant emails"""
    with get_session() as session:
        activities = session.exec(select(Activity)).all()
        result = {}
        for a in activities:
            result[a.name] = {
                "description": a.description,
                "schedule": a.schedule,
                "max_participants": a.max_participants,
                "participants": [p.email for p in a.participants]
            }
        return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists and perform signup in DB
    with get_session() as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).one_or_none()
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Check if already signed up
        for p in activity.participants:
            if p.email == email:
                raise HTTPException(status_code=400, detail="Student is already signed up")

        # Check capacity
        if len(activity.participants) >= activity.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

        participant = Participant(email=email, activity_id=activity.id)
        session.add(participant)
        session.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists and remove student in DB
    with get_session() as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).one_or_none()
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Find participant
        participant = None
        for p in activity.participants:
            if p.email == email:
                participant = p
                break

        if participant is None:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        session.delete(participant)
        session.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
