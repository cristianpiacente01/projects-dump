import secrets
import string
from backend.utils.passphrase import generate_passphrase


def generate_secret(method='password'):
    """
    Generates a password or passphrase according to the chosen method.
    The param method must be 'password' or 'passphrase'
    """
    if method == 'password':
        return generate_password()
    if method == 'passphrase':
        return generate_passphrase()
    raise ValueError("Invalid method. Use 'password' or 'passphrase'")
    

def generate_password(
    length=16,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
):
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected")

    return ''.join(secrets.choice(characters) for _ in range(length))