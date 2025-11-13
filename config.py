"""
Configuration file for PhoneBook Application
Contains database connection settings and application constants
"""

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "112006",  # Change this to your MySQL password
    "database": "phonebook_db",
    "port": 3306,
    "raise_on_warnings": True,
}

# Application Settings
APP_TITLE = "PhoneBook Application"
APP_VERSION = "1.0"
APP_WINDOW_SIZE = "1200x700"
APP_MIN_SIZE = (1000, 600)

# Security Settings
BCRYPT_ROUNDS = 12  # Number of rounds for bcrypt hashing

# Logging Settings
LOG_FILE = "data/error_log.txt"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Backup Settings
BACKUP_FOLDER = "data/backup"
EXPORT_FOLDER = "data/exports"

# UI Colors - Simple & Clean
COLORS = {
    "primary": "#2c3e50",
    "secondary": "#34495e",
    "success": "#27ae60",
    "danger": "#e74c3c",
    "warning": "#f39c12",
    "info": "#3498db",
    "light": "#ecf0f1",
    "dark": "#2c3e50",
    "white": "#ffffff",
    "bg": "#f5f6fa",
    "text": "#2c3e50",
}

# Font Settings
FONTS = {
    "title": ("Segoe UI", 16, "bold"),
    "heading": ("Segoe UI", 12, "bold"),
    "normal": ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "button": ("Segoe UI", 10, "bold"),
}

# Validation Patterns
PATTERNS = {
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone": r"^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$",  # International phone format
    "username": r"^[a-zA-Z0-9_]{3,20}$",
}
