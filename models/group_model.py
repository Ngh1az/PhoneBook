"""
Group Model for PhoneBook Application
Handles group-related database operations
"""

from models.base_model import BaseModel


class GroupModel(BaseModel):
    """Group model class"""

    table_name = "my_groups"

    @classmethod
    def get_user_groups(cls, user_id):
        """
        Get all groups for a user

        Args:
            user_id (int): User ID

        Returns:
            list: List of groups with contact count
        """
        query = """
            SELECT 
                g.*,
                COUNT(c.contact_id) as contact_count
            FROM my_groups g
            LEFT JOIN contacts c ON g.group_id = c.group_id AND c.is_deleted = FALSE
            WHERE g.user_id = ?
            GROUP BY g.group_id
            ORDER BY g.group_name
        """

        return db.execute_query(query, (user_id,), fetch=True) or []

    @classmethod
    def find_by_name(cls, user_id, group_name):
        """
        Find a group by name for a specific user

        Args:
            user_id (int): User ID
            group_name (str): Group name

        Returns:
            dict: Group data or None
        """
        query = f"SELECT * FROM {cls.table_name} WHERE user_id = ? AND group_name = ?"
        results = db.execute_query(query, (user_id, group_name), fetch=True)

        if results and len(results) > 0:
            return results[0]
        return None

    @classmethod
    def create_group(cls, user_id, group_name, description=None):
        """
        Create a new group

        Args:
            user_id (int): User ID
            group_name (str): Group name
            description (str): Description (optional)

        Returns:
            tuple: (group_id or None, message)
        """
        # Check if group name already exists for this user
        existing = cls.find_by_name(user_id, group_name)
        if existing:
            return None, "Tên nhóm đã tồn tại"

        data = {
            "user_id": user_id,
            "group_name": group_name,
            "description": description,
        }

        group_id = cls.create(data)

        if group_id:
            return group_id, "Tạo nhóm thành công"
        return None, "Lỗi tạo nhóm"

    @classmethod
    def update_group(cls, group_id, user_id, group_name=None, description=None):
        """
        Update a group

        Args:
            group_id (int): Group ID
            user_id (int): User ID
            group_name (str): New group name (optional)
            description (str): New description (optional)

        Returns:
            tuple: (bool, message)
        """
        # If updating name, check for duplicates
        if group_name:
            existing = cls.find_by_name(user_id, group_name)
            if existing and existing["group_id"] != group_id:
                return False, "Tên nhóm đã tồn tại"

        data = {}
        if group_name is not None:
            data["group_name"] = group_name
        if description is not None:
            data["description"] = description

        if not data:
            return False, "Không có dữ liệu để cập nhật"

        success = cls.update("group_id", group_id, data)

        if success:
            return True, "Cập nhật nhóm thành công"
        return False, "Lỗi cập nhật nhóm"

    @classmethod
    def delete_group(cls, group_id):
        """
        Delete a group (contacts in the group are not deleted)

        Args:
            group_id (int): Group ID

        Returns:
            tuple: (bool, message)
        """
        # First, remove group_id from all contacts in this group
        query = "UPDATE contacts SET group_id = NULL WHERE group_id = ?"
        db.execute_query(query, (group_id,))

        # Then delete the group
        success = cls.delete("group_id", group_id)

        if success:
            return True, "Xóa nhóm thành công"
        return False, "Lỗi xóa nhóm"

    @classmethod
    def count_user_groups(cls, user_id):
        """
        Count total groups for a user

        Args:
            user_id (int): User ID

        Returns:
            int: Number of groups
        """
        return cls.count({"user_id": user_id})


# Import db here to avoid circular import
from db import db
