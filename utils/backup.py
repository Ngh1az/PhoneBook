"""
Backup and restore utility for PhoneBook Application
Handles CSV export and import of contacts
"""

import csv
import os
from datetime import datetime
from config import BACKUP_FOLDER, EXPORT_FOLDER


def ensure_folders():
    """Ensure backup and export folders exist"""
    for folder in [BACKUP_FOLDER, EXPORT_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def export_contacts_to_csv(contacts, filename=None):
    """
    Export contacts to CSV file

    Args:
        contacts (list): List of contact dictionaries
        filename (str): Optional filename, auto-generated if None

    Returns:
        tuple: (bool, str) - (success, filepath or error message)
    """
    try:
        ensure_folders()

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"contacts_backup_{timestamp}.csv"

        filepath = os.path.join(EXPORT_FOLDER, filename)

        # Define CSV headers
        headers = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "address",
            "notes",
            "group_name",
            "tags",
        ]

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for contact in contacts:
                row = {
                    "first_name": contact.get("first_name", ""),
                    "last_name": contact.get("last_name", ""),
                    "phone": contact.get("phone", ""),
                    "email": contact.get("email", ""),
                    "address": contact.get("address", ""),
                    "notes": contact.get("notes", ""),
                    "group_name": contact.get("group_name", ""),
                    "tags": contact.get("tags", ""),  # Comma-separated tags
                }
                writer.writerow(row)

        return True, filepath

    except Exception as e:
        return False, f"Lỗi xuất file CSV: {str(e)}"


def import_contacts_from_csv(filepath):
    """
    Import contacts from CSV file

    Args:
        filepath (str): Path to CSV file

    Returns:
        tuple: (bool, list or str) - (success, contacts list or error message)
    """
    try:
        if not os.path.exists(filepath):
            return False, "File không tồn tại"

        contacts = []

        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                contact = {
                    "first_name": row.get("first_name", "").strip(),
                    "last_name": row.get("last_name", "").strip(),
                    "phone": row.get("phone", "").strip(),
                    "email": row.get("email", "").strip(),
                    "address": row.get("address", "").strip(),
                    "notes": row.get("notes", "").strip(),
                    "group_name": row.get("group_name", "").strip(),
                    "tags": row.get("tags", "").strip(),
                }

                # Skip empty rows
                if contact["first_name"] or contact["last_name"] or contact["phone"]:
                    contacts.append(contact)

        return True, contacts

    except Exception as e:
        return False, f"Lỗi đọc file CSV: {str(e)}"


def create_backup(contacts):
    """
    Create automatic backup of contacts

    Args:
        contacts (list): List of contact dictionaries

    Returns:
        tuple: (bool, str) - (success, message)
    """
    try:
        ensure_folders()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"auto_backup_{timestamp}.csv"
        filepath = os.path.join(BACKUP_FOLDER, filename)

        # Define CSV headers
        headers = ["first_name", "last_name", "phone", "email", "address", "notes"]

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for contact in contacts:
                row = {
                    "first_name": contact.get("first_name", ""),
                    "last_name": contact.get("last_name", ""),
                    "phone": contact.get("phone", ""),
                    "email": contact.get("email", ""),
                    "address": contact.get("address", ""),
                    "notes": contact.get("notes", ""),
                }
                writer.writerow(row)

        return True, f"Backup tạo thành công: {filepath}"

    except Exception as e:
        return False, f"Lỗi tạo backup: {str(e)}"
