import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.session import SessionLocal
from backend.models.user import User
from backend.utils.two_factor_auth import pyotp

client = TestClient(app)

@pytest.fixture
def test_user():
    db = SessionLocal()
    email = "2fauser@example.com"
    password = "testpassword"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            hashed_password=password,
            passphrase="testpassphrase",
            is_verified=True,
            verification_code="ABC123"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    yield user
    db.close()

def override_get_current_user():
    return {
        "id": 1,
        "two_factor_secret": None
    }

def test_enable_2fa_and_verify(test_user):
    from backend.utils.session import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {
        "id": test_user.id,
        "two_factor_secret": test_user.two_factor_secret
    }

    response = client.post("/api/enable-2fa")
    assert response.status_code == 200
    data = response.json()
    assert "manualCode" in data
    secret = data["manualCode"]

    totp = pyotp.TOTP(secret)
    otp = totp.now()

    response = client.post("/api/enable-2fa-verify", json={"otp": otp, "secret": secret})
    assert response.status_code == 200
    assert response.json()["message"] == "2FA enabled"

    app.dependency_overrides = {}