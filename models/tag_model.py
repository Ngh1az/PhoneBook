"""
Tag Model for PhoneBook Application
Handles tag-related database operations
"""

from models.base_model import BaseModel


class TagModel(BaseModel):
    """Tag model class"""

    table_name = "tags"

    @classmethod
    def get_user_tags(cls, user_id):
        """
        Get all tags for a user

        Args:
            user_id (int): User ID

        Returns:
            list: List of tags with usage count
        """
        query = """
            SELECT 
                t.*,
                COUNT(ct.contact_id) as usage_count
            FROM tags t
            LEFT JOIN contact_tags ct ON t.tag_id = ct.tag_id
            LEFT JOIN contacts c ON ct.contact_id = c.contact_id AND c.is_deleted = FALSE
            WHERE t.user_id = ?
            GROUP BY t.tag_id
            ORDER BY t.tag_name
        """

        return db.execute_query(query, (user_id,), fetch=True) or []

    @classmethod
    def find_by_name(cls, user_id, tag_name):
        """
        Find a tag by name for a specific user

        Args:
            user_id (int): User ID
            tag_name (str): Tag name

        Returns:
            dict: Tag data or None
        """
        query = f"SELECT * FROM {cls.table_name} WHERE user_id = ? AND tag_name = ?"
        results = db.execute_query(query, (user_id, tag_name), fetch=True)

        if results and len(results) > 0:
            return results[0]
        return None

    @classmethod
    def create_tag(cls, user_id, tag_name, description=None):
        """
        Create a new tag

        Args:
            user_id (int): User ID
            tag_name (str): Tag name
            description (str): Description (optional)

        Returns:
            tuple: (tag_id or None, message)
        """
        # Check if tag name already exists for this user
        existing = cls.find_by_name(user_id, tag_name)
        if existing:
            return None, "Tên thẻ đã tồn tại"

        data = {"user_id": user_id, "tag_name": tag_name, "description": description}

        tag_id = cls.create(data)

        if tag_id:
            return tag_id, "Tạo thẻ thành công"
        return None, "Lỗi tạo thẻ"

    @classmethod
    def update_tag(cls, tag_id, user_id, tag_name=None, description=None):
        """
        Update a tag

        Args:
            tag_id (int): Tag ID
            user_id (int): User ID
            tag_name (str): New tag name (optional)
            description (str): New description (optional)

        Returns:
            tuple: (bool, message)
        """
        # If updating name, check for duplicates
        if tag_name:
            existing = cls.find_by_name(user_id, tag_name)
            if existing and existing["tag_id"] != tag_id:
                return False, "Tên thẻ đã tồn tại"

        data = {}
        if tag_name is not None:
            data["tag_name"] = tag_name
        if description is not None:
            data["description"] = description

        if not data:
            return False, "Không có dữ liệu để cập nhật"

        success = cls.update("tag_id", tag_id, data)

        if success:
            return True, "Cập nhật thẻ thành công"
        return False, "Lỗi cập nhật thẻ"

    @classmethod
    def delete_tag(cls, tag_id):
        """
        Delete a tag (contact associations are automatically removed)

        Args:
            tag_id (int): Tag ID

        Returns:
            tuple: (bool, message)
        """
        # contact_tags will be automatically deleted due to ON DELETE CASCADE
        success = cls.delete("tag_id", tag_id)

        if success:
            return True, "Xóa thẻ thành công"
        return False, "Lỗi xóa thẻ"

    @classmethod
    def count_user_tags(cls, user_id):
        """
        Count total tags for a user

        Args:
            user_id (int): User ID

        Returns:
            int: Number of tags
        """
        return cls.count({"user_id": user_id})


# Import db here to avoid circular import
from db import db
