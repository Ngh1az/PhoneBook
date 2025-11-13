"""
Helper utility functions for PhoneBook Application
"""

from datetime import datetime


def format_phone(phone):
    """
    Format phone number for display

    Args:
        phone (str): Phone number to format

    Returns:
        str: Formatted phone number
    """
    if not phone:
        return ""

    # Remove spaces and dashes
    phone = phone.replace(" ", "").replace("-", "")

    # Format as: 0xxx-xxx-xxx
    if len(phone) == 10:
        return f"{phone[:4]}-{phone[4:7]}-{phone[7:]}"
    elif len(phone) == 11:
        return f"{phone[:4]}-{phone[4:7]}-{phone[7:]}"

    return phone


def format_datetime(dt):
    """
    Format datetime for display

    Args:
        dt (datetime): Datetime object

    Returns:
        str: Formatted datetime string
    """
    if not dt:
        return ""

    if isinstance(dt, str):
        return dt

    return dt.strftime("%d/%m/%Y %H:%M")


def format_date(dt):
    """
    Format date for display

    Args:
        dt (datetime): Datetime object

    Returns:
        str: Formatted date string
    """
    if not dt:
        return ""

    if isinstance(dt, str):
        return dt

    return dt.strftime("%d/%m/%Y")


def get_full_name(first_name, last_name):
    """
    Combine first and last name

    Args:
        first_name (str): First name
        last_name (str): Last name

    Returns:
        str: Full name
    """
    return f"{first_name} {last_name}".strip()


def truncate_text(text, max_length=50):
    """
    Truncate text to maximum length

    Args:
        text (str): Text to truncate
        max_length (int): Maximum length

    Returns:
        str: Truncated text
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


def get_initials(first_name, last_name):
    """
    Get initials from names

    Args:
        first_name (str): First name
        last_name (str): Last name

    Returns:
        str: Initials (e.g., "JD" for "John Doe")
    """
    initials = ""

    if first_name:
        initials += first_name[0].upper()

    if last_name:
        initials += last_name[0].upper()

    return initials or "?"
