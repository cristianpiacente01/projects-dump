"""
This module defines the request model for resending a verification code.
"""

from pydantic import BaseModel, EmailStr

class ResendCodeRequest(BaseModel):
    """Model for resend code request containing the user's email."""
    email: EmailStr
