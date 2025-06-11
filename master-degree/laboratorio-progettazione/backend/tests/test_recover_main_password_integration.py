import pytest
from backend.models.user import User
from backend.utils.hashing import get_password_hash

@pytest.mark.integration
def test_verify_passphrase_success(setup_database, test_client):
    user = User(
        email="integration@example.com",
        hashed_password=get_password_hash("Integration123!"),
        passphrase="integrationpass",
        is_verified=True,
        verification_code="654321"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post(
        "/api/recover/verify-passphrase",
        json={"email": "integration@example.com", "passphrase": "integrationpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user.id
    assert data["email"] == "integration@example.com"

@pytest.mark.integration
def test_verify_passphrase_invalid(setup_database, test_client):
    response = test_client.post(
        "/api/recover/verify-passphrase",
        json={"email": "notfound@example.com", "passphrase": "wrong"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid email or passphrase"

@pytest.mark.integration
def test_verify_passphrase_missing_fields(test_client):
    response = test_client.post(
        "/api/recover/verify-passphrase",
        json={"email": "missing@example.com"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email and passphrase required"

@pytest.mark.integration
def test_reset_password_success(setup_database, test_client):
    user = User(
        email="resetme@example.com",
        hashed_password=get_password_hash("OldPass123!"),
        passphrase="resetpass",
        is_verified=True,
        verification_code="111222"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post(
        "/api/recover/reset-password",
        json={"user_id": user.id, "new_password": "NewSecurePass!456"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Password reset successful"
    assert isinstance(data["new_passphrase"], str)
    # Verifica che la passphrase sia aggiornata nel DB
    setup_database.refresh(user)
    assert user.passphrase == data["new_passphrase"]

@pytest.mark.integration
def test_reset_password_user_not_found(test_client):
    response = test_client.post(
        "/api/recover/reset-password",
        json={"user_id": 999999, "new_password": "irrelevant"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.integration
def test_reset_password_missing_fields(test_client):
    response = test_client.post(
        "/api/recover/reset-password",
        json={"user_id": 1}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Missing data"

