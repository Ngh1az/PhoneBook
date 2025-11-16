"""
Contact Model for PhoneBook Application
Handles contact-related database operations
"""

from models.base_model import BaseModel
from datetime import datetime


class ContactModel(BaseModel):
    """Contact model class"""

    table_name = "contacts"

    @classmethod
    def get_user_contacts(cls, user_id, include_deleted=False):
        """
        Get all contacts for a user

        Args:
            user_id (int): User ID
            include_deleted (bool): Include soft-deleted contacts

        Returns:
            list: List of contacts with group and tag information
        """
        query = """
            SELECT 
                c.*,
                g.group_name,
                GROUP_CONCAT(t.tag_name, ', ') as tags
            FROM contacts c
            LEFT JOIN my_groups g ON c.group_id = g.group_id
            LEFT JOIN contact_tags ct ON c.contact_id = ct.contact_id
            LEFT JOIN tags t ON ct.tag_id = t.tag_id
            WHERE c.user_id = ?
        """

        if not include_deleted:
            query += " AND c.is_deleted = 0"

        query += " GROUP BY c.contact_id ORDER BY c.contact_id ASC"

        return db.execute_query(query, (user_id,), fetch=True) or []

    @classmethod
    def search_contacts(cls, user_id, search_term):
        """
        Search contacts by name, phone, or email

        Args:
            user_id (int): User ID
            search_term (str): Search term

        Returns:
            list: List of matching contacts
        """
        search_pattern = f"%{search_term}%"

        query = """
            SELECT 
                c.*,
                g.group_name,
                GROUP_CONCAT(t.tag_name, ', ') as tags
            FROM contacts c
            LEFT JOIN my_groups g ON c.group_id = g.group_id
            LEFT JOIN contact_tags ct ON c.contact_id = ct.contact_id
            LEFT JOIN tags t ON ct.tag_id = t.tag_id
            WHERE c.user_id = ? 
            AND c.is_deleted = 0
            AND (
                c.first_name LIKE ? 
                OR c.last_name LIKE ? 
                OR c.phone LIKE ? 
                OR c.email LIKE ?
            )
            GROUP BY c.contact_id
            ORDER BY c.contact_id ASC
        """

        params = (
            user_id,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
        )

        return db.execute_query(query, params, fetch=True) or []

    @classmethod
    def filter_by_group(cls, user_id, group_id):
        """
        Filter contacts by group

        Args:
            user_id (int): User ID
            group_id (int): Group ID

        Returns:
            list: List of contacts in the group
        """
        query = """
            SELECT 
                c.*,
                g.group_name,
                GROUP_CONCAT(t.tag_name, ', ') as tags
            FROM contacts c
            LEFT JOIN my_groups g ON c.group_id = g.group_id
            LEFT JOIN contact_tags ct ON c.contact_id = ct.contact_id
            LEFT JOIN tags t ON ct.tag_id = t.tag_id
            WHERE c.user_id = ? 
            AND c.group_id = ?
            AND c.is_deleted = 0
            GROUP BY c.contact_id
            ORDER BY c.contact_id ASC
        """

        return db.execute_query(query, (user_id, group_id), fetch=True) or []

    @classmethod
    def filter_by_tag(cls, user_id, tag_id):
        """
        Filter contacts by tag

        Args:
            user_id (int): User ID
            tag_id (int): Tag ID

        Returns:
            list: List of contacts with the tag
        """
        query = """
            SELECT 
                c.*,
                g.group_name,
                GROUP_CONCAT(t.tag_name, ', ') as tags
            FROM contacts c
            LEFT JOIN my_groups g ON c.group_id = g.group_id
            INNER JOIN contact_tags ct ON c.contact_id = ct.contact_id
            LEFT JOIN tags t ON ct.tag_id = t.tag_id
            WHERE c.user_id = ? 
            AND ct.tag_id = ?
            AND c.is_deleted = 0
            GROUP BY c.contact_id
            ORDER BY c.contact_id ASC
        """

        return db.execute_query(query, (user_id, tag_id), fetch=True) or []

    @classmethod
    def create_contact(
        cls,
        user_id,
        first_name,
        last_name,
        phone,
        email=None,
        address=None,
        notes=None,
        group_id=None,
    ):
        """
        Create a new contact

        Args:
            user_id (int): User ID
            first_name (str): First name
            last_name (str): Last name
            phone (str): Phone number
            email (str): Email (optional)
            address (str): Address (optional)
            notes (str): Notes (optional)
            group_id (int): Group ID (optional)

        Returns:
            tuple: (contact_id or None, message)
        """
        data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "address": address,
            "notes": notes,
            "group_id": group_id,
        }

        contact_id = cls.create(data)

        if contact_id:
            return contact_id, "Thêm liên hệ thành công"
        return None, "Lỗi thêm liên hệ"

    @classmethod
    def update_contact(cls, contact_id, data):
        """
        Update a contact

        Args:
            contact_id (int): Contact ID
            data (dict): Data to update

        Returns:
            tuple: (bool, message)
        """
        success = cls.update("contact_id", contact_id, data)

        if success:
            return True, "Cập nhật liên hệ thành công"
        return False, "Lỗi cập nhật liên hệ"

    @classmethod
    def soft_delete_contact(cls, contact_id):
        """
        Soft delete a contact (mark as deleted)

        Args:
            contact_id (int): Contact ID

        Returns:
            tuple: (bool, message)
        """
        data = {"is_deleted": True, "deleted_at": datetime.now()}

        success = cls.update("contact_id", contact_id, data)

        if success:
            return True, "Đã chuyển liên hệ vào thùng rác"
        return False, "Lỗi xóa liên hệ"

    @classmethod
    def restore_contact(cls, contact_id):
        """
        Restore a soft-deleted contact

        Args:
            contact_id (int): Contact ID

        Returns:
            tuple: (bool, message)
        """
        data = {"is_deleted": False, "deleted_at": None}

        success = cls.update("contact_id", contact_id, data)

        if success:
            return True, "Khôi phục liên hệ thành công"
        return False, "Lỗi khôi phục liên hệ"

    @classmethod
    def permanent_delete_contact(cls, contact_id):
        """
        Permanently delete a contact from database

        Args:
            contact_id (int): Contact ID

        Returns:
            tuple: (bool, message)
        """
        success = cls.delete("contact_id", contact_id)

        if success:
            return True, "Xóa vĩnh viễn liên hệ thành công"
        return False, "Lỗi xóa liên hệ"

    @classmethod
    def get_deleted_contacts(cls, user_id):
        """
        Get all deleted contacts for a user

        Args:
            user_id (int): User ID

        Returns:
            list: List of deleted contacts
        """
        query = """
            SELECT 
                c.*,
                g.group_name
            FROM contacts c
            LEFT JOIN my_groups g ON c.group_id = g.group_id
            WHERE c.user_id = ? AND c.is_deleted = 1
            ORDER BY c.deleted_at DESC
        """

        return db.execute_query(query, (user_id,), fetch=True) or []

    @classmethod
    def add_tag_to_contact(cls, contact_id, tag_id):
        """
        Add a tag to a contact

        Args:
            contact_id (int): Contact ID
            tag_id (int): Tag ID

        Returns:
            bool: True if successful
        """
        query = "INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)"
        result = db.execute_query(query, (contact_id, tag_id))

        return result is not None

    @classmethod
    def remove_tag_from_contact(cls, contact_id, tag_id):
        """
        Remove a tag from a contact

        Args:
            contact_id (int): Contact ID
            tag_id (int): Tag ID

        Returns:
            bool: True if successful
        """
        query = "DELETE FROM contact_tags WHERE contact_id = ? AND tag_id = ?"
        result = db.execute_query(query, (contact_id, tag_id))

        return result is not None

    @classmethod
    def get_contact_tags(cls, contact_id):
        """
        Get all tags for a contact

        Args:
            contact_id (int): Contact ID

        Returns:
            list: List of tags
        """
        query = """
            SELECT t.* 
            FROM tags t
            INNER JOIN contact_tags ct ON t.tag_id = ct.tag_id
            WHERE ct.contact_id = ?
        """

        return db.execute_query(query, (contact_id,), fetch=True) or []


# Import db here to avoid circular import
from db import db
