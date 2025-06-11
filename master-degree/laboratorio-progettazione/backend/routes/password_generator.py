from fastapi import APIRouter, Query
from backend.utils.generate_password import generate_password
from backend.utils.passphrase import generate_passphrase
from backend.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/api/generate-password")
def get_secure_password(
    length: int = Query(16, ge=12),
    uppercase: bool = Query(True),
    lowercase: bool = Query(True),
    numbers: bool = Query(True),
    symbols: bool = Query(True),
):
    password = generate_password(
        length=length,
        use_uppercase=uppercase,
        use_lowercase=lowercase,
        use_numbers=numbers,
        use_symbols=symbols
    )
    return {"password": password}

@router.get("/api/generate-passphrase")
def get_passphrase(
    words: int = Query(6, ge=4, le=10, description="Number of words in passphrase")
):
    passphrase = generate_passphrase(word_count=words)
    return {"passphrase": passphrase}