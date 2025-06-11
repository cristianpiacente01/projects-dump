from pydantic import BaseModel, field_validator
import re

class CredentialCreate(BaseModel):
    id_user: int
    url: str
    username: str
    password: str
    notes: str = ""

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        url_pattern = re.compile(r"^https?://[\w\-\.]+(\.[\w\-]+)+[/#?]?.*$")
        if not url_pattern.match(v):
            raise ValueError("Invalid URL format. Must start with http:// or https://")
        return v

class CredentialPreview(BaseModel):
    id_credential: int
    url: str
    username: str  # encrypted
    password: str  # encrypted
    notes: str     # encrypted

class DecryptedCredential(BaseModel):
    id_credential: int
    url: str
    username: str  # decrypted
    password: str  # decrypted
    notes: str     # decrypted

class CredentialUpdate(BaseModel):
    url: str = None
    username: str = None
    password: str = None
    notes: str = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        if v is not None:
            url_pattern = re.compile(r"^https?://[\w\-\.]+(\.[\w\-]+)+[/#?]?.*$")
            if not url_pattern.match(v):
                raise ValueError("Invalid URL format. Must start with http:// or https://")
        return v