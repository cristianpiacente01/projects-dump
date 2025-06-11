import pytest
from sqlalchemy.orm import Session
from backend.models.user import User


@pytest.mark.integration
def test_register_user_sends_email(test_client, setup_database: Session):
    setup_database.query(User).delete()
    setup_database.commit()

    response = test_client.post("/api/register", json={
        "email": "test@example.com",
        "confirm_email": "test@example.com",
        "password": "testpassword",
        "confirm_password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Verification code sent"