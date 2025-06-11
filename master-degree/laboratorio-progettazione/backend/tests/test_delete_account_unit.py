import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.models.user import User
from backend.models.credential import UserCredential
from backend.routes.user import delete_account

@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

@pytest.fixture
def mock_current_user(monkeypatch):
    # Mocka get_current_user per restituire sempre utente con id 1
    monkeypatch.setattr("backend.routes.user.get_current_user", lambda request: {"id": 1, "email": "test@example.com"})

@pytest.mark.unit
def test_delete_account_success(db_session, mock_current_user):
    # Mock user trovato in DB
    user = User(id=1, email="test@example.com", hashed_password="hashedpw")

    # Mock per db.query(User)
    query_user_mock = MagicMock()
    filter_user_mock = MagicMock()
    filter_user_mock.first.return_value = user
    query_user_mock.filter.return_value = filter_user_mock
    db_session.query.return_value = query_user_mock

    # Mock per db.query(UserCredential).filter().delete()
    query_cred_mock = MagicMock()
    filter_cred_mock = MagicMock()
    # Imposta il metodo delete sulla filter di UserCredential
    filter_cred_mock.delete = MagicMock()
    query_cred_mock.filter.return_value = filter_cred_mock

    # Quando viene chiamato db.query(UserCredential), ritorna query_cred_mock
    def query_side_effect(arg):
        if arg == UserCredential:
            return query_cred_mock
        else:
            return query_user_mock
    db_session.query.side_effect = query_side_effect

    # Mock delete e commit per l'utente
    db_session.delete = MagicMock()
    db_session.commit = MagicMock()

    # Chiamata alla funzione
    response = delete_account(request=MagicMock(), db=db_session)

    # Verifiche
    filter_cred_mock.delete.assert_called_once()  # delete credenziali
    db_session.delete.assert_called_once_with(user)
    db_session.commit.assert_called_once()
    assert "permanently deleted" in response["message"]

@pytest.mark.unit
def test_delete_account_user_not_found(db_session, mock_current_user):
    # Mock db.query(User) che non trova l'utente
    query_user_mock = MagicMock()
    filter_user_mock = MagicMock()
    filter_user_mock.first.return_value = None
    query_user_mock.filter.return_value = filter_user_mock
    db_session.query.return_value = query_user_mock

    with pytest.raises(HTTPException) as exc_info:
        delete_account(request=MagicMock(), db=db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Utente non trovato"
