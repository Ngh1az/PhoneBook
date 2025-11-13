"""
Authentication Controller for PhoneBook Application
Handles login, register, and logout operations
"""

from models.user_model import UserModel
from utils import (
    validate_email,
    validate_username,
    validate_password,
    validate_required,
    sanitize_input,
)


class AuthController:
    """Controller for authentication operations"""

    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        """
        Login user

        Args:
            username (str): Username
            password (str): Password

        Returns:
            tuple: (bool, user_data or error_message)
        """
        # Validate input
        is_valid, msg = validate_required(username, "Tên đăng nhập")
        if not is_valid:
            return False, msg

        is_valid, msg = validate_required(password, "Mật khẩu")
        if not is_valid:
            return False, msg

        # Sanitize input
        username = sanitize_input(username)

        # Authenticate
        success, result = UserModel.authenticate(username, password)

        if success:
            self.current_user = result
            return True, result

        return False, result

    def register(
        self,
        username,
        email,
        password,
        confirm_password,
        fullname,
        phone=None,
        address=None,
    ):
        """
        Register new user

        Args:
            username (str): Username
            email (str): Email
            password (str): Password
            confirm_password (str): Confirm password
            fullname (str): Full name
            phone (str): Phone number (optional)
            address (str): Address (optional)

        Returns:
            tuple: (bool, message)
        """
        # Validate required fields
        is_valid, msg = validate_required(fullname, "Họ và tên")
        if not is_valid:
            return False, msg

        is_valid, msg = validate_required(username, "Tên đăng nhập")
        if not is_valid:
            return False, msg

        is_valid, msg = validate_required(email, "Email")
        if not is_valid:
            return False, msg

        # Validate username format
        if not validate_username(username):
            return False, "Tên đăng nhập chỉ chứa chữ, số và dấu gạch dưới (3-20 ký tự)"

        # Validate email format
        if not validate_email(email):
            return False, "Định dạng email không hợp lệ"

        # Validate password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return False, msg

        # Check password confirmation
        if password != confirm_password:
            return False, "Mật khẩu xác nhận không khớp"

        # Validate phone if provided
        if phone and phone.strip():
            from utils import validate_phone

            if not validate_phone(phone):
                return False, "Số điện thoại không hợp lệ (10-11 chữ số)"

        # Sanitize inputs
        username = sanitize_input(username)
        email = sanitize_input(email)
        fullname = sanitize_input(fullname)
        phone = sanitize_input(phone) if phone else None
        address = sanitize_input(address) if address else None

        # Create user
        user_id, message = UserModel.create_user(
            username=username,
            email=email,
            password=password,
            fullname=fullname,
            phone=phone,
            address=address,
        )

        if user_id:
            return True, message

        return False, message

    def logout(self):
        """Logout current user"""
        self.current_user = None
        return True, "Đăng xuất thành công"

    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user

    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
