import pytest
from backend.utils.verificationcode import generate_verification_code

@pytest.mark.unit
def test_generate_verification_code():
    code = generate_verification_code()
    assert len(code) == 6, "The verification code should be 6 characters long"
    assert code.isalnum(), "The verification code should be alphanumeric"
    assert code.isupper(), "The verification code should be in uppercase"