import pytest
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.utils.hashing import get_password_hash, encrypt_text, decrypt_password
from backend.models.credential import UserCredential

@pytest.mark.integration
def test_add_credential_success(setup_database: Session, test_client):
    user = User(
        email="user@example.com",
        hashed_password=get_password_hash("securepass"),
        passphrase="userpassphrase",
        is_verified=True,
        verification_code="ABC123"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post("/api/credentials/add", json={
        "id_user": user.id,
        "url": "https://example.com",
        "username": "testuser",
        "password": "testpass123",
        "notes": "My secure login"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Credential saved successfully"

    saved_cred = setup_database.query(UserCredential).filter_by(id_user=user.id).first()
    assert saved_cred is not None
    assert saved_cred.url == "https://example.com"
    assert decrypt_password(saved_cred.encrypted_username) == "testuser"
    assert decrypt_password(saved_cred.encrypted_password) == "testpass123"
    assert decrypt_password(saved_cred.encrypted_notes) == "My secure login"


@pytest.mark.integration
def test_add_credential_user_not_found(setup_database: Session, test_client):
    response = test_client.post("/api/credentials/add", json={
        "id_user": 9999,
        "url": "https://example.com",
        "username": "ghost",
        "password": "nopass",
        "notes": "invisible"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.integration
def test_fetch_credentials_for_user(setup_database: Session, test_client):
    user = User(
        email="vaultuser@example.com",
        hashed_password=get_password_hash("vaultpass"),
        passphrase="vaultphrase",
        is_verified=True,
        verification_code="DEF456"
    )
    setup_database.add(user)
    setup_database.commit()

    test_client.post("/api/credentials/add", json={
        "id_user": user.id,
        "url": "https://testsite.com",
        "username": "vaultuser",
        "password": "vaultpass123",
        "notes": "test notes"
    })

    response = test_client.get(f"/api/credentials/{user.id}")
    assert response.status_code == 200

    credentials = response.json()
    assert isinstance(credentials, list)

    # Find the one we just added
    matching = [cred for cred in credentials if cred["url"] == "https://testsite.com"]
    assert len(matching) >= 1
    cred = matching[-1]
    assert isinstance(cred["username"], str)
    assert isinstance(cred["password"], str)
    assert isinstance(cred["notes"], str)


@pytest.mark.integration
def test_get_decrypted_credentials(setup_database: Session, test_client):
    # Create and add user
    user = User(
        email="decryptme@example.com",
        hashed_password=get_password_hash("letmein"),
        passphrase="passphrase123",
        is_verified=True,
        verification_code="XYZ789"
    )
    setup_database.add(user)
    setup_database.commit()

    # Log in to establish session
    login_response = test_client.post("/api/login", json={
        "email": "decryptme@example.com",
        "password": "letmein"
    })
    assert login_response.status_code == 200

    # Add credentials
    add_response = test_client.post("/api/credentials/add", json={
        "id_user": user.id,
        "url": "https://unique-testsite.com",
        "username": "decrypted_user",
        "password": "decrypted_pass",
        "notes": "decrypted notes"
    })
    assert add_response.status_code == 200

    # Fetch decrypted credentials
    decrypted_response = test_client.get("/api/credentials/decrypted")
    assert decrypted_response.status_code == 200

    credentials = decrypted_response.json()
    assert isinstance(credentials, list)
    assert len(credentials) >= 1

    matching = [cred for cred in credentials if cred["url"] == "https://unique-testsite.com"]
    assert len(matching) >= 1
    cred = matching[-1]
    assert cred["username"] == "decrypted_user"
    assert cred["password"] == "decrypted_pass"
    assert cred["notes"] == "decrypted notes"