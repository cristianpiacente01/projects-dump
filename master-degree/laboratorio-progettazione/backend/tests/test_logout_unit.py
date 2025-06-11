import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.utils.session import logout_user

@pytest.mark.unit
def test_logout_user():
    client = TestClient(app)
    response = logout_user()
    assert response.status_code == 200
    assert response.body == b'{"message":"Logged out successfully"}'
    assert response.headers.get("set-cookie") is not None
    assert 'session="";' in response.headers.get("set-cookie")
    assert 'expires=' in response.headers.get("set-cookie")