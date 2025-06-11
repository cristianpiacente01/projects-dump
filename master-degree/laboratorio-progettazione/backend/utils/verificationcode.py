"""
This module provides a function to generate a verification code.
"""

import secrets
import string

def generate_verification_code():
    """Generate a 6-character alphanumeric verification code."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))
