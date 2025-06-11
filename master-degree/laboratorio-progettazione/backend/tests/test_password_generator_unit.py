#test_password_generator


import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.credential import UserCredential
from backend.routes.credential import delete_credential

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.mark.unit
def test_delete_credential_existing(db_session):
    # Mock credential
    credential = UserCredential(id_credential=1, id_user=123, url="http://example.com", encrypted_username="user", encrypted_password="pass")

    # Mock DB behavior
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = credential
    query_mock.filter.return_value = filter_mock
    db_session.query.return_value = query_mock

    db_session.delete = MagicMock()
    db_session.commit = MagicMock()

    # Execute function
    response = delete_credential(credential_id=1, db=db_session)

    # Assertions
    db_session.delete.assert_called_once_with(credential)
    db_session.commit.assert_called_once()
    assert response == {"message": "Credential deleted successfully"}

@pytest.mark.unit
def test_delete_credential_not_found(db_session):
    # Simulate credential not found
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = None
    query_mock.filter.return_value = filter_mock
    db_session.query.return_value = query_mock

    with pytest.raises(HTTPException) as exc_info:
        delete_credential(credential_id=1, db=db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Credential not found"