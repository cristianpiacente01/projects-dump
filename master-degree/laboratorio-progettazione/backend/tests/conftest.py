import pytest
import os
os.environ["PYTEST_CURRENT_TEST"] = "1"

@pytest.fixture(scope="module")
def test_client():
    from backend.main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    yield client

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    from backend.db.session import init_db, SessionLocal
    from backend.models.user import User
    from sqlalchemy.exc import IntegrityError

    init_db()
    db = SessionLocal()
    yield db
    try:
        db.query(User).delete()
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

def create_verified_user(setup_database, email: str, password: str):
    from backend.models.user import User
    from backend.utils.hashing import get_password_hash
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        passphrase="testpassphrase",
        is_verified=True,
        verification_code="123456"
    )
    setup_database.add(user)
    setup_database.commit()
    return user

def login_user(test_client, email: str, password: str):
    return test_client.post("/api/login", json={
        "email": email,
        "password": password
    })