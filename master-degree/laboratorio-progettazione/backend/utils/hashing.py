"""
This module provides functions for hashing and encrypting passwords.
"""

import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from nacl.secret import SecretBox
from nacl.utils import random
from dotenv import load_dotenv

load_dotenv()

ph = PasswordHasher()
key = bytes.fromhex(os.getenv("SECRET_KEY"))

def encrypt_text(text):
    """Encrypt the text using a secret key."""
    box = SecretBox(key)
    nonce = random(SecretBox.NONCE_SIZE)
    return box.encrypt(text.encode(), nonce)

def get_password_hash(password):
    """Hash the password and encrypt the hash."""
    hashed_password = ph.hash(password)
    return encrypt_text(hashed_password)

def decrypt_password(encrypted_password):
    """Decrypt the encrypted password using the secret key."""
    box = SecretBox(key)
    decrypted_password = box.decrypt(encrypted_password)
    return decrypted_password.decode()

def verify_password(password, encrypted_password):
    if isinstance(encrypted_password, str):
        encrypted_password = bytes.fromhex(encrypted_password)
    try:
        decrypted_password = decrypt_password(encrypted_password)
        ph.verify(decrypted_password, password)
        return True
    except VerifyMismatchError:
        return False

def set_new_password(password):
    """Hash and encrypt a new password for storage."""
    return get_password_hash(password)
