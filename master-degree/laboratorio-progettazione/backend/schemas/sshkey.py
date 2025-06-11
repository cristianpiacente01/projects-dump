from pydantic import BaseModel, field_validator
import re

class SSHKeyCreate(BaseModel):
    id_user: int
    name: str
    private_key: str
    public_key: str
    passphrase: str
    notes: str = ""

    @field_validator("public_key")
    @classmethod
    def validate_public_key(cls, v):
        # Empty string is ok
        if not v:
            return v
        
        # This regular expression validates an SSH public key in standard format:
        # - It must start with one of the supported prefixes: ssh-ed25519, ssh-rsa, ssh-dss, ssh-ecdsa
        # - Followed by a Base64-encoded string (the actual key)
        # - Optionally, it can include a comment like user@host
        ssh_pubkey_pattern = re.compile(
            r"^ssh-(ed25519|rsa|dss|ecdsa) "
            r"AAAA(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})"
            r"( [^@]+@[^@]+)?$"
        )
        if not ssh_pubkey_pattern.match(v.strip()):
            raise ValueError("Invalid SSH public key format")
        return v


class SSHKeyPreview(BaseModel):
    id_sshkey: int
    name: str
    private_key: str    # encrypted
    public_key: str     # encrypted
    passphrase: str     # encrypted
    notes: str          # encrypted


class DecryptedSSHKey(BaseModel):
    id_sshkey: int
    name: str
    private_key: str    # decrypted
    public_key: str     # decrypted
    passphrase: str     # decrypted
    notes: str          # decrypted


class SSHKeyUpdate(BaseModel):
    name: str = None
    private_key: str = None
    public_key: str = None
    passphrase: str = None
    notes: str = None

    @field_validator("public_key")
    @classmethod
    def validate_public_key(cls, v):
        if not v:
            return v
        
        ssh_pubkey_pattern = re.compile(
            r"^ssh-(ed25519|rsa|dss|ecdsa) "
            r"AAAA(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})"
            r"( [^@]+@[^@]+)?$"
        )
        if not ssh_pubkey_pattern.match(v.strip()):
            raise ValueError("Invalid SSH public key format")
        return v