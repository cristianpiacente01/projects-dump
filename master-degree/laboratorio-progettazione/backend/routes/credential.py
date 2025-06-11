from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from base64 import b64encode

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.models.credential import UserCredential
from backend.schemas.credential import CredentialCreate, CredentialPreview, DecryptedCredential, CredentialUpdate
from backend.utils.hashing import encrypt_text, decrypt_password
from backend.utils.session import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/credentials/add")
def add_credential(cred: CredentialCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == cred.id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_credential = UserCredential(
        id_user=cred.id_user,
        url=cred.url,
        encrypted_username=encrypt_text(cred.username),
        encrypted_password=encrypt_text(cred.password),
        encrypted_notes=encrypt_text(cred.notes)
    )

    db.add(new_credential)
    db.commit()
    return {"message": "Credential saved successfully"}



@router.get("/api/credentials/decrypted", response_model=List[DecryptedCredential])
def get_decrypted_credentials(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request)
    creds = db.query(UserCredential).filter_by(id_user=current_user["id"]).all()
    return [
        DecryptedCredential(
            id_credential=c.id_credential,
            url=c.url,
            username=decrypt_password(c.encrypted_username),
            password=decrypt_password(c.encrypted_password),
            notes=decrypt_password(c.encrypted_notes),
        ) for c in creds
    ]


@router.get("/api/credentials/{id_user}", response_model=List[CredentialPreview])
def get_credentials(id_user: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    creds = db.query(UserCredential).filter(UserCredential.id_user == id_user).all()

    result = []
    for cred in creds:
        # Don't decrypt, but encode bytes to base64 to make them JSON serializable
        result.append({
            "id_credential": cred.id_credential,
            "url": cred.url,
            "username": b64encode(cred.encrypted_username).decode(),
            "password": b64encode(cred.encrypted_password).decode(),
            "notes": b64encode(cred.encrypted_notes).decode() if cred.encrypted_notes else ""
        })

    return result

@router.put("/api/credentials/{credential_id}")
def update_credential(credential_id: int, cred_update: CredentialUpdate, db: Session = Depends(get_db)):
    credential = db.query(UserCredential).filter(UserCredential.id_credential == credential_id).first()
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    if cred_update.url is not None:
        credential.url = cred_update.url
    if cred_update.username is not None:
        credential.encrypted_username = encrypt_text(cred_update.username)
    if cred_update.password is not None:
        credential.encrypted_password = encrypt_text(cred_update.password)
    if cred_update.notes is not None:
        credential.encrypted_notes = encrypt_text(cred_update.notes)

    db.commit()
    return {"message": "Credential updated successfully"}

@router.delete("/api/credentials/{credential_id}")
def delete_credential(credential_id: int, db: Session = Depends(get_db)):
    credential = db.query(UserCredential).filter(UserCredential.id_credential == credential_id).first()
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")

    db.delete(credential)
    db.commit()
    return {"message": "Credential deleted successfully"}