from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.models.enable_2fa_verify_request import Enable2FAVerifyRequest
from backend.models.login_otp_request import LoginOTPRequest
from backend.models.verify_otp_request import VerifyOTPRequest
from backend.utils.session import get_current_user, create_session
from backend.utils.two_factor_auth import generate_2fa_secret, generate_qr_code, verify_otp_code
from backend.models.user import User
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/enable-2fa")
def enable_2fa(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a new secret and QR code
    secret = generate_2fa_secret()
    qr_code_base64 = generate_qr_code(secret, user.email)

    return {"qrCode": qr_code_base64, "manualCode": secret}

@router.post("/api/disable-2fa")
def disable_2fa(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.two_factor_secret = None
    db.commit()

    return {"message": "Two-factor authentication disabled"}


@router.post("/api/login-otp")
def login_with_otp(request: LoginOTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not verify_otp_code(request.otp, user.two_factor_secret):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return create_session(user.id)


@router.post("/api/enable-2fa-verify")
def enable_2fa_verify(
    body: Enable2FAVerifyRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # body.otp e body.secret sono obbligatori
    if not body.otp or not body.secret:
        raise HTTPException(status_code=422, detail="OTP and secret are required")
    if not verify_otp_code(body.otp, body.secret):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    user = db.query(User).filter(User.id == current_user["id"]).first()
    user.two_factor_secret = body.secret
    db.commit()
    return {"message": "2FA enabled"}


@router.post("/api/verify-otp")
def verify_otp(
    request_body: VerifyOTPRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    def get_user_by_email_or_id(email=None, user_id=None):
        if email:
            return db.query(User).filter(User.email == email).first()
        if user_id:
            return db.query(User).filter(User.id == user_id).first()
        return None

    if request_body.secret:
        current_user = get_current_user(request)
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        user = get_user_by_email_or_id(user_id=current_user["id"])
        if not user or not verify_otp_code(request_body.otp, request_body.secret):
            raise HTTPException(status_code=400, detail="Invalid OTP")
        user.two_factor_secret = request_body.secret
        db.commit()
        return {"message": "2FA enabled"}

    if request_body.email:
        user = get_user_by_email_or_id(email=request_body.email)
        if not user or not user.two_factor_secret or not verify_otp_code(request_body.otp, user.two_factor_secret):
            raise HTTPException(status_code=400, detail="Invalid OTP or 2FA not enabled")
        return create_session(user.id)

    raise HTTPException(status_code=400, detail="Missing email or secret for OTP verification")


@router.get("/api/2fa-status")
def get_2fa_status(current_user: dict = Depends(get_current_user)):
    return {"enabled": bool(current_user["two_factor_secret"])}
