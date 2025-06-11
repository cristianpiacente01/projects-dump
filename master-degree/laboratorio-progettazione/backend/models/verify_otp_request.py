from pydantic import BaseModel
from typing import Optional


class VerifyOTPRequest(BaseModel):
    email: Optional[str] = None
    otp: str
    secret: Optional[str] = None