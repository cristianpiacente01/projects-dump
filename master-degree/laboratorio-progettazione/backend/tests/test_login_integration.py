import pytest
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.utils.hashing import get_password_hash

@pytest.mark.integration
def test_login_user_success(setup_database: Session, test_client):
    # Pre-insert a verified user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        passphrase="testpassphrase",
        is_verified=True,
        verification_code="123456"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post("/api/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

@pytest.mark.integration
def test_login_user_incorrect_password(setup_database: Session, test_client):
    # Pre-insert a verified user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        passphrase="testpassphrase",
        is_verified=True,
        verification_code="123456"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post("/api/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect password"

@pytest.mark.integration
def test_login_user_not_verified(setup_database: Session, test_client):
    # Pre-insert an unverified user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        passphrase="testpassphrase",
        is_verified=False,
        verification_code="123456"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post("/api/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "Email not verified"