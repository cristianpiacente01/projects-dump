import pytest
from sqlalchemy.orm import Session
from backend.tests.conftest import create_verified_user, login_user

@pytest.mark.integration
def test_logout_user(setup_database: Session, test_client):
    create_verified_user(setup_database, "test@example.com", "testpassword")

    login_response = login_user(test_client, "test@example.com", "testpassword")
    assert login_response.status_code == 200

    session_cookie = login_response.cookies.get("session")
    test_client.cookies.set("session", session_cookie)

    logout_response = test_client.post("/api/logout")
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"
    assert 'session="";' in logout_response.headers.get("set-cookie")
    assert 'expires=' in logout_response.headers.get("set-cookie")