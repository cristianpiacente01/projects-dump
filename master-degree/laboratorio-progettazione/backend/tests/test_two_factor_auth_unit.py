import pytest
from backend.utils import two_factor_auth

def test_generate_2fa_secret_length():
    secret = two_factor_auth.generate_2fa_secret()
    assert isinstance(secret, str)
    assert len(secret) >= 16

def test_generate_qr_code_returns_base64():
    secret = two_factor_auth.generate_2fa_secret()
    email = "test@example.com"
    qr_code = two_factor_auth.generate_qr_code(secret, email)
    assert isinstance(qr_code, str)
    assert len(qr_code) > 100

def test_verify_otp_code_valid(monkeypatch):
    secret = two_factor_auth.generate_2fa_secret()
    totp = two_factor_auth.pyotp.TOTP(secret)
    otp = totp.now()
    assert two_factor_auth.verify_otp_code(otp, secret) is True

def test_verify_otp_code_invalid():
    secret = two_factor_auth.generate_2fa_secret()
    invalid_otp = "000000"
    assert two_factor_auth.verify_otp_code(invalid_otp, secret) is False
