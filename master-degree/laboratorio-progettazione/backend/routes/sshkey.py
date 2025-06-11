from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from base64 import b64encode

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.models.sshkey import UserSSHKey
from backend.schemas.sshkey import SSHKeyCreate, SSHKeyPreview, DecryptedSSHKey, SSHKeyUpdate
from backend.utils.hashing import encrypt_text, decrypt_password
from backend.utils.session import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/sshkeys/add")
def add_sshkey(sshkey: SSHKeyCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == sshkey.id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_sshkey = UserSSHKey(
        id_user=sshkey.id_user,
        name=sshkey.name,
        encrypted_private_key=encrypt_text(sshkey.private_key),
        encrypted_public_key=encrypt_text(sshkey.public_key),
        encrypted_passphrase=encrypt_text(sshkey.passphrase),
        encrypted_notes=encrypt_text(sshkey.notes)
    )

    db.add(new_sshkey)
    db.commit()
    return {"message": "SSH key saved successfully"}



@router.get("/api/sshkeys/decrypted", response_model=List[DecryptedSSHKey])
def get_decrypted_sshkeys(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request)
    sshkeys = db.query(UserSSHKey).filter_by(id_user=current_user["id"]).all()
    return [
        DecryptedSSHKey(
            id_sshkey=k.id_sshkey,
            name=k.name,
            private_key=decrypt_password(k.encrypted_private_key),
            public_key=decrypt_password(k.encrypted_public_key),
            passphrase=decrypt_password(k.encrypted_passphrase),
            notes=decrypt_password(k.encrypted_notes),
        ) for k in sshkeys
    ]


@router.get("/api/sshkeys/{id_user}", response_model=List[SSHKeyPreview])
def get_sshkeys(id_user: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sshkeys = db.query(UserSSHKey).filter(UserSSHKey.id_user == id_user).all()

    result = []
    for sshkey in sshkeys:
        # Don't decrypt, but encode bytes to base64 to make them JSON serializable
        result.append({
            "id_sshkey": sshkey.id_sshkey,
            "name": sshkey.name,
            "private_key": b64encode(sshkey.encrypted_private_key).decode(),
            "public_key": b64encode(sshkey.encrypted_public_key).decode() if sshkey.encrypted_public_key else "",
            "passphrase": b64encode(sshkey.encrypted_passphrase).decode() if sshkey.encrypted_passphrase else "",
            "notes": b64encode(sshkey.encrypted_notes).decode() if sshkey.encrypted_notes else ""
        })

    return result


@router.put("/api/sshkeys/{sshkey_id}")
def update_sshkey(sshkey_id: int, sshkey_update: SSHKeyUpdate, db: Session = Depends(get_db)):
    sshkey = db.query(UserSSHKey).filter(UserSSHKey.id_sshkey == sshkey_id).first()
    if not sshkey:
        raise HTTPException(status_code=404, detail="SSH key not found")

    if sshkey_update.name is not None:
        sshkey.name = sshkey_update.name
    if sshkey_update.private_key is not None:
        sshkey.encrypted_private_key = encrypt_text(sshkey_update.private_key)
    if sshkey_update.public_key is not None:
        sshkey.encrypted_public_key = encrypt_text(sshkey_update.public_key)
    if sshkey_update.passphrase is not None:
        sshkey.encrypted_passphrase = encrypt_text(sshkey_update.passphrase)
    if sshkey_update.notes is not None:
        sshkey.encrypted_notes = encrypt_text(sshkey_update.notes)

    db.commit()
    return {"message": "SSH key updated successfully"}


@router.delete("/api/sshkeys/{id_sshkey}")
def delete_sshkey(id_sshkey: int, db: Session = Depends(get_db), request: Request = None):
    current_user = get_current_user(request)
    sshkey = db.query(UserSSHKey).filter_by(id_sshkey=id_sshkey, id_user=current_user["id"]).first()
    if not sshkey:
        raise HTTPException(status_code=404, detail="SSH key not found or not authorized")

    db.delete(sshkey)
    db.commit()
    return {"message": "SSH key deleted successfully"}