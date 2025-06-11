import pytest
from backend.utils.hashing import get_password_hash, verify_password, encrypt_text, decrypt_password

def test_encrypt_and_decrypt_text():
    text = "mysecret"
    encrypted = encrypt_text(text)
    decrypted = decrypt_password(encrypted)
    assert decrypted == text

def test_get_password_hash_and_verify():
    password = "StrongPassword123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)

def test_decrypt_wrong_data():
    with pytest.raises(Exception):
        decrypt_password(b"notavalidciphertext")
