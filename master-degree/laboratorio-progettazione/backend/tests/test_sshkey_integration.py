import pytest
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.sshkey import UserSSHKey
from backend.utils.hashing import get_password_hash, decrypt_password

@pytest.mark.integration
def test_add_sshkey_success(setup_database: Session, test_client):
    user = User(
        email="sshuser@example.com",
        hashed_password=get_password_hash("sshpassword"),
        passphrase="sshphrase",
        is_verified=True,
        verification_code="SSH123"
    )
    setup_database.add(user)
    setup_database.commit()

    response = test_client.post("/api/sshkeys/add", json={
        "id_user": user.id,
        "name": "My SSH Key",
        "private_key": "PRIVATE_KEY_DATA",
        "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA7Q== user@host",
        "passphrase": "securepassphrase",
        "notes": "This is my SSH key"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "SSH key saved successfully"

    saved_key = setup_database.query(UserSSHKey).filter_by(id_user=user.id).first()
    assert saved_key is not None
    assert saved_key.name == "My SSH Key"
    assert decrypt_password(saved_key.encrypted_private_key) == "PRIVATE_KEY_DATA"
    assert decrypt_password(saved_key.encrypted_public_key) == "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA7Q== user@host"
    assert decrypt_password(saved_key.encrypted_passphrase) == "securepassphrase"
    assert decrypt_password(saved_key.encrypted_notes) == "This is my SSH key"

@pytest.mark.integration
def test_add_sshkey_user_not_found(setup_database: Session, test_client):
    response = test_client.post("/api/sshkeys/add", json={
        "id_user": 9999,
        "name": "Ghost Key",
        "private_key": "PRIVATE_KEY_DATA",
        "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA7Q== ghost@nowhere",
        "passphrase": "nopass",
        "notes": "Should not work"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.integration
def test_fetch_sshkeys_for_user(setup_database: Session, test_client):
    user = User(
        email="sshreader@example.com",
        hashed_password=get_password_hash("readsshpass"),
        passphrase="sshphrasefetch",
        is_verified=True,
        verification_code="FETCH123"
    )
    setup_database.add(user)
    setup_database.commit()

    test_client.post("/api/sshkeys/add", json={
        "id_user": user.id,
        "name": "ReadMyKey",
        "private_key": "PRIVATE_READ_KEY",
        "public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGZvb2JhcnpAZXhhbXBsZS5jb20= reader@host",
        "passphrase": "readerpass",
        "notes": "just a test"
    })

    response = test_client.get(f"/api/sshkeys/{user.id}")
    assert response.status_code == 200

    sshkeys = response.json()
    assert isinstance(sshkeys, list)

    matching = [k for k in sshkeys if k["name"] == "ReadMyKey"]
    assert len(matching) >= 1
    key = matching[-1]
    assert isinstance(key["private_key"], str)
    assert isinstance(key["public_key"], str)
    assert isinstance(key["passphrase"], str)
    assert isinstance(key["notes"], str)

@pytest.mark.integration
def test_get_decrypted_sshkeys(setup_database: Session, test_client):
    # Create and add user
    user = User(
        email="decryptssh@example.com",
        hashed_password=get_password_hash("mypassword"),
        passphrase="decryptionpass",
        is_verified=True,
        verification_code="KEY321"
    )
    setup_database.add(user)
    setup_database.commit()

    # Log in to establish session
    login_response = test_client.post("/api/login", json={
        "email": "decryptssh@example.com",
        "password": "mypassword"
    })
    assert login_response.status_code == 200

    # Add SSH key
    test_client.post("/api/sshkeys/add", json={
        "id_user": user.id,
        "name": "Session Key",
        "private_key": "PRIVATE_KEY_123",
        "public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGZvb2JhcnpAZXhhbXBsZS5jb20= reader@host",
        "passphrase": "passphrase123",
        "notes": "session note"
    })

    # Fetch decrypted SSH keys
    response = test_client.get("/api/sshkeys/decrypted")
    assert response.status_code == 200

    keys = response.json()
    assert isinstance(keys, list)
    assert len(keys) >= 1

    matching = [k for k in keys if k["name"] == "Session Key"]
    assert len(matching) >= 1
    key = matching[0]
    assert key["private_key"] == "PRIVATE_KEY_123"
    assert key["public_key"] == "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGZvb2JhcnpAZXhhbXBsZS5jb20= reader@host"
    assert key["passphrase"] == "passphrase123"
    assert key["notes"] == "session note"
