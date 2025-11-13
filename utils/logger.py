"""
Logging utility for PhoneBook Application
Handles error logging to file
"""

import os
from datetime import datetime
from config import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def ensure_log_file():
    """Ensure log file and directory exist"""
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"=== PhoneBook Application Error Log ===\n")
            f.write(f"Started at: {datetime.now().strftime(LOG_DATE_FORMAT)}\n\n")


def log_error(message):
    """
    Log error message to file

    Args:
        message (str): Error message to log
    """
    try:
        ensure_log_file()
        timestamp = datetime.now().strftime(LOG_DATE_FORMAT)
        log_entry = f"[{timestamp}] ERROR: {message}\n"

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write to log file: {e}")


def log_info(message):
    """
    Log info message to file

    Args:
        message (str): Info message to log
    """
    try:
        ensure_log_file()
        timestamp = datetime.now().strftime(LOG_DATE_FORMAT)
        log_entry = f"[{timestamp}] INFO: {message}\n"

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write to log file: {e}")


def log_warning(message):
    """
    Log warning message to file

    Args:
        message (str): Warning message to log
    """
    try:
        ensure_log_file()
        timestamp = datetime.now().strftime(LOG_DATE_FORMAT)
        log_entry = f"[{timestamp}] WARNING: {message}\n"

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write to log file: {e}")
