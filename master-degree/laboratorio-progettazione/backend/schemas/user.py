"""
This module defines the schemas for user-related operations.
"""

from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    confirm_email: EmailStr
    password: str
    confirm_password: str

    @field_validator("email")
    @classmethod
    def email_is_valid(cls, v):
        """Validate that the email is from a valid domain."""
        valid_domains = ["gmail", "yahoo", "hotmail", "outlook", "proton", "duck", "example"]
        if not any(domain in v for domain in valid_domains):
            raise ValueError("Email must be from a valid domain")
        return v

    @field_validator("password")
    @classmethod
    def password_is_valid(cls, v):
        """Validate that the password is at least 8 characters long."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("confirm_email")
    @classmethod
    def emails_match(cls, v, values):
        """Validate that the email and confirm email fields match."""
        if "email" in values.data and v != values.data["email"]:
            raise ValueError("Emails do not match")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, values):
        """Validate that the password and confirm password fields match."""
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v
