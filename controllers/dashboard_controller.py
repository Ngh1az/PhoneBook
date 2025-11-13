"""
Dashboard Controller for PhoneBook Application
Handles dashboard statistics
"""

from models.contact_model import ContactModel
from models.group_model import GroupModel
from models.tag_model import TagModel


class DashboardController:
    """Controller for dashboard operations"""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_statistics(self):
        """
        Get dashboard statistics

        Returns:
            dict: Statistics data
        """
        # Count total contacts (not deleted)
        total_contacts = ContactModel.count(
            {"user_id": self.user_id, "is_deleted": False}
        )

        # Count groups
        total_groups = GroupModel.count_user_groups(self.user_id)

        # Count tags
        total_tags = TagModel.count_user_tags(self.user_id)

        # Get recent contacts (last 5)
        all_contacts = ContactModel.get_user_contacts(
            self.user_id, include_deleted=False
        )
        recent_contacts = sorted(
            all_contacts, key=lambda x: x.get("created_at", ""), reverse=True
        )[:5]

        # Get top 5 most used groups
        top_groups = self.get_top_groups(5)

        # Get top 5 most used tags
        top_tags = self.get_top_tags(5)

        return {
            "total_contacts": total_contacts,
            "total_groups": total_groups,
            "total_tags": total_tags,
            "recent_contacts": recent_contacts,
            "top_groups": top_groups,
            "top_tags": top_tags,
        }

    def get_top_groups(self, limit=5):
        """
        Get top groups by contact count

        Args:
            limit (int): Number of groups to return

        Returns:
            list: Top groups with contact count
        """
        groups = GroupModel.get_user_groups(self.user_id)
        # Sort by contact_count descending
        sorted_groups = sorted(
            groups, key=lambda x: x.get("contact_count", 0), reverse=True
        )
        return sorted_groups[:limit]

    def get_top_tags(self, limit=5):
        """
        Get top tags by usage count

        Args:
            limit (int): Number of tags to return

        Returns:
            list: Top tags with usage count
        """
        tags = TagModel.get_user_tags(self.user_id)
        # Sort by usage_count descending
        sorted_tags = sorted(tags, key=lambda x: x.get("usage_count", 0), reverse=True)
        return sorted_tags[:limit]

    def get_groups_with_count(self):
        """Get all groups with contact count"""
        return GroupModel.get_user_groups(self.user_id)

    def get_tags_with_count(self):
        """Get all tags with usage count"""
        return TagModel.get_user_tags(self.user_id)
