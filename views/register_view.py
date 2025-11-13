"""
Register View for PhoneBook Application
"""

import tkinter as tk
from config import COLORS, FONTS
from controllers.auth_controller import AuthController
from views.components import show_error, show_info


class RegisterView(tk.Frame):
    """Register view class"""

    def __init__(self, parent, on_register_success, on_show_login):
        super().__init__(parent, bg=COLORS["bg"])
        self.parent = parent
        self.on_register_success = on_register_success
        self.on_show_login = on_show_login
        self.auth_controller = AuthController()

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        """Create simple register form - giống login view"""
        # Center container - giống y hệt login
        container = tk.Frame(self, bg=COLORS["bg"])
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(
            container,
            text="ĐĂNG KÝ TÀI KHOẢN",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 30))

        # Form frame
        form_frame = tk.Frame(container, bg=COLORS["white"], padx=40, pady=30)
        form_frame.pack()

        # Fullname
        tk.Label(
            form_frame,
            text="Họ và tên: *",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.fullname_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.fullname_entry.grid(row=1, column=0, pady=(0, 15))
        self.fullname_entry.focus()

        # Username
        tk.Label(
            form_frame,
            text="Tên đăng nhập: *",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))

        self.username_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.username_entry.grid(row=3, column=0, pady=(0, 15))

        # Email
        tk.Label(
            form_frame,
            text="Email: *",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))

        self.email_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.email_entry.grid(row=5, column=0, pady=(0, 15))

        # Phone
        tk.Label(
            form_frame,
            text="Số điện thoại:",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))

        self.phone_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.phone_entry.grid(row=7, column=0, pady=(0, 15))

        # Address
        tk.Label(
            form_frame,
            text="Địa chỉ:",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=8, column=0, sticky=tk.W, pady=(0, 5))

        self.address_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.address_entry.grid(row=9, column=0, pady=(0, 15))

        # Password
        tk.Label(
            form_frame,
            text="Mật khẩu: *",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=10, column=0, sticky=tk.W, pady=(0, 5))

        self.password_entry = tk.Entry(
            form_frame, font=FONTS["normal"], width=30, show="●"
        )
        self.password_entry.grid(row=11, column=0, pady=(0, 15))

        # Confirm Password
        tk.Label(
            form_frame,
            text="Xác nhận mật khẩu: *",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=12, column=0, sticky=tk.W, pady=(0, 5))

        self.confirm_password_entry = tk.Entry(
            form_frame, font=FONTS["normal"], width=30, show="●"
        )
        self.confirm_password_entry.grid(row=13, column=0, pady=(0, 20))

        # Register button
        tk.Button(
            form_frame,
            text="Đăng ký",
            font=FONTS["button"],
            bg=COLORS["success"],
            fg=COLORS["white"],
            cursor="hand2",
            width=25,
            command=self.handle_register,
        ).grid(row=14, column=0, pady=(0, 10))

        # Login link
        login_frame = tk.Frame(form_frame, bg=COLORS["white"])
        login_frame.grid(row=15, column=0)

        tk.Label(
            login_frame,
            text="Đã có tài khoản?",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).pack(side=tk.LEFT)

        login_link = tk.Label(
            login_frame,
            text="Đăng nhập",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["info"],
            cursor="hand2",
        )
        login_link.pack(side=tk.LEFT, padx=(5, 0))
        login_link.bind("<Button-1>", lambda e: self.on_show_login())

    def handle_register(self):
        """Handle register button click"""
        fullname = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        success, message = self.auth_controller.register(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password,
            fullname=fullname,
            phone=phone if phone else None,
            address=address if address else None,
        )

        if success:
            show_info("Thành công", message)
            self.on_register_success()
        else:
            show_error("Đăng ký thất bại", message)
