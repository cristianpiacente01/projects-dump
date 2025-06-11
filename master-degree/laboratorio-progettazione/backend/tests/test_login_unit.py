import pytest
from backend.models.login import LoginRequest
from pydantic import ValidationError

@pytest.mark.unit
def test_login_request_valid():
    request = LoginRequest(email="test@example.com", password="testpassword")
    assert request.email == "test@example.com"
    assert request.password == "testpassword"

@pytest.mark.unit
def test_login_request_invalid_email():
    with pytest.raises(ValidationError):
        LoginRequest(email="invalid-email", password="testpassword")

@pytest.mark.unit
def test_login_request_missing_password():
    with pytest.raises(ValidationError):
        LoginRequest(email="test@example.com")