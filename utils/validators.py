"""
Validation utility for PhoneBook Application
Handles validation of email, phone, username, etc.
"""

import re
from config import PATTERNS


def validate_email(email):
    """
    Validate email format

    Args:
        email (str): Email to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False

    pattern = re.compile(PATTERNS["email"])
    return bool(pattern.match(email))


def validate_phone(phone):
    """
    Validate phone number format (supports international formats and hotlines)

    Args:
        phone (str): Phone number to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return False

    # Allow spaces, dashes, parentheses, and + for international format
    phone = phone.strip()

    # Check minimum length (at least 3 digits for hotlines like 113, 114, 115)
    digits_only = re.sub(r"[^\d]", "", phone)
    if len(digits_only) < 3 or len(digits_only) > 15:
        return False

    pattern = re.compile(PATTERNS["phone"])
    return bool(pattern.match(phone))


def validate_username(username):
    """
    Validate username format

    Args:
        username (str): Username to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not username:
        return False

    pattern = re.compile(PATTERNS["username"])
    return bool(pattern.match(username))


def validate_password(password):
    """
    Validate password strength

    Args:
        password (str): Password to validate

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not password:
        return False, "Mật khẩu không được để trống"

    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự"

    if len(password) > 50:
        return False, "Mật khẩu không được quá 50 ký tự"

    return True, ""


def validate_required(value, field_name):
    """
    Validate required field

    Args:
        value: Value to validate
        field_name (str): Name of the field

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not value or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} không được để trống"

    return True, ""


def sanitize_input(text):
    """
    Sanitize user input by removing potentially dangerous characters

    Args:
        text (str): Text to sanitize

    Returns:
        str: Sanitized text
    """
    if not text:
        return ""

    # Remove leading/trailing whitespace
    text = text.strip()

    # Remove null bytes
    text = text.replace("\x00", "")

    return text
