"""
Tests for the High School Management System API

Tests cover:
- GET /activities endpoint
- POST /activities/{activity_name}/signup endpoint
- DELETE /activities/{activity_name}/signup endpoint
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI application"""
    return TestClient(app)


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns the activities list"""
    # Arrange
    expected_activity_count = 9
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Debate Club",
        "Science Olympiad",
        "Drama Club",
        "Art Studio"
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    for activity_name in expected_activities:
        assert activity_name in activities


def test_signup_for_activity_success(client):
    """Test that a student can successfully sign up for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_for_activity_duplicate_rejected(client):
    """Test that signing up twice for the same activity is rejected"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_for_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_cancel_signup_success(client):
    """Test that a student can successfully cancel their signup"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_cancel_signup_for_nonexistent_activity_returns_404(client):
    """Test that canceling signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_cancel_signup_for_unregistered_participant_returns_404(client):
    """Test that canceling signup for non-registered participant returns 404"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"  # Not signed up

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()
