"""
This module defines the User model for the database.
"""

from sqlalchemy import Column, Integer, String, Boolean
from backend.db.base import Base

class User(Base):
    """Represents a user in the database."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    passphrase = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=False)
    two_factor_secret = Column(String, nullable=True)
