"""
Profile Controller for PhoneBook Application
Handles user profile operations
"""

from models.user_model import UserModel
from utils import (
    validate_email,
    validate_password,
    validate_phone,
    validate_required,
    sanitize_input,
)


class ProfileController:
    """Controller for profile operations"""

    def __init__(self, user_id):
        self.user_id = user_id

    def get_profile(self):
        """Get user profile"""
        return UserModel.find_by_id("user_id", self.user_id)

    def update_profile(self, fullname=None, email=None, phone=None, address=None):
        """
        Update user profile

        Args:
            fullname (str): Full name (optional)
            email (str): Email (optional)
            phone (str): Phone (optional)
            address (str): Address (optional)

        Returns:
            tuple: (bool, message)
        """
        data = {}

        # Validate and add fullname
        if fullname is not None:
            is_valid, msg = validate_required(fullname, "Họ và tên")
            if not is_valid:
                return False, msg
            data["fullname"] = sanitize_input(fullname)

        # Validate and add email
        if email is not None:
            is_valid, msg = validate_required(email, "Email")
            if not is_valid:
                return False, msg
            if not validate_email(email):
                return False, "Định dạng email không hợp lệ"
            data["email"] = sanitize_input(email)

        # Validate and add phone
        if phone is not None and phone.strip():
            if not validate_phone(phone):
                return False, "Số điện thoại không hợp lệ (10-11 chữ số)"
            data["phone"] = sanitize_input(phone)
        elif phone is not None:
            data["phone"] = None

        # Add address
        if address is not None:
            data["address"] = sanitize_input(address) if address.strip() else None

        if not data:
            return False, "Không có dữ liệu để cập nhật"

        return UserModel.update_profile(self.user_id, data)

    def change_password(self, old_password, new_password, confirm_password):
        """
        Change user password

        Args:
            old_password (str): Current password
            new_password (str): New password
            confirm_password (str): Confirm new password

        Returns:
            tuple: (bool, message)
        """
        # Validate old password
        is_valid, msg = validate_required(old_password, "Mật khẩu hiện tại")
        if not is_valid:
            return False, msg

        # Validate new password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return False, msg

        # Check password confirmation
        if new_password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp"

        # Check if new password is different from old
        if old_password == new_password:
            return False, "Mật khẩu mới phải khác mật khẩu hiện tại"

        return UserModel.change_password(self.user_id, old_password, new_password)
