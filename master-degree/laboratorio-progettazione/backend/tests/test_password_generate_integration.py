import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.main import app as main_app
from backend.routes.password_generator import router as security_router

# We create a new test app that includes the routes of main + security
app = FastAPI()

# We copy the routes already registered in main_app
for route in main_app.routes:
    app.routes.append(route)

# We copy the routes already registered in main_app
app.include_router(security_router)

client = TestClient(app)

@pytest.mark.integration
def test_generate_password():
    response = client.get("/api/generate-password?length=16")
    assert response.status_code == 200
    data = response.json()
    assert "password" in data
    assert isinstance(data["password"], str)
    assert len(data["password"]) >= 12

@pytest.mark.integration
def test_generate_passphrase():
    response = client.get("/api/generate-passphrase?words=6")
    assert response.status_code == 200
    data = response.json()
    assert "passphrase" in data
    assert isinstance(data["passphrase"], str)
    assert len(data["passphrase"].split("-")) >= 4  # at least 4 words separated by '-'