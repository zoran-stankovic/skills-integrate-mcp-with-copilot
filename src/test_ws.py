import pytest
from fastapi.testclient import TestClient
from src.app import app, manager
import asyncio

client = TestClient(app)

def test_websocket_broadcast():
    """
    Test that a signup event is broadcasted to connected WebSocket clients.
    """
    with client.websocket_connect("/ws") as websocket:
        # Perform a signup via REST API
        # Use a fresh email to avoid "already signed up" error
        email = "test_ws@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Receive the message from WebSocket
        data = websocket.receive_json()
        
        assert data["type"] == "signup"
        assert data["activity"] == activity
        assert data["email"] == email
        assert "participants_count" in data

def test_activity_creation_broadcast():
    """
    Test that an activity creation event is broadcasted.
    """
    with client.websocket_connect("/ws") as websocket:
        name = "New Test Activity"
        response = client.post(f"/activities?name={name}&description=Test&schedule=None&max_participants=10")
        assert response.status_code == 200
        
        data = websocket.receive_json()
        assert data["type"] == "activity_created"
        assert data["name"] == name

def test_activity_update_broadcast():
    """
    Test that an activity update event is broadcasted.
    """
    with client.websocket_connect("/ws") as websocket:
        activity = "Gym Class"
        new_desc = "Updated Gym Description"
        response = client.patch(f"/activities/{activity}?description={new_desc}")
        assert response.status_code == 200
        
        data = websocket.receive_json()
        assert data["type"] == "activity_updated"
        assert data["name"] == activity
        assert data["details"]["description"] == new_desc
