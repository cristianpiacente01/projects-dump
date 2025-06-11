from pydantic import BaseModel, EmailStr

class LoginOTPRequest(BaseModel):
    email: EmailStr
    otp: str