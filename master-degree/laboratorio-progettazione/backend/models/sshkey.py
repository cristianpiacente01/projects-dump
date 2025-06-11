from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.base import Base

class UserSSHKey(Base):
    """Represents a SSH key for a specific user."""
    __tablename__ = "users_sshkeys"

    id_sshkey = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    encrypted_private_key = Column(String, nullable=False)
    encrypted_public_key = Column(String, nullable=False)
    encrypted_passphrase = Column(String, nullable=False)
    encrypted_notes = Column(String, nullable=True)