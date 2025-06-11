from sqlalchemy import Column, Integer, String, ForeignKey
from backend.db.base import Base

class UserCredential(Base):
    """Represents a credential for a specific user."""
    __tablename__ = "users_credentials"

    id_credential = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    encrypted_username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    encrypted_notes = Column(String, nullable=True)