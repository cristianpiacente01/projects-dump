import pyotp
import qrcode
import base64
from io import BytesIO

def generate_2fa_secret():
    """Generate a new 2FA secret."""
    return pyotp.random_base32()

def generate_qr_code(secret, email, issuer_name="PassGuard"):
    """Generate a QR code for the 2FA secret."""
    totp = pyotp.TOTP(secret)
    qr_code_url = totp.provisioning_uri(email, issuer_name=issuer_name)
    qr = qrcode.make(qr_code_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def verify_otp_code(otp, secret):
    """Verify the OTP code against the secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)