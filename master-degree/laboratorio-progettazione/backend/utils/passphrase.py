"""
This module provides a function to generate a recovery passphrase.
"""

from faker import Faker

fake = Faker()

def generate_passphrase(word_count: int = 6) -> str:
    """Generate a passphrase consisting of word_count random words."""
    words = [fake.word() for _ in range(word_count)]
    return '-'.join(words)
