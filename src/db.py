from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    name: Optional[str] = None
    grade: Optional[int] = None
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id")
    activity: Optional["Activity"] = Relationship(back_populates="participants")


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    schedule: str
    max_participants: int
    participants: List[Participant] = Relationship(back_populates="activity")


import os

DATABASE_URL = "sqlite:///./activities.db"


def get_engine(database_url: str = None):
    database_url = database_url or os.environ.get("ACTIVITIES_DATABASE_URL") or DATABASE_URL
    return create_engine(database_url, connect_args={"check_same_thread": False})


def init_db(engine=None):
    engine = engine or get_engine()
    SQLModel.metadata.create_all(engine)


def get_session(engine=None):
    engine = engine or get_engine()
    return Session(engine)


def seed_default_data(engine=None):
    """Seed the database with the example activities if it's empty."""
    engine = engine or get_engine()
    with Session(engine) as session:
        result = session.exec(select(Activity))
        if result.first() is not None:
            return

        # Minimal seed copied from previous in-memory data
        defaults = [
            Activity(name="Chess Club", description="Learn strategies and compete in chess tournaments", schedule="Fridays, 3:30 PM - 5:00 PM", max_participants=12),
            Activity(name="Programming Class", description="Learn programming fundamentals and build software projects", schedule="Tuesdays and Thursdays, 3:30 PM - 4:30 PM", max_participants=20),
            Activity(name="Gym Class", description="Physical education and sports activities", schedule="Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM", max_participants=30),
            Activity(name="Soccer Team", description="Join the school soccer team and compete in matches", schedule="Tuesdays and Thursdays, 4:00 PM - 5:30 PM", max_participants=22),
            Activity(name="Basketball Team", description="Practice and play basketball with the school team", schedule="Wednesdays and Fridays, 3:30 PM - 5:00 PM", max_participants=15),
            Activity(name="Art Club", description="Explore your creativity through painting and drawing", schedule="Thursdays, 3:30 PM - 5:00 PM", max_participants=15),
            Activity(name="Drama Club", description="Act, direct, and produce plays and performances", schedule="Mondays and Wednesdays, 4:00 PM - 5:30 PM", max_participants=20),
            Activity(name="Math Club", description="Solve challenging problems and participate in math competitions", schedule="Tuesdays, 3:30 PM - 4:30 PM", max_participants=10),
            Activity(name="Debate Team", description="Develop public speaking and argumentation skills", schedule="Fridays, 4:00 PM - 5:30 PM", max_participants=12),
        ]

        session.add_all(defaults)
        session.commit()
