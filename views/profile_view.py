"""
Profile View - User Profile Management
"""

import tkinter as tk
from config import COLORS, FONTS
from controllers.profile_controller import ProfileController
from views.components.messagebox_custom import show_error, show_success


class ProfileView(tk.Frame):
    def __init__(self, parent, user_data, on_logout, on_switch_view, on_profile_update):
        super().__init__(parent, bg=COLORS["bg"])
        self.user_data = user_data
        self.on_logout = on_logout
        self.on_switch_view = on_switch_view
        self.on_profile_update = on_profile_update
        self.controller = ProfileController(user_data["user_id"])

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Main container centered
        container = tk.Frame(self, bg=COLORS["bg"])
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(
            container,
            text="HỒ SƠ CÁ NHÂN",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 30))

        # Profile Form
        form_frame = tk.Frame(container, bg=COLORS["bg"])
        form_frame.pack(padx=40, pady=20)

        # Fullname
        tk.Label(
            form_frame, text="Họ và tên:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.fullname_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.fullname_entry.grid(row=0, column=1, pady=10, padx=(10, 0))
        self.fullname_entry.insert(0, self.user_data["fullname"])

        # Username (readonly)
        tk.Label(
            form_frame, text="Tên đăng nhập:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=1, column=0, sticky=tk.W, pady=10)
        username_display = tk.Entry(
            form_frame, font=FONTS["normal"], width=30, state="readonly"
        )
        username_display.grid(row=1, column=1, pady=10, padx=(10, 0))
        username_display.config(state="normal")
        username_display.insert(0, self.user_data["username"])
        username_display.config(state="readonly")

        # Email
        tk.Label(form_frame, text="Email:", font=FONTS["normal"], bg=COLORS["bg"]).grid(
            row=2, column=0, sticky=tk.W, pady=10
        )
        self.email_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.email_entry.grid(row=2, column=1, pady=10, padx=(10, 0))
        self.email_entry.insert(0, self.user_data["email"])

        # Phone
        tk.Label(
            form_frame, text="Số điện thoại:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.phone_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.phone_entry.grid(row=3, column=1, pady=10, padx=(10, 0))
        if self.user_data.get("phone"):
            self.phone_entry.insert(0, self.user_data["phone"])

        # Address
        tk.Label(
            form_frame, text="Địa chỉ:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=4, column=0, sticky=tk.W, pady=10)
        self.address_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.address_entry.grid(row=4, column=1, pady=10, padx=(10, 0))
        if self.user_data.get("address"):
            self.address_entry.insert(0, self.user_data["address"])

        # Buttons
        button_frame = tk.Frame(container, bg=COLORS["bg"])
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Cập nhật thông tin",
            command=self.update_profile,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Đổi mật khẩu",
            command=self.show_change_password_dialog,
            bg=COLORS["warning"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Về trang chủ",
            command=lambda: self.on_switch_view("dashboard"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

    def update_profile(self):
        """Update user profile information"""
        fullname = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        success, message = self.controller.update_profile(
            fullname=fullname,
            email=email,
            phone=phone if phone else None,
            address=address if address else None,
        )

        if success:
            show_success(message)
            # Update user data and notify parent
            updated_user = self.controller.get_profile()
            if updated_user:
                self.user_data = updated_user
                self.on_profile_update(updated_user)
        else:
            show_error("Lỗi", message)

    def show_change_password_dialog(self):
        """Show change password dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Đổi mật khẩu")
        dialog.geometry("400x300")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Title
        tk.Label(
            dialog,
            text="ĐỔI MẬT KHẨU",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=20)

        # Form
        form_frame = tk.Frame(dialog, bg=COLORS["bg"])
        form_frame.pack(padx=30)

        # Old password
        tk.Label(
            form_frame, text="Mật khẩu hiện tại:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=0, column=0, sticky=tk.W, pady=10)
        old_password_entry = tk.Entry(
            form_frame, font=FONTS["normal"], width=20, show="*"
        )
        old_password_entry.grid(row=0, column=1, pady=10, padx=(10, 0))

        # New password
        tk.Label(
            form_frame, text="Mật khẩu mới:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=1, column=0, sticky=tk.W, pady=10)
        new_password_entry = tk.Entry(
            form_frame, font=FONTS["normal"], width=20, show="*"
        )
        new_password_entry.grid(row=1, column=1, pady=10, padx=(10, 0))

        # Confirm password
        tk.Label(
            form_frame, text="Xác nhận mật khẩu:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=2, column=0, sticky=tk.W, pady=10)
        confirm_password_entry = tk.Entry(
            form_frame, font=FONTS["normal"], width=20, show="*"
        )
        confirm_password_entry.grid(row=2, column=1, pady=10, padx=(10, 0))

        # Buttons
        button_frame = tk.Frame(dialog, bg=COLORS["bg"])
        button_frame.pack(pady=20)

        def change_password():
            old_password = old_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            success, message = self.controller.change_password(
                old_password, new_password, confirm_password
            )

            if success:
                show_success(message)
                dialog.destroy()
            else:
                show_error("Lỗi", message)

        tk.Button(
            button_frame,
            text="Đổi mật khẩu",
            command=change_password,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=12,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Hủy",
            command=dialog.destroy,
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=12,
        ).pack(side=tk.LEFT, padx=5)
