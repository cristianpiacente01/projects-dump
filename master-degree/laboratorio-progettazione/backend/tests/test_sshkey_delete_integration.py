import pytest
from backend.models.user import User
from backend.models.sshkey import UserSSHKey
from backend.utils.hashing import get_password_hash, encrypt_text

@pytest.mark.integration
def test_delete_sshkey_success(setup_database, test_client):
    user = User(
        email="delssh@example.com",
        hashed_password=get_password_hash("delpass"),
        passphrase="delphrase",
        is_verified=True,
        verification_code="DEL123"
    )
    setup_database.add(user)
    setup_database.commit()

    sshkey = UserSSHKey(
        id_user=user.id,
        name="KeyToDelete",
        encrypted_private_key=encrypt_text("private"),
        encrypted_public_key=encrypt_text("public"),
        encrypted_passphrase=encrypt_text("pass"),
        encrypted_notes=encrypt_text("notes")
    )
    setup_database.add(sshkey)
    setup_database.commit()

    login_response = test_client.post("/api/login", json={
        "email": "delssh@example.com",
        "password": "delpass"
    })
    assert login_response.status_code == 200

    response = test_client.delete(f"/api/sshkeys/{sshkey.id_sshkey}")
    assert response.status_code == 200
    assert response.json() == {"message": "SSH key deleted successfully"}

    assert setup_database.query(UserSSHKey).filter_by(id_sshkey=sshkey.id_sshkey).first() is None

@pytest.mark.integration
def test_delete_sshkey_not_found(setup_database, test_client):
    user = User(
        email="delnotfound@example.com",
        hashed_password=get_password_hash("delnotfoundpass"),
        passphrase="delnotfoundphrase",
        is_verified=True,
        verification_code="DELNF123"
    )
    setup_database.add(user)
    setup_database.commit()

    login_response = test_client.post("/api/login", json={
        "email": "delnotfound@example.com",
        "password": "delnotfoundpass"
    })
    assert login_response.status_code == 200

    response = test_client.delete("/api/sshkeys/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "SSH key not found or not authorized"
