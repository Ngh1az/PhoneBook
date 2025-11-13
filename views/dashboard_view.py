"""
Dashboard View for PhoneBook Application
"""

import tkinter as tk
from tkinter import ttk, filedialog
from config import COLORS, FONTS
from controllers.dashboard_controller import DashboardController
from controllers.contact_controller import ContactController
from views.components.messagebox_custom import (
    show_error,
    show_success,
    show_info,
    ask_yes_no,
)


class DashboardView(tk.Frame):
    """Dashboard view class"""

    def __init__(self, parent, user_data, on_logout, on_switch_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout
        self.on_switch_view = on_switch_view
        self.dashboard_controller = DashboardController(user_data["user_id"])
        self.contact_controller = ContactController(user_data["user_id"])

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_statistics()

    def create_widgets(self):
        """Create dashboard widgets"""
        # Top bar
        top_bar = tk.Frame(self, bg=COLORS["primary"], height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        # App title
        tk.Label(
            top_bar,
            text="📞 PHONEBOOK",
            font=FONTS["title"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(side=tk.LEFT, padx=20)

        # User info
        user_frame = tk.Frame(top_bar, bg=COLORS["primary"])
        user_frame.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            user_frame,
            text=f"Xin chào, {self.user_data['fullname']}",
            font=FONTS["normal"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(side=tk.LEFT, padx=(0, 10))

        logout_btn = tk.Button(
            user_frame,
            text="Đăng xuất",
            font=FONTS["small"],
            bg=COLORS["danger"],
            fg=COLORS["white"],
            cursor="hand2",
            command=self.on_logout,
        )
        logout_btn.pack(side=tk.LEFT)

        # Main content
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title with welcome message
        title_frame = tk.Frame(content, bg=COLORS["bg"])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🏠 TRANG CHỦ",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT)
        
        tk.Label(
            title_frame,
            font=("Segoe UI", 11),
            bg=COLORS["bg"],
            fg=COLORS["text"],
        ).pack(side=tk.RIGHT, pady=5)

        # Statistics cards - redesigned with icons and better layout
        stats_frame = tk.Frame(content, bg=COLORS["bg"])
        stats_frame.pack(fill=tk.X, pady=(0, 25))

        # Contacts card
        self.contacts_card = self.create_stat_card(
            stats_frame, "📇 Liên hệ", "0", COLORS["info"], "Tổng số"
        )
        self.contacts_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))

        # Groups card
        self.groups_card = self.create_stat_card(
            stats_frame, "📁 Nhóm", "0", COLORS["success"], "Tổng số"
        )
        self.groups_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))

        # Tags card
        self.tags_card = self.create_stat_card(
            stats_frame, "🏷️ Thẻ", "0", COLORS["warning"], "Tổng số"
        )
        self.tags_card.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Main content area - 2 columns layout
        main_area = tk.Frame(content, bg=COLORS["bg"])
        main_area.pack(fill=tk.BOTH, expand=True)

        # LEFT COLUMN - Recent Activity
        left_column = tk.Frame(main_area, bg=COLORS["bg"])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Recent activity header
        activity_header = tk.Frame(left_column, bg=COLORS["bg"])
        activity_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            activity_header,
            text="📊 Hoạt động gần đây",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT)

        # Recent contacts
        recent_contacts_frame = tk.LabelFrame(
            left_column,
            text="  📇 5 Liên hệ mới nhất  ",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["white"],
            fg=COLORS["info"],
            padx=15,
            pady=15,
            relief=tk.RIDGE,
            borderwidth=2,
        )
        recent_contacts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.recent_contacts_list = tk.Listbox(
            recent_contacts_frame,
            font=("Segoe UI", 10),
            bg=COLORS["white"],
            fg=COLORS["text"],
            height=6,
            relief=tk.FLAT,
            selectbackground=COLORS["info"],
            activestyle="none",
        )
        self.recent_contacts_list.pack(fill=tk.BOTH, expand=True)

        # Top groups and tags in same row
        stats_row = tk.Frame(left_column, bg=COLORS["bg"])
        stats_row.pack(fill=tk.BOTH, expand=True)

        # Top groups
        top_groups_frame = tk.LabelFrame(
            stats_row,
            text="  📁 Nhóm phổ biến  ",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["white"],
            fg=COLORS["success"],
            padx=15,
            pady=15,
            relief=tk.RIDGE,
            borderwidth=2,
        )
        top_groups_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.top_groups_list = tk.Listbox(
            top_groups_frame,
            font=("Segoe UI", 9),
            bg=COLORS["white"],
            fg=COLORS["text"],
            height=5,
            relief=tk.FLAT,
            selectbackground=COLORS["success"],
            activestyle="none",
        )
        self.top_groups_list.pack(fill=tk.BOTH, expand=True)

        # Top tags
        top_tags_frame = tk.LabelFrame(
            stats_row,
            text="  🏷️ Thẻ phổ biến  ",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["white"],
            fg=COLORS["warning"],
            padx=15,
            pady=15,
            relief=tk.RIDGE,
            borderwidth=2,
        )
        top_tags_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.top_tags_list = tk.Listbox(
            top_tags_frame,
            font=("Segoe UI", 9),
            bg=COLORS["white"],
            fg=COLORS["text"],
            height=5,
            relief=tk.FLAT,
            selectbackground=COLORS["warning"],
            activestyle="none",
        )
        self.top_tags_list.pack(fill=tk.BOTH, expand=True)

        # RIGHT COLUMN - Quick Actions
        right_column = tk.Frame(main_area, bg=COLORS["bg"], width=350)
        right_column.pack(side=tk.LEFT, fill=tk.Y)
        right_column.pack_propagate(False)

        # Quick actions header
        actions_header = tk.Frame(right_column, bg=COLORS["bg"])
        actions_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            actions_header,
            text="⚡ Thao tác nhanh",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT)

        # Quick actions container
        actions_container = tk.Frame(right_column, bg=COLORS["white"], relief=tk.RIDGE, borderwidth=2)
        actions_container.pack(fill=tk.BOTH, expand=True)
        
        actions_inner = tk.Frame(actions_container, bg=COLORS["white"], padx=15, pady=15)
        actions_inner.pack(fill=tk.BOTH, expand=True)

        # Action buttons - vertical layout for better visibility
        actions = [
            ("📇 Quản lý liên hệ", lambda: self.on_switch_view("contacts"), COLORS["info"]),
            ("📁 Quản lý nhóm", lambda: self.on_switch_view("groups"), COLORS["success"]),
            ("🏷️ Quản lý thẻ", lambda: self.on_switch_view("tags"), COLORS["warning"]),
            ("🗑️ Thùng rác", lambda: self.on_switch_view("trash"), COLORS["danger"]),
            ("👤 Hồ sơ cá nhân", lambda: self.on_switch_view("profile"), COLORS["primary"]),
        ]

        for text, command, color in actions:
            btn_frame = tk.Frame(actions_inner, bg=COLORS["white"])
            btn_frame.pack(fill=tk.X, pady=(0, 10))
            
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg=color,
                fg=COLORS["white"],
                cursor="hand2",
                relief=tk.FLAT,
                padx=20,
                pady=12,
                command=command,
                activebackground=color,
                activeforeground=COLORS["white"],
            )
            btn.pack(fill=tk.X)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.FLAT))

        # Separator
        separator = tk.Frame(actions_inner, bg=COLORS["bg"], height=2)
        separator.pack(fill=tk.X, pady=15)

        # Import/Export section
        tk.Label(
            actions_inner,
            text="� Sao lưu & Khôi phục",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["white"],
            fg=COLORS["text"],
        ).pack(anchor=tk.W, pady=(0, 10))

        backup_actions = [
            ("📤 Xuất ra CSV", self.export_to_csv, "#3498db"),
            ("📥 Nhập từ CSV", self.import_from_csv, "#27ae60"),
            ("➕ Thêm nhanh liên hệ", self.quick_add_contact, "#f39c12"),
        ]

        for text, command, color in backup_actions:
            btn_frame = tk.Frame(actions_inner, bg=COLORS["white"])
            btn_frame.pack(fill=tk.X, pady=(0, 8))
            
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Segoe UI", 10),
                bg=color,
                fg=COLORS["white"],
                cursor="hand2",
                relief=tk.FLAT,
                padx=15,
                pady=10,
                command=command,
                activebackground=color,
                activeforeground=COLORS["white"],
            )
            btn.pack(fill=tk.X)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.FLAT))

    def create_stat_card(self, parent, title, value, color, subtitle=""):
        """Create a statistics card with modern design"""
        card = tk.Frame(parent, bg=COLORS["white"], relief=tk.RIDGE, borderwidth=2)
        card_inner = tk.Frame(card, bg=color, padx=25, pady=20)
        card_inner.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Subtitle
        if subtitle:
            tk.Label(
                card_inner, 
                text=subtitle, 
                font=("Segoe UI", 9), 
                bg=color, 
                fg=COLORS["white"],
                anchor=tk.W,
            ).pack(fill=tk.X)

        # Title
        tk.Label(
            card_inner, 
            text=title, 
            font=("Segoe UI", 12, "bold"), 
            bg=color, 
            fg=COLORS["white"],
            anchor=tk.W,
        ).pack(fill=tk.X, pady=(0, 5))

        value_label = tk.Label(
            card_inner,
            text=value,
            font=("Segoe UI", 24, "bold"),
            bg=color,
            fg=COLORS["white"],
        )
        value_label.pack(pady=(5, 0))

        card.value_label = value_label
        return card

    def load_statistics(self):
        """Load and display statistics"""
        stats = self.dashboard_controller.get_statistics()

        self.contacts_card.value_label.config(text=str(stats["total_contacts"]))
        self.groups_card.value_label.config(text=str(stats["total_groups"]))
        self.tags_card.value_label.config(text=str(stats["total_tags"]))

        # Load recent contacts
        self.recent_contacts_list.delete(0, tk.END)
        recent_contacts = stats.get("recent_contacts", [])
        if recent_contacts:
            for contact in recent_contacts:
                first_name = contact.get("first_name", "")
                last_name = contact.get("last_name", "")
                name = f"{first_name} {last_name}".strip() or "N/A"
                phone = contact.get("phone", "N/A")
                self.recent_contacts_list.insert(tk.END, f"  {name} - {phone}")
        else:
            self.recent_contacts_list.insert(tk.END, "  Chưa có liên hệ nào")

        # Load top groups
        self.top_groups_list.delete(0, tk.END)
        top_groups = stats.get("top_groups", [])
        if top_groups:
            for group in top_groups:
                name = group.get("group_name", "N/A")
                count = group.get("contact_count", 0)
                self.top_groups_list.insert(tk.END, f"  {name} ({count} liên hệ)")
        else:
            self.top_groups_list.insert(tk.END, "  Chưa có nhóm nào")

        # Load top tags
        self.top_tags_list.delete(0, tk.END)
        top_tags = stats.get("top_tags", [])
        if top_tags:
            for tag in top_tags:
                name = tag.get("tag_name", "N/A")
                count = tag.get("usage_count", 0)
                self.top_tags_list.insert(tk.END, f"  {name} ({count} lần dùng)")
        else:
            self.top_tags_list.insert(tk.END, "  Chưa có thẻ nào")

    def export_to_csv(self):
        """Export all contacts to CSV"""
        contacts = self.contact_controller.get_all_contacts()

        if not contacts:
            show_info("Thông báo", "Không có liên hệ nào để xuất")
            return

        success, result = self.contact_controller.export_contacts_to_csv(contacts)

        if success:
            show_success(
                f"Đã xuất {len(contacts)} liên hệ ra file CSV!\n\nĐường dẫn: {result}"
            )
        else:
            show_error("Lỗi", result)

    def import_from_csv(self):
        """Import contacts from CSV"""
        filepath = filedialog.askopenfilename(
            title="Chọn file CSV để nhập",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if not filepath:
            return

        if ask_yes_no(
            "Xác nhận",
            "Bạn có chắc muốn nhập liên hệ từ file CSV?\nCác số điện thoại trùng lặp sẽ bị bỏ qua.",
        ):
            success, result = self.contact_controller.import_contacts_from_csv(filepath)

            if success:
                imported = result.get("imported", 0)
                skipped = result.get("skipped", 0)
                errors = result.get("errors", [])

                message = f"Đã nhập: {imported} liên hệ\nBỏ qua: {skipped} liên hệ"

                if errors and len(errors) > 0:
                    message += f"\n\nLỗi ({len(errors)}):\n" + "\n".join(errors[:5])
                    if len(errors) > 5:
                        message += f"\n... và {len(errors) - 5} lỗi khác"

                show_info("Kết quả nhập dữ liệu", message)
                self.load_statistics()
            else:
                show_error("Lỗi", result)

    def quick_add_contact(self):
        """Quick add contact dialog"""
        from controllers.group_controller import GroupController

        dialog = tk.Toplevel(self)
        dialog.title("Thêm nhanh liên hệ")
        dialog.geometry("400x450")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"+{x}+{y}")

        form = tk.Frame(dialog, bg=COLORS["white"], padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(
            form,
            text="THÊM NHANH LIÊN HỆ",
            font=FONTS["heading"],
            bg=COLORS["white"],
            fg=COLORS["primary"],
        ).grid(row=0, column=0, pady=(0, 20))

        fields = {}
        row = 1

        for label, key in [
            ("Tên:", "first_name"),
            ("Họ:", "last_name"),
            ("Số điện thoại:", "phone"),
            ("Email:", "email"),
        ]:
            tk.Label(form, text=label, font=FONTS["normal"], bg=COLORS["white"]).grid(
                row=row, column=0, sticky=tk.W, pady=(0, 5)
            )
            entry = tk.Entry(form, font=FONTS["normal"], width=30)
            entry.grid(row=row + 1, column=0, pady=(0, 10))
            fields[key] = entry
            row += 2

        # Group dropdown
        tk.Label(form, text="Nhóm:", font=FONTS["normal"], bg=COLORS["white"]).grid(
            row=row, column=0, sticky=tk.W, pady=(0, 5)
        )

        group_controller = GroupController(self.user_data["user_id"])
        groups = group_controller.get_all_groups()
        group_options = ["-- Không chọn --"] + [g["group_name"] for g in groups]
        group_var = tk.StringVar(value=group_options[0])

        group_dropdown = ttk.Combobox(
            form,
            textvariable=group_var,
            values=group_options,
            state="readonly",
            font=FONTS["normal"],
            width=28,
        )
        group_dropdown.grid(row=row + 1, column=0, pady=(0, 20))

        fields["first_name"].focus()

        def save_contact():
            # Find group_id from selected group name
            group_id = None
            selected_group = group_var.get()
            if selected_group != "-- Không chọn --":
                for g in groups:
                    if g["group_name"] == selected_group:
                        group_id = g["group_id"]
                        break

            success, result = self.contact_controller.add_contact(
                first_name=fields["first_name"].get().strip(),
                last_name=fields["last_name"].get().strip(),
                phone=fields["phone"].get().strip(),
                email=fields["email"].get().strip() or None,
                group_id=group_id,
            )

            if success:
                show_info("Thành công", "Đã thêm liên hệ mới")
                dialog.destroy()
                self.load_statistics()
            else:
                show_error("Lỗi", result)

        tk.Button(
            form,
            text="Lưu",
            font=FONTS["button"],
            bg=COLORS["success"],
            fg=COLORS["white"],
            cursor="hand2",
            width=15,
            command=save_contact,
        ).grid(row=row + 2, column=0, pady=(10, 0))
