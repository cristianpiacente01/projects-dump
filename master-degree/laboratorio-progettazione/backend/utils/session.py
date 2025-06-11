import base64
from itsdangerous import URLSafeTimedSerializer
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from backend.db.session import SessionLocal
from backend.models.user import User
import os

SECRET_KEY = os.getenv("SECRET_KEY")
SESSION_COOKIE_NAME = "session"

serializer = URLSafeTimedSerializer(SECRET_KEY)

def create_session(user_id: int):
    session_token = base64.urlsafe_b64encode(serializer.dumps(user_id).encode()).decode()
    response = JSONResponse(content={"access_token": session_token, "token_type": "bearer"})
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_token, httponly=True)
    return response

def get_current_user(request: Request):
    session_token = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        decoded_token = base64.urlsafe_b64decode(session_token.encode()).decode()
        user_id = serializer.loads(decoded_token, max_age=3600)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid session token") from exc
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # Convert any binary data to base64 string
    user_data = {
        "id": user.id,
        "email": user.email,
        "hashed_password": base64.b64encode(user.hashed_password).decode() if isinstance(user.hashed_password, bytes) else user.hashed_password,
        "passphrase": user.passphrase,
        "is_verified": user.is_verified,
        "verification_code": user.verification_code,
        "two_factor_secret": user.two_factor_secret
    }
    return user_data

def logout_user():
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return response