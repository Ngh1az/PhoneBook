"""
Trash View - Deleted Contacts Management
"""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS
from controllers.trash_controller import TrashController
from views.components.messagebox_custom import show_error, show_success, ask_yes_no


class TrashView(tk.Frame):
    def __init__(self, parent, user_data, on_logout, on_switch_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.user_data = user_data
        self.on_logout = on_logout
        self.on_switch_view = on_switch_view
        self.controller = TrashController(user_data["user_id"])

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_deleted_contacts()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=COLORS["bg"])
        header_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(
            header_frame,
            text="THÙNG RÁC",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT)

        tk.Button(
            header_frame,
            text="Về trang chủ",
            command=lambda: self.on_switch_view("dashboard"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            font=FONTS["button"],
        ).pack(side=tk.RIGHT)

        # Deleted contacts list with scrollbar
        list_frame = tk.Frame(self, bg=COLORS["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Treeview
        columns = ("Họ", "Tên", "Số điện thoại", "Email", "Nhóm", "Ngày xóa")
        self.tree = ttk.Treeview(
            list_frame, columns=columns, show="headings", height=15
        )

        self.tree.heading("Họ", text="Họ")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Số điện thoại", text="Số điện thoại")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Nhóm", text="Nhóm")
        self.tree.heading("Ngày xóa", text="Ngày xóa")

        self.tree.column("Họ", width=100)
        self.tree.column("Tên", width=100)
        self.tree.column("Số điện thoại", width=120)
        self.tree.column("Email", width=180)
        self.tree.column("Nhóm", width=120)
        self.tree.column("Ngày xóa", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Action buttons
        action_frame = tk.Frame(self, bg=COLORS["bg"])
        action_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            action_frame,
            text="Khôi phục",
            command=self.restore_contact,
            bg=COLORS["success"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Xóa vĩnh viễn",
            command=self.delete_permanently,
            bg=COLORS["danger"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Làm trống thùng rác",
            command=self.empty_trash,
            bg=COLORS["danger"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=15,
        ).pack(side=tk.LEFT, padx=5)

    def load_deleted_contacts(self):
        """Load deleted contacts from database"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        contacts = self.controller.get_deleted_contacts()
        for contact in contacts:
            deleted_at = contact.get("deleted_at", "")
            if deleted_at and hasattr(deleted_at, "strftime"):
                deleted_at = deleted_at.strftime("%Y-%m-%d %H:%M:%S")

            self.tree.insert(
                "",
                tk.END,
                values=(
                    contact.get("first_name", ""),
                    contact.get("last_name", ""),
                    contact.get("phone", ""),
                    contact.get("email", ""),
                    contact.get("group_name", ""),
                    deleted_at,
                ),
                tags=(contact["contact_id"],),
            )

    def restore_contact(self):
        """Restore selected contact"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn liên hệ cần khôi phục")
            return

        item = self.tree.item(selected[0])
        contact_id = item["tags"][0]
        contact_name = f"{item['values'][0]} {item['values'][1]}"

        if ask_yes_no(
            "Xác nhận", f"Bạn có chắc muốn khôi phục liên hệ '{contact_name}'?"
        ):
            success, message = self.controller.restore_contact(contact_id)

            if success:
                show_success(message)
                self.load_deleted_contacts()
            else:
                show_error("Lỗi", message)

    def delete_permanently(self):
        """Delete selected contact permanently"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn liên hệ cần xóa vĩnh viễn")
            return

        item = self.tree.item(selected[0])
        contact_id = item["tags"][0]
        contact_name = f"{item['values'][0]} {item['values'][1]}"

        if ask_yes_no(
            "Xác nhận",
            f"Bạn có chắc muốn xóa vĩnh viễn liên hệ '{contact_name}'?\nHành động này không thể hoàn tác!",
        ):
            success, message = self.controller.permanent_delete(contact_id)

            if success:
                show_success(message)
                self.load_deleted_contacts()
            else:
                show_error("Lỗi", message)

    def empty_trash(self):
        """Empty entire trash"""
        if ask_yes_no(
            "Xác nhận",
            "Bạn có chắc muốn làm trống thùng rác?\nTất cả liên hệ sẽ bị xóa vĩnh viễn và không thể khôi phục!",
        ):
            success, message = self.controller.empty_trash()

            if success:
                show_success(message)
                self.load_deleted_contacts()
            else:
                show_error("Lỗi", message)
