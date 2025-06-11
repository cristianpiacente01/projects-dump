import pytest
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.sshkey import UserSSHKey
from backend.utils.hashing import get_password_hash, encrypt_text

@pytest.mark.integration
def test_update_sshkey_success(setup_database: Session, test_client):
    user = User(
        email="sshuser@example.com",
        hashed_password=get_password_hash("securepass"),
        passphrase="securephrase",
        is_verified=True,
        verification_code="654321"
    )
    setup_database.add(user)
    setup_database.commit()

    sshkey = UserSSHKey(
        id_user=user.id,
        name="Old Key",
        encrypted_private_key=encrypt_text("old_private_key"),
        encrypted_public_key=encrypt_text("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCold"),
        encrypted_passphrase=encrypt_text("old_passphrase"),
        encrypted_notes=encrypt_text("old notes")
    )
    setup_database.add(sshkey)
    setup_database.commit()

    response = test_client.put(f"/api/sshkeys/{sshkey.id_sshkey}", json={
        "name": "Updated Key",
        "private_key": "new_private_key",
        "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCnewvalidkey==",
        "passphrase": "new_passphrase",
        "notes": "updated notes"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "SSH key updated successfully"

    setup_database.refresh(sshkey)
    updated_key = setup_database.query(UserSSHKey).filter_by(id_sshkey=sshkey.id_sshkey).first()

    assert updated_key.name == "Updated Key"
    assert updated_key.encrypted_private_key != encrypt_text("old_private_key")
    assert updated_key.encrypted_notes != encrypt_text("old notes")
    assert updated_key.encrypted_public_key != encrypt_text("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCold")

@pytest.mark.integration
def test_update_sshkey_not_found(setup_database: Session, test_client):
    response = test_client.put("/api/sshkeys/9999", json={
        "name": "Doesn't matter",
        "private_key": "irrelevant",
        "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAnotfoundbutvalidformat==",
        "passphrase": "",
        "notes": ""
    })

    assert response.status_code == 404
    assert response.json()["detail"] == "SSH key not found"