import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.session import SessionLocal
from backend.models.user import User
from backend.models.credential import UserCredential
from backend.utils.hashing import get_password_hash, encrypt_text

client = TestClient(app)

@pytest.fixture
def test_db():
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture
def create_user(test_db):
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("oldpassword"),
        passphrase="test-passphrase",
        is_verified=True,
        verification_code="123456"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture
def create_credential(test_db, create_user):
    cred = UserCredential(
        id_user=create_user.id,
        url="https://example.com",
        encrypted_username=encrypt_text("testuser"),
        encrypted_password=encrypt_text("testpass"),
        encrypted_notes=encrypt_text("somenotes")
    )
    test_db.add(cred)
    test_db.commit()
    test_db.refresh(cred)
    return cred

@pytest.mark.integration
def login(client, email, password):
    response = client.post("/api/login", json={"email": email, "password": password})
    assert response.status_code == 200
    # Set cookies on the client instance
    for k, v in response.cookies.items():
        client.cookies.set(k, v)
    return client

@pytest.mark.integration
def test_change_password_success(test_db, create_user, create_credential):
    login(client, "testuser@example.com", "oldpassword")
    response = client.post(
        "/api/change-password",
        json={"old_password": "oldpassword", "new_password": "newpassword"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"

@pytest.mark.integration
def test_change_password_wrong_old(test_db, create_user):
    login(client, "testuser@example.com", "oldpassword")
    response = client.post(
        "/api/change-password",
        json={"old_password": "wrongpassword", "new_password": "newpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect old password"

@pytest.mark.integration
def test_change_password_requires_auth(test_db):
    response = client.post(
        "/api/change-password",
        json={"old_password": "oldpassword", "new_password": "newpassword"}
    )
    assert response.status_code in (401, 403)
