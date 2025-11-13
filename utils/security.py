"""
Security utility for PhoneBook Application
Handles password hashing and verification using bcrypt
"""

import bcrypt
from config import BCRYPT_ROUNDS


def hash_password(password):
    """
    Hash a password using bcrypt

    Args:
        password (str): Plain text password

    Returns:
        str: Hashed password
    """
    if isinstance(password, str):
        password = password.encode("utf-8")

    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hash

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    if isinstance(plain_password, str):
        plain_password = plain_password.encode("utf-8")

    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain_password, hashed_password)
