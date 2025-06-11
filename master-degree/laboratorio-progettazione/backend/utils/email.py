"""
This module provides functions for generating and sending verification emails.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

def generate_verification_email(recipient_email, verification_code):
    """Generate the HTML content for the verification email."""
    return f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #007bb8;">Welcome to PassGuard!</h2>
            <p>Dear {recipient_email},</p>
            <p>Thank you for registering with PassGuard. To complete your registration, please use the following verification code:</p>
            <h3 style="color: #007bb8;">{verification_code}</h3>
            <p>If you did not request this code, please ignore this email.</p>
            <p>Best regards,<br>PassGuard Team</p>
        </div>
    </body>
    </html>
    """

def send_email(to: EmailStr, subject: str, body: str):
    """Send an email with the specified subject and body to the given recipient."""
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # Use 'html' instead of 'plain'
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to, text)
        server.quit()
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
