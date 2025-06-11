import pytest
from sqlalchemy.orm import sessionmaker
from backend.db.session import engine, init_db
from backend.db.base import Base
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
def setup_credential(db_session):
    # Insert a credential into the test database
    credential = UserCredential(id_credential=1, id_user=123, url="http://example.com", encrypted_username="user", encrypted_password="pass")
    db_session.add(credential)
    db_session.commit()
    return credential

@pytest.mark.integration
def test_delete_credential_integration(setup_credential, db_session):
    # Test deleting a credential via HTTP DELETE request
    response = client.delete("/api/credentials/1")

    # Verify the response
    assert response.status_code == 200
    assert response.json() == {"message": "Credential deleted successfully"}

    # Verify the credential is actually deleted
    credential = db_session.query(UserCredential).filter(UserCredential.id_credential == 1).first()
    assert credential is None

@pytest.mark.integration
def test_delete_credential_not_found(db_session):
    # Test deleting a non-existing credential
    response = client.delete("/api/credentials/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Credential not found"}