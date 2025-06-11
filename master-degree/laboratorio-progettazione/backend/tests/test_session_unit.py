import pytest
import json
from backend.utils.session import create_session

@pytest.mark.unit
def test_create_session():
    user_id = 1
    response = create_session(user_id)
    assert response.status_code == 200
    response_content = json.loads(response.body)
    assert "access_token" in response_content
    assert "token_type" in response_content