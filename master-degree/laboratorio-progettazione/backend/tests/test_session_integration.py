import pytest
from sqlalchemy.orm import Session
from backend.tests.conftest import create_verified_user, login_user

@pytest.mark.integration
def test_login_creates_session(setup_database: Session, test_client):
    create_verified_user(setup_database, "test@example.com", "testpassword")

    response = login_user(test_client, "test@example.com", "testpassword")

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.cookies.get("session") is not None

@pytest.mark.integration
def test_get_current_user(setup_database: Session, test_client):
    create_verified_user(setup_database, "test@example.com", "testpassword")

    login_response = login_user(test_client, "test@example.com", "testpassword")

    assert login_response.status_code == 200
    session_cookie = login_response.cookies.get("session")

    test_client.cookies.set("session", session_cookie)
    response = test_client.get("/api/me")

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"