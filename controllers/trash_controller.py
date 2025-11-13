"""
Trash Controller for PhoneBook Application
Handles trash/recycle bin operations
"""

from models.contact_model import ContactModel


class TrashController:
    """Controller for trash operations"""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_deleted_contacts(self):
        """Get all deleted contacts"""
        return ContactModel.get_deleted_contacts(self.user_id)

    def restore_contact(self, contact_id):
        """
        Restore a deleted contact

        Args:
            contact_id (int): Contact ID

        Returns:
            tuple: (bool, message)
        """
        return ContactModel.restore_contact(contact_id)

    def restore_multiple(self, contact_ids):
        """
        Restore multiple contacts

        Args:
            contact_ids (list): List of contact IDs

        Returns:
            tuple: (bool, message)
        """
        success_count = 0
        fail_count = 0

        for contact_id in contact_ids:
            success, _ = ContactModel.restore_contact(contact_id)
            if success:
                success_count += 1
            else:
                fail_count += 1

        if fail_count == 0:
            return True, f"Khôi phục thành công {success_count} liên hệ"
        elif success_count == 0:
            return False, f"Không thể khôi phục liên hệ"
        else:
            return (
                True,
                f"Khôi phục thành công {success_count} liên hệ, thất bại {fail_count} liên hệ",
            )

    def permanent_delete(self, contact_id):
        """
        Permanently delete a contact

        Args:
            contact_id (int): Contact ID

        Returns:
            tuple: (bool, message)
        """
        return ContactModel.permanent_delete_contact(contact_id)

    def permanent_delete_multiple(self, contact_ids):
        """
        Permanently delete multiple contacts

        Args:
            contact_ids (list): List of contact IDs

        Returns:
            tuple: (bool, message)
        """
        success_count = 0
        fail_count = 0

        for contact_id in contact_ids:
            success, _ = ContactModel.permanent_delete_contact(contact_id)
            if success:
                success_count += 1
            else:
                fail_count += 1

        if fail_count == 0:
            return True, f"Xóa vĩnh viễn thành công {success_count} liên hệ"
        elif success_count == 0:
            return False, f"Không thể xóa liên hệ"
        else:
            return (
                True,
                f"Xóa thành công {success_count} liên hệ, thất bại {fail_count} liên hệ",
            )

    def empty_trash(self):
        """
        Empty trash (permanently delete all deleted contacts)

        Returns:
            tuple: (bool, message)
        """
        deleted_contacts = self.get_deleted_contacts()

        if not deleted_contacts:
            return False, "Thùng rác trống"

        contact_ids = [contact["contact_id"] for contact in deleted_contacts]
        return self.permanent_delete_multiple(contact_ids)
