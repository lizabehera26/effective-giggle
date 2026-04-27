"""
Integration tests for FastAPI endpoints using AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient


def test_root_redirect(client):
    """
    Test that GET / redirects to /static/index.html
    
    AAA Pattern:
    - Arrange: TestClient is ready (fixture)
    - Act: Send GET request to /
    - Assert: Verify redirect response with correct location
    """
    # Arrange
    # client fixture provides TestClient instance

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """
    Test that GET /activities returns all 3 activities with correct structure
    
    AAA Pattern:
    - Arrange: TestClient is ready (fixture)
    - Act: Send GET request to /activities
    - Assert: Verify status code, number of activities, and data structure
    """
    # Arrange
    # client fixture provides TestClient instance
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert set(data.keys()) == set(expected_activities)
    
    # Verify activity structure
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_signup_happy_path(client):
    """
    Test that POST /activities/{activity_name}/signup successfully adds email to participants
    
    AAA Pattern:
    - Arrange: TestClient ready, prepare signup data
    - Act: Send POST request to signup endpoint
    - Assert: Verify success response and email added to participants list
    """
    # Arrange
    activity_name = "Chess Club"
    test_email = "newstudent@mergington.edu"
    
    # Get initial participant count
    response_before = client.get("/activities")
    initial_participants = response_before.json()[activity_name]["participants"]
    initial_count = len(initial_participants)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert test_email in response.json()["message"]
    
    # Verify participant was actually added
    response_after = client.get("/activities")
    updated_participants = response_after.json()[activity_name]["participants"]
    assert len(updated_participants) == initial_count + 1
    assert test_email in updated_participants
