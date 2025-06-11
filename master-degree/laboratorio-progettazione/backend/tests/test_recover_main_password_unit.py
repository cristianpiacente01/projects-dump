import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from backend.routes import recover_main_password

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.mark.unit
def test_verify_passphrase_success(db_session):
    # Mock user
    user = MagicMock(id=10, email="unituser@example.com")
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = user
    query_mock.filter.return_value = filter_mock
    db_session.query.return_value = query_mock

    data = {"email": "unituser@example.com", "passphrase": "unitpass"}
    result = recover_main_password.verify_passphrase(data, db=db_session)
    assert result == {"user_id": 10, "email": "unituser@example.com"}

@pytest.mark.unit
def test_verify_passphrase_missing_fields(db_session):
    with pytest.raises(HTTPException) as exc:
        recover_main_password.verify_passphrase({"email": "unituser@example.com"}, db=db_session)
    assert exc.value.status_code == 400

@pytest.mark.unit
def test_verify_passphrase_not_found(db_session):
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = None
    query_mock.filter.return_value = filter_mock
    db_session.query.return_value = query_mock

    data = {"email": "unituser@example.com", "passphrase": "wrong"}
    with pytest.raises(HTTPException) as exc:
        recover_main_password.verify_passphrase(data, db=db_session)
    assert exc.value.status_code == 404

@pytest.mark.unit
@patch("backend.routes.recover_main_password.set_new_password", return_value="hashedpass")
@patch("backend.routes.recover_main_password.generate_passphrase", return_value="newunitpass")
def test_reset_password_success(mock_generate, mock_set_new, db_session):
    user = MagicMock(id=20)
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = user
    query_mock.filter.return_value = filter_mock
    db_session.query.return_value = query_mock
    db_session.commit = MagicMock()

    data = {"user_id": 20, "new_password": "newpass"}
    result = recover_main_password.reset_password(data, db=db_session)
    assert result["message"] == "Password reset successful"
    assert result["new_passphrase"] == "newunitpass"
    assert user.hashed_password == "hashedpass"
    assert user.passphrase == "newunitpass"
    db_session.commit.assert_called_once()

@pytest.mark.unit
def test_reset_password_missing_fields(db_session):
    with pytest.raises(HTTPException) as exc:
        recover_main_password.reset_password({"user_id": 20}, db=db_session)
    assert exc.value.status_code == 400

@pytest.mark.unit
def test_reset_password_user_not_found(db_session):
    query_mock = MagicMock()
    filter_mock = MagicMock()
    filter_mock.first.return_value = None
    query_mock.filter.return_value = filter_mock
    db_session.query.return_value = query_mock

    data = {"user_id": 99, "new_password": "irrelevant"}
    with pytest.raises(HTTPException) as exc:
        recover_main_password.reset_password(data, db=db_session)
    assert exc.value.status_code == 404
