import pytest
from backend.utils.email import send_email

@pytest.mark.unit
def test_send_email(mocker):
    mock_smtp = mocker.patch("smtplib.SMTP")
    send_email("test@example.com", "Test Subject", "Test Body")

    mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
    mock_smtp.return_value.starttls.assert_called_once()
    mock_smtp.return_value.sendmail.assert_called_once()
    mock_smtp.return_value.quit.assert_called_once()