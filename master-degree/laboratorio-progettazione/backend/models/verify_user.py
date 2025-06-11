"""
This module defines the request model for verifying a user.
"""

from pydantic import BaseModel, EmailStr

class VerifyRequest(BaseModel):
    """Model for verify request containing the user's email and verification code."""
    email: EmailStr
    code: str
