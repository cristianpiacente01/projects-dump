"""
This module contains integration tests for user registration.
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.models.user import User

@pytest.mark.integration
def test_register_user_success(setup_database: Session, test_client):
    response = test_client.post("/api/register", json={
        "email": "test@example.com",
        "confirm_email": "test@example.com",
        "password": "testpassword",
        "confirm_password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Verification code sent"

@pytest.mark.integration
def test_register_user_email_already_registered(setup_database: Session, test_client):
    # Pre-insert a user with the same email
    user = User(email="test@example.com", hashed_password="hashedpassword", passphrase="passphrase", is_verified=True, verification_code="123456")
    try:
        setup_database.add(user)
        setup_database.commit()
    except IntegrityError:
        setup_database.rollback()

    response = test_client.post("/api/register", json={
        "email": "test@example.com",
        "confirm_email": "test@example.com",
        "password": "testpassword",
        "confirm_password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"