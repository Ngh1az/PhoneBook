"""
User Model for PhoneBook Application
Handles user-related database operations
"""

from models.base_model import BaseModel
from utils import hash_password, verify_password


class UserModel(BaseModel):
    """User model class"""

    table_name = "users"

    @classmethod
    def find_by_username(cls, username):
        """
        Find user by username

        Args:
            username (str): Username to search

        Returns:
            dict: User data or None
        """
        query = f"SELECT * FROM {cls.table_name} WHERE username = %s"
        results = db.execute_query(query, (username,), fetch=True)

        if results and len(results) > 0:
            return results[0]
        return None

    @classmethod
    def find_by_email(cls, email):
        """
        Find user by email

        Args:
            email (str): Email to search

        Returns:
            dict: User data or None
        """
        query = f"SELECT * FROM {cls.table_name} WHERE email = %s"
        results = db.execute_query(query, (email,), fetch=True)

        if results and len(results) > 0:
            return results[0]
        return None

    @classmethod
    def create_user(cls, username, email, password, fullname, phone=None, address=None):
        """
        Create a new user

        Args:
            username (str): Username
            email (str): Email
            password (str): Plain text password (will be hashed)
            fullname (str): Full name
            phone (str): Phone number (optional)
            address (str): Address (optional)

        Returns:
            int: User ID or None if failed
        """
        # Check if username or email already exists
        if cls.find_by_username(username):
            return None, "Tên đăng nhập đã tồn tại"

        if cls.find_by_email(email):
            return None, "Email đã được sử dụng"

        # Hash password
        password_hash = hash_password(password)

        # Create user data
        data = {
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "fullname": fullname,
            "phone": phone,
            "address": address,
        }

        user_id = cls.create(data)

        if user_id:
            return user_id, "Đăng ký thành công"
        return None, "Lỗi tạo tài khoản"

    @classmethod
    def authenticate(cls, username, password):
        """
        Authenticate user with username and password

        Args:
            username (str): Username
            password (str): Plain text password

        Returns:
            tuple: (bool, user_data or error_message)
        """
        user = cls.find_by_username(username)

        if not user:
            return False, "Tên đăng nhập không tồn tại"

        if verify_password(password, user["password_hash"]):
            return True, user

        return False, "Mật khẩu không đúng"

    @classmethod
    def update_profile(cls, user_id, data):
        """
        Update user profile

        Args:
            user_id (int): User ID
            data (dict): Data to update

        Returns:
            tuple: (bool, message)
        """
        # If updating email, check for duplicates
        if "email" in data:
            existing_user = cls.find_by_email(data["email"])
            if existing_user and existing_user["user_id"] != user_id:
                return False, "Email đã được sử dụng bởi tài khoản khác"

        # If updating password, hash it
        if "password" in data:
            data["password_hash"] = hash_password(data["password"])
            del data["password"]

        success = cls.update("user_id", user_id, data)

        if success:
            return True, "Cập nhật thông tin thành công"
        return False, "Lỗi cập nhật thông tin"

    @classmethod
    def change_password(cls, user_id, old_password, new_password):
        """
        Change user password

        Args:
            user_id (int): User ID
            old_password (str): Current password
            new_password (str): New password

        Returns:
            tuple: (bool, message)
        """
        user = cls.find_by_id("user_id", user_id)

        if not user:
            return False, "Người dùng không tồn tại"

        # Verify old password
        if not verify_password(old_password, user["password_hash"]):
            return False, "Mật khẩu hiện tại không đúng"

        # Hash new password
        new_password_hash = hash_password(new_password)

        # Update password
        success = cls.update("user_id", user_id, {"password_hash": new_password_hash})

        if success:
            return True, "Đổi mật khẩu thành công"
        return False, "Lỗi đổi mật khẩu"


# Import db here to avoid circular import
from db import db
