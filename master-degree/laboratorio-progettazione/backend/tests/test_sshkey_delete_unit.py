import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from backend.models.sshkey import UserSSHKey
from backend.routes.sshkey import delete_sshkey

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def request_mock():
    req = MagicMock(spec=Request)
    return req

@pytest.mark.unit
def test_delete_sshkey_existing(db_session, request_mock, monkeypatch):
    sshkey = UserSSHKey(id_sshkey=1, id_user=123, name="test", encrypted_private_key="...", encrypted_public_key="...", encrypted_passphrase="...", encrypted_notes="...")

    monkeypatch.setattr("backend.routes.sshkey.get_current_user", lambda req: {"id": 123})

    db_session.query.return_value.filter_by.return_value.first.return_value = sshkey
    db_session.delete = MagicMock()
    db_session.commit = MagicMock()

    response = delete_sshkey(id_sshkey=1, db=db_session, request=request_mock)

    db_session.delete.assert_called_once_with(sshkey)
    db_session.commit.assert_called_once()
    assert response == {"message": "SSH key deleted successfully"}

@pytest.mark.unit
def test_delete_sshkey_not_found(db_session, request_mock, monkeypatch):
    monkeypatch.setattr("backend.routes.sshkey.get_current_user", lambda req: {"id": 123})

    db_session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        delete_sshkey(id_sshkey=1, db=db_session, request=request_mock)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "SSH key not found or not authorized"
