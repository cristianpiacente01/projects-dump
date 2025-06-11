import pytest
from pydantic import ValidationError
from backend.schemas.sshkey import SSHKeyUpdate

@pytest.mark.unit
def test_sshkey_update_valid():
    valid_key = SSHKeyUpdate(
        name="Work Laptop Key",
        private_key="some_private_key_data",
        public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDl1c2VyQGV4YW1wbGUuY29t user@host",
        passphrase="optional",
        notes="Updated for integration testing"
    )
    assert valid_key.name == "Work Laptop Key"
    assert "ssh-ed25519" in valid_key.public_key


@pytest.mark.unit
def test_sshkey_update_invalid_public_key():
    with pytest.raises(ValidationError):
        SSHKeyUpdate(
            name="Bad SSH Key",
            private_key="data",
            public_key="not-ssh-format",
            passphrase="pass",
            notes=""
        )
