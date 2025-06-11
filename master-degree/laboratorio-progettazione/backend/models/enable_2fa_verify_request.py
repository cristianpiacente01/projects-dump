from pydantic import BaseModel

class Enable2FAVerifyRequest(BaseModel):
    otp: str
    secret: str