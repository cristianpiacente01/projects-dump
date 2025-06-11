"""
This module contains unit tests for email verification.
"""

import pytest

@pytest.mark.unit
def test_register_user_invalid_data(test_client):
    response = test_client.post("/api/register", json={
        "email": "invalid-email",
        "confirm_email": "invalid-email",
        "password": "short",
        "confirm_password": "short"
    })
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.unit
def test_register_user_emails_do_not_match(test_client):
    response = test_client.post("/api/register", json={
        "email": "test@example.com",
        "confirm_email": "different@example.com",
        "password": "testpassword",
        "confirm_password": "testpassword"
    })
    assert response.status_code == 422  # Unprocessable Entity
    assert any("Emails do not match" in error["msg"] for error in response.json()["detail"])

@pytest.mark.unit
def test_register_user_passwords_do_not_match(test_client):
    response = test_client.post("/api/register", json={
        "email": "test@example.com",
        "confirm_email": "test@example.com",
        "password": "testpassword",
        "confirm_password": "differentpassword"
    })
    assert response.status_code == 422  # Unprocessable Entity
    assert any("Passwords do not match" in error["msg"] for error in response.json()["detail"])
