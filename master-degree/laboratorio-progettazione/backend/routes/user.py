from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from faker import Faker
from backend.db.session import SessionLocal
from backend.schemas.user import UserCreate
from backend.utils.passphrase import generate_passphrase
from backend.models.user import User
from backend.utils.verificationcode import generate_verification_code
from backend.models.verify_user import VerifyRequest
from backend.models.resend_code import ResendCodeRequest
from backend.models.login import LoginRequest
from backend.utils.email import send_email, generate_verification_email
from backend.utils.session import create_session, get_current_user, logout_user
from backend.models.credential import UserCredential
from backend.utils.hashing import encrypt_text, decrypt_password, get_password_hash, verify_password

router = APIRouter()

fake = Faker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    passphrase = generate_passphrase()
    verification_code = generate_verification_code()
    new_user = User(email=user.email,
                    hashed_password=hashed_password,
                    passphrase=passphrase,
                    verification_code=verification_code,
                    two_factor_secret=None)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    email_body = generate_verification_email(user.email, verification_code)
    send_email(to=user.email, subject="Your PassGuard Verification Code", body=email_body)

    return {"message": "Verification code sent"}

@router.post("/api/resend-code")
def resend_code(request: ResendCodeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    verification_code = generate_verification_code()
    user.verification_code = verification_code
    db.commit()

    email_body = generate_verification_email(request.email, verification_code)
    send_email(to=request.email, subject="Your PassGuard Verification Code", body=email_body)

    return {"message": "Verification code resent"}

@router.post("/api/verify")
def verify_user(request: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.verification_code != request.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully", "passphrase": user.passphrase}


@router.post("/api/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    if user.two_factor_secret:
        return {"message": "OTP required", "otp_required": True, "email": user.email}

    return create_session(user.id)

@router.get("/api/me")
def read_users_me(request: Request):
    current_user = get_current_user(request)
    return current_user

@router.post("/api/logout")
def logout():
    return logout_user()

@router.post("/api/change-password")
def change_password(request: Request, data: dict, db: Session = Depends(get_db)):
    """
    Change the user's main password:
    - Verify the old password
    - Decrypt all credentials
    - Encrypt again all the credentials with the new password
    - Update the password hash
    """
    current_user = get_current_user(request)
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    # Verify the old password
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Decrypt and encrypt again all the credentials
    credentials = db.query(UserCredential).filter(UserCredential.id_user == user.id).all()
    for cred in credentials:
        username = decrypt_password(cred.encrypted_username)
        password = decrypt_password(cred.encrypted_password)
        notes = decrypt_password(cred.encrypted_notes) if cred.encrypted_notes else ""
        cred.encrypted_username = encrypt_text(username)
        cred.encrypted_password = encrypt_text(password)
        cred.encrypted_notes = encrypt_text(notes) if notes else None

    # Update the password hash
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return {"message": "Password changed successfully"}


@router.delete("/api/delete-account", status_code=200)
def delete_account(request: Request, db: Session = Depends(get_db)):
    """
    It deletes the authenticated user's account and all its saved credentials.
    """
    current_user = get_current_user(request)
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    # Delete all credentials associated with the user
    db.query(UserCredential).filter(UserCredential.id_user == user.id).delete()

    # Delete user
    db.delete(user)
    db.commit()

    return {"message": f"L'account '{user.email}' has been permanently deleted."}
