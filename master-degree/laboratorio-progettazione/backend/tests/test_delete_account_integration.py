import pytest
from sqlalchemy.orm import sessionmaker
from backend.db.session import engine, init_db
from backend.db.base import Base
from backend.models.user import User
from backend.models.credential import UserCredential
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    init_db()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def setup_user_and_credentials(db_session):
    # Insert a user and credentials into the test database
    user = User(
        id=1, 
        email="test@example.com", 
        hashed_password="fakehash", 
        passphrase="fakepassphrase", 
        verification_code="dummycode"  # valore non null
    )
    db_session.add(user)
    db_session.commit()

    cred1 = UserCredential(id_user=user.id, url="http://test1.com", encrypted_username="user1", encrypted_password="pass1")
    cred2 = UserCredential(id_user=user.id, url="http://test2.com", encrypted_username="user2", encrypted_password="pass2")
    db_session.add_all([cred1, cred2])
    db_session.commit()

    yield user

    # Cleanup: elimina credenziali e utente
    db_session.query(UserCredential).filter(UserCredential.id_user == user.id).delete()
    db_session.query(User).filter(User.id == user.id).delete()
    db_session.commit()

@pytest.mark.integration
def test_delete_account_integration(setup_user_and_credentials, db_session, monkeypatch):
    user_email = setup_user_and_credentials.email
    user_id = setup_user_and_credentials.id

    # Mock get_current_user to simulate authenticated user
    def mock_get_current_user(request):
        return {"id": user_id, "email": user_email}

    # Patch get_current_user used in your delete_account route
    monkeypatch.setattr("backend.routes.user.get_current_user", mock_get_current_user)

    # Call the delete-account endpoint
    response = client.delete("/api/delete-account")

    # Verify response
    assert response.status_code == 200
    assert f"L'account '{user_email}' has been permanently deleted." in response.json()["message"]

    # Verify user is deleted
    user_check = db_session.query(User).filter(User.id == user_id).first()
    assert user_check is None

    # Verify all credentials of the user are deleted
    creds_check = db_session.query(UserCredential).filter(UserCredential.id_user == user_id).all()
    assert creds_check == []

@pytest.mark.integration
def test_delete_account_user_not_found(db_session, monkeypatch):
    # Mock get_current_user returning non-existent user id
    def mock_get_current_user(request):
        return {"id": 999, "email": "notfound@example.com"}

    monkeypatch.setattr("backend.routes.user.get_current_user", mock_get_current_user)

    # Call the endpoint, user 999 doesn't exist in DB
    response = client.delete("/api/delete-account")

    assert response.status_code == 404
    assert response.json() == {"detail": "Utente non trovato"}
