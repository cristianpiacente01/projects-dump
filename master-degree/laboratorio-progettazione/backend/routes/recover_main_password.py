from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db.session import SessionLocal
from backend.models.user import User
from backend.utils.hashing import set_new_password
from backend.utils.passphrase import generate_passphrase

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/recover/verify-passphrase")
def verify_passphrase(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    passphrase = data.get("passphrase")
    if not email or not passphrase:
        raise HTTPException(status_code=400, detail="Email and passphrase required")
    user = db.query(User).filter(User.email == email, User.passphrase == passphrase).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or passphrase")
    return {"user_id": user.id, "email": user.email}

@router.post("/api/recover/reset-password")
def reset_password(data: dict, db: Session = Depends(get_db)):
    user_id = data.get("user_id")
    new_password = data.get("new_password")
    if not user_id or not new_password:
        raise HTTPException(status_code=400, detail="Missing data")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = set_new_password(new_password)
    new_passphrase = generate_passphrase()
    user.passphrase = new_passphrase
    db.commit()
    return {"message": "Password reset successful", "new_passphrase": new_passphrase}
