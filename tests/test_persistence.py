import os
import shutil
import tempfile

from fastapi.testclient import TestClient


def setup_test_db(tmpdir):
    # Use a temporary DB file so we don't clobber the main DB
    db_path = os.path.join(tmpdir, "test_activities.db")
    return db_path


def test_seed_and_get_activities(tmp_path):
    # prepare isolated DB file
    db_file = setup_test_db(str(tmp_path))

    # Ensure src is on sys.path for imports
    import sys
    sys.path.insert(0, os.path.join(os.getcwd(), "src"))

    # Initialize DB and seed using the same file as the app will use
    from db import get_engine, init_db, seed_default_data, DATABASE_URL

    engine = get_engine(f"sqlite:///{db_file}")
    init_db(engine)
    seed_default_data(engine)

    # Ensure the app uses the same DB file
    import sys
    sys.path.insert(0, os.path.join(os.getcwd(), "src"))
    import os as _os
    _os.environ["ACTIVITIES_DATABASE_URL"] = f"sqlite:///{db_file}"

    from app import app

    # Run client against seeded DB
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_persistence(tmp_path):
    db_file = setup_test_db(str(tmp_path))

    from db import get_engine, init_db, seed_default_data

    engine = get_engine(f"sqlite:///{db_file}")
    init_db(engine)
    seed_default_data(engine)

    import sys
    sys.path.insert(0, os.path.join(os.getcwd(), "src"))
    import os as _os
    _os.environ["ACTIVITIES_DATABASE_URL"] = f"sqlite:///{db_file}"
    from app import app

    client = TestClient(app)

    # sign up a new student
    resp = client.post("/activities/Chess%20Club/signup?email=test_student@example.com")
    assert resp.status_code == 200

    # check the participant appears
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data = resp2.json()
    assert "test_student@example.com" in data["Chess Club"]["participants"]
