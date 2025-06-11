import pytest
from pydantic import ValidationError
from backend.schemas.credential import CredentialUpdate

@pytest.mark.unit
def test_credential_update_valid():
    update = CredentialUpdate(url="https://example.com", username="newuser", password="newpass", notes="new notes")
    assert update.url == "https://example.com"
    assert update.username == "newuser"
    assert update.password == "newpass"
    assert update.notes == "new notes"

@pytest.mark.unit
def test_credential_update_invalid_url():
    with pytest.raises(ValidationError):
        CredentialUpdate(url="invalid-url")