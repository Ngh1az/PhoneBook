"""
Login View for PhoneBook Application
"""

import tkinter as tk
from config import COLORS, FONTS
from controllers.auth_controller import AuthController
from views.components import show_error


class LoginView(tk.Frame):
    """Login view class"""

    def __init__(self, parent, on_login_success, on_show_register):
        super().__init__(parent, bg=COLORS["bg"])
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_show_register = on_show_register
        self.auth_controller = AuthController()

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        """Create simple login form"""
        # Center container
        container = tk.Frame(self, bg=COLORS["bg"])
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(
            container,
            text="ĐĂNG NHẬP",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 30))

        # Form frame
        form_frame = tk.Frame(container, bg=COLORS["white"], padx=40, pady=30)
        form_frame.pack()

        # Username
        tk.Label(
            form_frame,
            text="Tên đăng nhập:",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.username_entry = tk.Entry(form_frame, font=FONTS["normal"], width=30)
        self.username_entry.grid(row=1, column=0, pady=(0, 15))
        self.username_entry.focus()

        # Password
        tk.Label(
            form_frame,
            text="Mật khẩu:",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))

        self.password_entry = tk.Entry(
            form_frame, font=FONTS["normal"], width=30, show="●"
        )
        self.password_entry.grid(row=3, column=0, pady=(0, 20))

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

        # Login button
        tk.Button(
            form_frame,
            text="Đăng nhập",
            font=FONTS["button"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
            cursor="hand2",
            width=25,
            command=self.handle_login,
        ).grid(row=4, column=0, pady=(0, 10))

        # Register link
        register_frame = tk.Frame(form_frame, bg=COLORS["white"])
        register_frame.grid(row=5, column=0)

        tk.Label(
            register_frame,
            text="Chưa có tài khoản?",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).pack(side=tk.LEFT)

        register_link = tk.Label(
            register_frame,
            text="Đăng ký ngay",
            font=FONTS["normal"],
            bg=COLORS["white"],
            fg=COLORS["info"],
            cursor="hand2",
        )
        register_link.pack(side=tk.LEFT, padx=(5, 0))
        register_link.bind("<Button-1>", lambda e: self.on_show_register())

    def old_create_widgets(self):
        """Create login form widgets with modern minimal design"""
        # Main container with centered card
        main_container = tk.Frame(self, bg=COLORS["bg"])
        main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Card container with shadow effect (using multiple frames)
        shadow_frame = tk.Frame(main_container, bg=COLORS["border"], padx=2, pady=2)
        shadow_frame.pack()

        card = tk.Frame(shadow_frame, bg=COLORS["card"], padx=50, pady=40)
        card.pack()

        # App branding
        brand_frame = tk.Frame(card, bg=COLORS["card"])
        brand_frame.pack(pady=(0, 30))

        tk.Label(
            brand_frame,
            text="📱",
            font=("Segoe UI", 36),
            bg=COLORS["card"],
        ).pack()

        tk.Label(
            brand_frame,
            text="PhoneBook",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["card"],
            fg=COLORS["text_primary"],
        ).pack(pady=(5, 0))

        tk.Label(
            brand_frame,
            text="Đăng nhập vào tài khoản của bạn",
            font=FONTS["label"],
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
        ).pack(pady=(5, 0))

        # Form container
        form_frame = tk.Frame(card, bg=COLORS["card"])
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Username field
        username_frame = tk.Frame(form_frame, bg=COLORS["card"])
        username_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            username_frame,
            text="Tên đăng nhập",
            font=FONTS["label"],
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor=tk.W)

        username_container = tk.Frame(
            username_frame, bg=COLORS["input_border"], padx=1, pady=1
        )
        username_container.pack(fill=tk.X, pady=(8, 0))

        self.username_entry = tk.Entry(
            username_container,
            font=FONTS["normal"],
            bg=COLORS["input_bg"],
            fg=COLORS["input_text"],
            relief=tk.FLAT,
            highlightthickness=0,
            insertbackground=COLORS["text_primary"],
        )
        self.username_entry.pack(fill=tk.BOTH, padx=12, pady=10, ipady=4)
        self.username_entry.focus()

        # Focus effects for username
        def on_username_focus_in(e):
            username_container.config(bg=COLORS["input_focus"], padx=2, pady=2)

        def on_username_focus_out(e):
            username_container.config(bg=COLORS["input_border"], padx=1, pady=1)

        self.username_entry.bind("<FocusIn>", on_username_focus_in)
        self.username_entry.bind("<FocusOut>", on_username_focus_out)

        # Password field
        password_frame = tk.Frame(form_frame, bg=COLORS["card"])
        password_frame.pack(fill=tk.X, pady=(0, 25))

        tk.Label(
            password_frame,
            text="Mật khẩu",
            font=FONTS["label"],
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
        ).pack(anchor=tk.W)

        password_container = tk.Frame(
            password_frame, bg=COLORS["input_border"], padx=1, pady=1
        )
        password_container.pack(fill=tk.X, pady=(8, 0))

        self.password_entry = tk.Entry(
            password_container,
            font=FONTS["normal"],
            bg=COLORS["input_bg"],
            fg=COLORS["input_text"],
            relief=tk.FLAT,
            highlightthickness=0,
            show="●",
            insertbackground=COLORS["text_primary"],
        )
        self.password_entry.pack(fill=tk.BOTH, padx=12, pady=10, ipady=4)

        # Focus effects for password
        def on_password_focus_in(e):
            password_container.config(bg=COLORS["input_focus"], padx=2, pady=2)

        def on_password_focus_out(e):
            password_container.config(bg=COLORS["input_border"], padx=1, pady=1)

        self.password_entry.bind("<FocusIn>", on_password_focus_in)
        self.password_entry.bind("<FocusOut>", on_password_focus_out)

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

        # Login button with hover effect
        self.login_btn = tk.Button(
            form_frame,
            text="Đăng nhập",
            font=FONTS["button"],
            bg=COLORS["accent"],
            fg=COLORS["text_white"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_white"],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.handle_login,
        )
        self.login_btn.pack(fill=tk.X, ipady=10)

        # Hover effects for button
        self.login_btn.bind(
            "<Enter>", lambda e: self.login_btn.config(bg=COLORS["accent_hover"])
        )
        self.login_btn.bind(
            "<Leave>", lambda e: self.login_btn.config(bg=COLORS["accent"])
        )

        # Divider
        divider_frame = tk.Frame(form_frame, bg=COLORS["card"])
        divider_frame.pack(fill=tk.X, pady=25)

        tk.Frame(divider_frame, bg=COLORS["border"], height=1).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        tk.Label(
            divider_frame,
            text="HOẶC",
            font=FONTS["small"],
            bg=COLORS["card"],
            fg=COLORS["text_muted"],
        ).pack(side=tk.LEFT, padx=15)
        tk.Frame(divider_frame, bg=COLORS["border"], height=1).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )

        # Register section
        register_frame = tk.Frame(form_frame, bg=COLORS["card"])
        register_frame.pack()

        tk.Label(
            register_frame,
            text="Chưa có tài khoản?",
            font=FONTS["normal"],
            bg=COLORS["card"],
            fg=COLORS["text_secondary"],
        ).pack(side=tk.LEFT)

        register_link = tk.Label(
            register_frame,
            text="Đăng ký ngay",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["card"],
            fg=COLORS["accent"],
            cursor="hand2",
        )
        register_link.pack(side=tk.LEFT, padx=(5, 0))
        register_link.bind("<Button-1>", lambda e: self.on_show_register())
        register_link.bind(
            "<Enter>", lambda e: register_link.config(fg=COLORS["accent_hover"])
        )
        register_link.bind(
            "<Leave>", lambda e: register_link.config(fg=COLORS["accent"])
        )

    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            show_error("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        success, result = self.auth_controller.login(username, password)

        if success:
            self.on_login_success(result)
        else:
            show_error("Đăng nhập thất bại", result)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
