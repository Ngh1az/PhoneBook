"""
PhoneBook Application - Main Entry Point
A desktop application for managing contacts using MySQL and Tkinter

Author: Group 10
Version: 1.0
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import APP_TITLE, APP_WINDOW_SIZE, COLORS
from db import db
from utils.logger import log_info, log_error


class PhoneBookApp:
    """Main application class"""

    def __init__(self):
        self.root = None
        self.current_view = None
        self.current_user = None

    def initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            print("=" * 50)
            print("Khởi động PhoneBook Application...")
            print("=" * 50)

            # Initialize database
            if not db.init_database():
                messagebox.showerror(
                    "Lỗi Database",
                    "Không thể khởi tạo database.\nVui lòng kiểm tra cấu hình trong file config.py",
                )
                return False

            # Create default admin user if not exists
            self.create_default_admin()

            # Print default login credentials
            print("\n" + "=" * 50)
            print("THÔNG TIN ĐĂNG NHẬP:")
            print("-" * 50)
            print("Tên đăng nhập: admin")
            print("Mật khẩu: 123456")
            print("=" * 50 + "\n")

            log_info("Application started successfully")
            return True

        except Exception as e:
            error_msg = f"Lỗi khởi tạo ứng dụng: {str(e)}"
            log_error(error_msg)
            messagebox.showerror("Lỗi", error_msg)
            return False

    def create_default_admin(self):
        """Create default admin user if not exists"""
        try:
            from utils.security import hash_password

            # Check if admin exists
            check_query = "SELECT user_id FROM users WHERE username = ?"
            existing = db.execute_query(check_query, ("admin",), fetch=True)

            if existing:
                print("✓ Tài khoản admin đã tồn tại")
                return

            # Create admin user
            password_hash = hash_password("123456")
            insert_query = """
                INSERT INTO users (username, email, password_hash, fullname, phone, address)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            result = db.execute_query(
                insert_query,
                (
                    "admin",
                    "admin@phonebook.com",
                    password_hash,
                    "Administrator",
                    None,
                    None,
                ),
            )

            if result and result["last_id"]:
                print("✓ Đã tạo tài khoản admin mặc định")
            else:
                print("⚠️ Không thể tạo tài khoản admin")

        except Exception as e:
            print(f"⚠️ Lỗi tạo admin: {e}")

    def start(self):
        """Start the application"""
        # Initialize database
        if not self.initialize_database():
            return

        # Create main window
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(APP_WINDOW_SIZE)
        self.root.configure(bg=COLORS["bg"])

        # Center window on screen
        self.center_window()

        # Show login view
        self.show_login()

        # Start main loop
        self.root.mainloop()

    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Calculate position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"+{x}+{y}")

    def show_login(self):
        """Show login view"""
        # Clear current view
        if self.current_view:
            self.current_view.destroy()

        # Import and show login view
        from views.login_view import LoginView

        self.current_view = LoginView(
            self.root, self.on_login_success, self.show_register
        )

    def show_register(self):
        """Show register view"""
        # Clear current view
        if self.current_view:
            self.current_view.destroy()

        # Import and show register view
        from views.register_view import RegisterView

        self.current_view = RegisterView(
            self.root, self.on_register_success, self.show_login
        )

    def on_login_success(self, user_data):
        """
        Handle successful login

        Args:
            user_data (dict): User data from database
        """
        self.current_user = user_data
        log_info(f"User logged in: {user_data['username']}")
        self.show_dashboard()

    def on_register_success(self):
        """Handle successful registration"""
        messagebox.showinfo(
            "Thành công", "Đăng ký thành công!\nVui lòng đăng nhập để sử dụng ứng dụng."
        )
        self.show_login()

    def show_dashboard(self):
        """Show dashboard view"""
        # Clear current view
        if self.current_view:
            self.current_view.destroy()

        # Import and show dashboard view
        from views.dashboard_view import DashboardView

        self.current_view = DashboardView(
            self.root, self.current_user, self.on_logout, self.switch_view
        )

    def switch_view(self, view_name):
        """
        Switch to a different view

        Args:
            view_name (str): Name of the view to switch to
        """
        # Clear current view
        if self.current_view:
            self.current_view.destroy()

        # Import and show requested view
        if view_name == "dashboard":
            from views.dashboard_view import DashboardView

            self.current_view = DashboardView(
                self.root, self.current_user, self.on_logout, self.switch_view
            )

        elif view_name == "contacts":
            from views.contact_view import ContactView

            self.current_view = ContactView(
                self.root, self.current_user, self.on_logout, self.switch_view
            )

        elif view_name == "groups":
            from views.group_view import GroupView

            self.current_view = GroupView(
                self.root, self.current_user, self.on_logout, self.switch_view
            )

        elif view_name == "tags":
            from views.tag_view import TagView

            self.current_view = TagView(
                self.root, self.current_user, self.on_logout, self.switch_view
            )

        elif view_name == "trash":
            from views.trash_view import TrashView

            self.current_view = TrashView(
                self.root, self.current_user, self.on_logout, self.switch_view
            )

        elif view_name == "profile":
            from views.profile_view import ProfileView

            self.current_view = ProfileView(
                self.root,
                self.current_user,
                self.on_logout,
                self.switch_view,
                self.on_profile_update,
            )

    def on_profile_update(self, updated_user):
        """
        Handle profile update

        Args:
            updated_user (dict): Updated user data
        """
        self.current_user = updated_user
        log_info(f"Profile updated: {updated_user['username']}")

    def on_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            log_info(f"User logged out: {self.current_user['username']}")
            self.current_user = None
            self.show_login()

    def cleanup(self):
        """Cleanup resources"""
        db.close()
        log_info("Application closed")


def main():
    """Main entry point"""
    app = PhoneBookApp()

    try:
        app.start()
    except KeyboardInterrupt:
        print("\nĐã dừng ứng dụng")
    except Exception as e:
        error_msg = f"Lỗi nghiêm trọng: {str(e)}"
        log_error(error_msg)
        print(f"\n{error_msg}")
    finally:
        app.cleanup()


if __name__ == "__main__":
    main()
