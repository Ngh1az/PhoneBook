"""
Group Controller for PhoneBook Application
Handles group-related operations
"""

from models.group_model import GroupModel
from utils import validate_required, sanitize_input


class GroupController:
    """Controller for group operations"""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_all_groups(self):
        """Get all groups for current user"""
        return GroupModel.get_user_groups(self.user_id)

    def add_group(self, group_name, description=None):
        """
        Add new group

        Args:
            group_name (str): Group name
            description (str): Description (optional)

        Returns:
            tuple: (bool, group_id or error_message)
        """
        # Validate required fields
        is_valid, msg = validate_required(group_name, "Tên nhóm")
        if not is_valid:
            return False, msg

        # Sanitize inputs
        group_name = sanitize_input(group_name)
        description = sanitize_input(description) if description else None

        # Create group
        group_id, message = GroupModel.create_group(
            user_id=self.user_id, group_name=group_name, description=description
        )

        if group_id:
            return True, group_id

        return False, message

    def update_group(self, group_id, group_name=None, description=None):
        """
        Update group

        Args:
            group_id (int): Group ID
            group_name (str): New group name (optional)
            description (str): New description (optional)

        Returns:
            tuple: (bool, message)
        """
        # Validate if updating name
        if group_name is not None:
            is_valid, msg = validate_required(group_name, "Tên nhóm")
            if not is_valid:
                return False, msg
            group_name = sanitize_input(group_name)

        # Sanitize description
        if description is not None:
            description = sanitize_input(description)

        return GroupModel.update_group(group_id, self.user_id, group_name, description)

    def delete_group(self, group_id):
        """
        Delete group

        Args:
            group_id (int): Group ID

        Returns:
            tuple: (bool, message)
        """
        return GroupModel.delete_group(group_id)

    def get_group_by_id(self, group_id):
        """
        Get group by ID

        Args:
            group_id (int): Group ID

        Returns:
            dict: Group data or None
        """
        return GroupModel.find_by_id("group_id", group_id)
