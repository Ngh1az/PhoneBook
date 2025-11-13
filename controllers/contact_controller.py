"""
Contact Controller for PhoneBook Application
Handles contact-related operations
"""

from models.contact_model import ContactModel
from models.group_model import GroupModel
from utils import validate_phone, validate_email, validate_required, sanitize_input
from utils.backup import export_contacts_to_csv, import_contacts_from_csv


class ContactController:
    """Controller for contact operations"""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_all_contacts(self):
        """Get all contacts for current user"""
        return ContactModel.get_user_contacts(self.user_id, include_deleted=False)

    def search_contacts(self, search_term):
        """
        Search contacts

        Args:
            search_term (str): Search term

        Returns:
            list: List of matching contacts
        """
        if not search_term or not search_term.strip():
            return self.get_all_contacts()

        return ContactModel.search_contacts(self.user_id, search_term.strip())

    def filter_by_group(self, group_id):
        """
        Filter contacts by group

        Args:
            group_id (int): Group ID

        Returns:
            list: List of contacts in group
        """
        return ContactModel.filter_by_group(self.user_id, group_id)

    def filter_by_tag(self, tag_id):
        """
        Filter contacts by tag

        Args:
            tag_id (int): Tag ID

        Returns:
            list: List of contacts with tag
        """
        return ContactModel.filter_by_tag(self.user_id, tag_id)

    def add_contact(
        self,
        first_name,
        last_name,
        phone,
        email=None,
        address=None,
        notes=None,
        group_id=None,
    ):
        """
        Add new contact

        Args:
            first_name (str): First name
            last_name (str): Last name
            phone (str): Phone number
            email (str): Email (optional)
            address (str): Address (optional)
            notes (str): Notes (optional)
            group_id (int): Group ID (optional)

        Returns:
            tuple: (bool, contact_id or error_message)
        """
        # Validate required fields
        is_valid, msg = validate_required(first_name, "Tên")
        if not is_valid:
            return False, msg

        is_valid, msg = validate_required(last_name, "Họ")
        if not is_valid:
            return False, msg

        is_valid, msg = validate_required(phone, "Số điện thoại")
        if not is_valid:
            return False, msg

        # Validate phone format
        if not validate_phone(phone):
            return False, "Số điện thoại không hợp lệ (10-11 chữ số)"

        # Validate email if provided
        if email and email.strip():
            if not validate_email(email):
                return False, "Định dạng email không hợp lệ"

        # Sanitize inputs
        first_name = sanitize_input(first_name)
        last_name = sanitize_input(last_name)
        phone = sanitize_input(phone)
        email = sanitize_input(email) if email else None
        address = sanitize_input(address) if address else None
        notes = sanitize_input(notes) if notes else None

        # Create contact
        contact_id, message = ContactModel.create_contact(
            user_id=self.user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            address=address,
            notes=notes,
            group_id=group_id,
        )

        if contact_id:
            return True, contact_id

        return False, message

    def update_contact(self, contact_id, data):
        """
        Update contact

        Args:
            contact_id (int): Contact ID
            data (dict): Data to update

        Returns:
            tuple: (bool, message)
        """
        # Validate phone if present
        if "phone" in data and data["phone"]:
            if not validate_phone(data["phone"]):
                return False, "Số điện thoại không hợp lệ (10-11 chữ số)"

        # Validate email if present
        if "email" in data and data["email"]:
            if not validate_email(data["email"]):
                return False, "Định dạng email không hợp lệ"

        # Sanitize all string fields
        sanitized_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized_data[key] = sanitize_input(value)
            else:
                sanitized_data[key] = value

        return ContactModel.update_contact(contact_id, sanitized_data)

    def delete_contact(self, contact_id):
        """
        Soft delete contact

        Args:
            contact_id (int): Contact ID

        Returns:
            tuple: (bool, message)
        """
        return ContactModel.soft_delete_contact(contact_id)

    def get_contact_by_id(self, contact_id):
        """
        Get contact by ID

        Args:
            contact_id (int): Contact ID

        Returns:
            dict: Contact data or None
        """
        return ContactModel.find_by_id("contact_id", contact_id)

    def add_tag_to_contact(self, contact_id, tag_id):
        """
        Add tag to contact

        Args:
            contact_id (int): Contact ID
            tag_id (int): Tag ID

        Returns:
            tuple: (bool, message)
        """
        success = ContactModel.add_tag_to_contact(contact_id, tag_id)

        if success:
            return True, "Thêm thẻ thành công"
        return False, "Lỗi thêm thẻ"

    def remove_tag_from_contact(self, contact_id, tag_id):
        """
        Remove tag from contact

        Args:
            contact_id (int): Contact ID
            tag_id (int): Tag ID

        Returns:
            tuple: (bool, message)
        """
        success = ContactModel.remove_tag_from_contact(contact_id, tag_id)

        if success:
            return True, "Xóa thẻ thành công"
        return False, "Lỗi xóa thẻ"

    def get_contact_tags(self, contact_id):
        """
        Get all tags for a contact

        Args:
            contact_id (int): Contact ID

        Returns:
            list: List of tags
        """
        return ContactModel.get_contact_tags(contact_id)

    def export_contacts_to_csv(self, contacts=None, filename=None):
        """
        Export contacts to CSV file

        Args:
            contacts (list): List of contacts to export. If None, exports all contacts
            filename (str): Optional filename

        Returns:
            tuple: (bool, filepath or error message)
        """
        if contacts is None:
            contacts = self.get_all_contacts()

        return export_contacts_to_csv(contacts, filename)

    def import_contacts_from_csv(self, filepath):
        """
        Import contacts from CSV file

        Args:
            filepath (str): Path to CSV file

        Returns:
            tuple: (bool, dict with results or error message)
        """
        # Read CSV file
        success, result = import_contacts_from_csv(filepath)

        if not success:
            return False, result

        contacts_data = result
        imported = 0
        skipped = 0
        errors = []

        for contact_data in contacts_data:
            first_name = contact_data.get("first_name", "").strip()
            last_name = contact_data.get("last_name", "").strip()
            phone = contact_data.get("phone", "").strip()
            email = contact_data.get("email", "").strip()
            address = contact_data.get("address", "").strip()
            notes = contact_data.get("notes", "").strip()
            group_name = contact_data.get("group_name", "").strip()

            # Skip empty rows
            if not first_name and not last_name and not phone:
                continue

            # Find group_id if group_name provided
            group_id = None
            if group_name:
                groups = GroupModel.get_user_groups(self.user_id)
                for group in groups:
                    if group.get("group_name") == group_name:
                        group_id = group.get("group_id")
                        break

            # Try to add contact
            success, msg = self.add_contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email if email else None,
                address=address if address else None,
                notes=notes if notes else None,
                group_id=group_id,
            )

            if success:
                imported += 1
            else:
                skipped += 1
                errors.append(f"{first_name} {last_name} ({phone}): {msg}")

        return True, {"imported": imported, "skipped": skipped, "errors": errors}
