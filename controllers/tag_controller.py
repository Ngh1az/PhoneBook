"""
Tag Controller for PhoneBook Application
Handles tag-related operations
"""

from models.tag_model import TagModel
from utils import validate_required, sanitize_input


class TagController:
    """Controller for tag operations"""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_all_tags(self):
        """Get all tags for current user"""
        return TagModel.get_user_tags(self.user_id)

    def add_tag(self, tag_name, description=None):
        """
        Add new tag

        Args:
            tag_name (str): Tag name
            description (str): Description (optional)

        Returns:
            tuple: (bool, tag_id or error_message)
        """
        # Validate required fields
        is_valid, msg = validate_required(tag_name, "Tên thẻ")
        if not is_valid:
            return False, msg

        # Sanitize inputs
        tag_name = sanitize_input(tag_name)
        description = sanitize_input(description) if description else None

        # Create tag
        tag_id, message = TagModel.create_tag(
            user_id=self.user_id, tag_name=tag_name, description=description
        )

        if tag_id:
            return True, tag_id

        return False, message

    def update_tag(self, tag_id, tag_name=None, description=None):
        """
        Update tag

        Args:
            tag_id (int): Tag ID
            tag_name (str): New tag name (optional)
            description (str): New description (optional)

        Returns:
            tuple: (bool, message)
        """
        # Validate if updating name
        if tag_name is not None:
            is_valid, msg = validate_required(tag_name, "Tên thẻ")
            if not is_valid:
                return False, msg
            tag_name = sanitize_input(tag_name)

        # Sanitize description
        if description is not None:
            description = sanitize_input(description)

        return TagModel.update_tag(tag_id, self.user_id, tag_name, description)

    def delete_tag(self, tag_id):
        """
        Delete tag

        Args:
            tag_id (int): Tag ID

        Returns:
            tuple: (bool, message)
        """
        return TagModel.delete_tag(tag_id)

    def get_tag_by_id(self, tag_id):
        """
        Get tag by ID

        Args:
            tag_id (int): Tag ID

        Returns:
            dict: Tag data or None
        """
        return TagModel.find_by_id("tag_id", tag_id)
