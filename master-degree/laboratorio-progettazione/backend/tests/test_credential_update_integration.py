import pytest
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.credential import UserCredential
from backend.utils.hashing import get_password_hash, encrypt_text

@pytest.mark.integration
def test_update_credential_success(setup_database: Session, test_client):
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("testpassword"),
        passphrase="testpassphrase",
        is_verified=True,
        verification_code="123456"
    )
    setup_database.add(user)
    setup_database.commit()

    credential = UserCredential(
        id_user=user.id,
        url="https://old-url.com",
        encrypted_username=encrypt_text("olduser"),
        encrypted_password=encrypt_text("oldpass"),
        encrypted_notes=encrypt_text("old notes")
    )
    setup_database.add(credential)
    setup_database.commit()

    response = test_client.put(f"/api/credentials/{credential.id_credential}", json={
        "url": "https://new-url.com",
        "username": "newuser",
        "password": "newpass",
        "notes": "new notes"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Credential updated successfully"

    setup_database.refresh(credential)
    updated_cred = setup_database.query(UserCredential).filter_by(id_credential=credential.id_credential).first()
    assert updated_cred.url == "https://new-url.com"
    assert updated_cred.encrypted_username != encrypt_text("olduser")
    assert updated_cred.encrypted_password != encrypt_text("oldpass")
    assert updated_cred.encrypted_notes != encrypt_text("old notes")

@pytest.mark.integration
def test_update_credential_not_found(setup_database: Session, test_client):
    response = test_client.put("/api/credentials/9999", json={
        "url": "https://new-url.com",
        "username": "newuser",
        "password": "newpass",
        "notes": "new notes"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "Credential not found"