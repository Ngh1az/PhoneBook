"""
Contact View for PhoneBook Application - Simplified version
"""

import tkinter as tk
from tkinter import ttk, filedialog
from config import COLORS, FONTS
from controllers.contact_controller import ContactController
from controllers.group_controller import GroupController
from controllers.tag_controller import TagController
from views.components import show_error, show_info, ask_yes_no
from views.components.messagebox_custom import show_success


class ContactView(tk.Frame):
    """Contact view class"""

    def __init__(self, parent, user_data, on_logout, on_switch_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout
        self.on_switch_view = on_switch_view
        self.contact_controller = ContactController(user_data["user_id"])
        self.group_controller = GroupController(user_data["user_id"])
        self.tag_controller = TagController(user_data["user_id"])

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_contacts()

    def create_widgets(self):
        """Create contact management widgets"""
        # Top bar
        self.create_top_bar()

        # Main content
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title and buttons
        header = tk.Frame(content, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            header,
            text="QUẢN LÝ LIÊN HỆ",
            font=FONTS["heading"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT)

        tk.Button(
            header,
            text="+ Thêm liên hệ",
            font=FONTS["button"],
            bg=COLORS["success"],
            fg=COLORS["white"],
            cursor="hand2",
            command=self.show_add_contact_dialog,
        ).pack(side=tk.RIGHT)

        tk.Button(
            header,
            text="📤 Xuất CSV",
            font=FONTS["button"],
            bg=COLORS["info"],
            fg=COLORS["white"],
            cursor="hand2",
            command=self.export_to_csv,
        ).pack(side=tk.RIGHT, padx=(0, 10))

        tk.Button(
            header,
            text="📥 Nhập CSV",
            font=FONTS["button"],
            bg=COLORS["warning"],
            fg=COLORS["white"],
            cursor="hand2",
            command=self.import_from_csv,
        ).pack(side=tk.RIGHT, padx=(0, 10))

        tk.Button(
            header,
            text="🏠 Trang chủ",
            font=FONTS["button"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
            cursor="hand2",
            command=lambda: self.on_switch_view("dashboard"),
        ).pack(side=tk.RIGHT, padx=(0, 10))

        # Search bar
        search_frame = tk.Frame(content, bg=COLORS["bg"])
        search_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            search_frame, text="Tìm kiếm:", font=FONTS["normal"], bg=COLORS["bg"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.search_entry = tk.Entry(search_frame, font=FONTS["normal"], width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_contacts())

        # Filter by group
        tk.Label(
            search_frame, text="Lọc theo nhóm:", font=FONTS["normal"], bg=COLORS["bg"]
        ).pack(side=tk.LEFT, padx=(10, 10))

        groups = self.group_controller.get_all_groups()
        group_options = ["-- Tất cả --"] + [g.get("group_name", "") for g in groups]
        self.filter_group_var = tk.StringVar(value=group_options[0])

        group_filter = ttk.Combobox(
            search_frame,
            textvariable=self.filter_group_var,
            values=group_options,
            state="readonly",
            font=FONTS["normal"],
            width=20,
        )
        group_filter.pack(side=tk.LEFT)
        group_filter.bind("<<ComboboxSelected>>", lambda e: self.load_contacts())

        # Filter by tag
        tk.Label(
            search_frame, text="Lọc theo thẻ:", font=FONTS["normal"], bg=COLORS["bg"]
        ).pack(side=tk.LEFT, padx=(10, 10))

        tags = self.tag_controller.get_all_tags()
        tag_options = ["-- Tất cả --"] + [t.get("tag_name", "") for t in tags]
        self.filter_tag_var = tk.StringVar(value=tag_options[0])

        tag_filter = ttk.Combobox(
            search_frame,
            textvariable=self.filter_tag_var,
            values=tag_options,
            state="readonly",
            font=FONTS["normal"],
            width=20,
        )
        tag_filter.pack(side=tk.LEFT)
        tag_filter.bind("<<ComboboxSelected>>", lambda e: self.load_contacts())

        # Contacts list
        list_frame = tk.Frame(content, bg=COLORS["white"])
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview (với selectmode extended để chọn nhiều)
        columns = ("name", "phone", "email", "group")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="tree headings",
            height=15,
            selectmode="extended",
        )

        self.tree.heading("#0", text="ID")
        self.tree.heading("name", text="Họ và tên")
        self.tree.heading("phone", text="Số điện thoại")
        self.tree.heading("email", text="Email")
        self.tree.heading("group", text="Nhóm")

        self.tree.column("#0", width=50)
        self.tree.column("name", width=200)
        self.tree.column("phone", width=150)
        self.tree.column("email", width=200)
        self.tree.column("group", width=150)

        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Context menu
        self.tree.bind("<Double-Button-1>", lambda e: self.show_edit_contact_dialog())
        self.tree.bind("<Delete>", lambda e: self.delete_contact())

        # Action buttons
        action_frame = tk.Frame(content, bg=COLORS["bg"])
        action_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            action_frame,
            text="Sửa",
            font=FONTS["button"],
            bg=COLORS["warning"],
            fg=COLORS["white"],
            cursor="hand2",
            width=12,
            command=self.show_edit_contact_dialog,
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            action_frame,
            text="Xóa",
            font=FONTS["button"],
            bg=COLORS["danger"],
            fg=COLORS["white"],
            cursor="hand2",
            width=12,
            command=self.delete_contact,
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            action_frame,
            text=" Xóa nhiều ",
            font=FONTS["button"],
            bg="#c0392b",  # Màu đỏ đậm hơn
            fg=COLORS["white"],
            cursor="hand2",
            width=18,
            command=self.delete_multiple_contacts,
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            action_frame,
            text="Quản lý nhóm",
            font=FONTS["button"],
            bg=COLORS["info"],
            fg=COLORS["white"],
            cursor="hand2",
            width=12,
            command=self.show_manage_groups_dialog,
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            action_frame,
            text="Quản lý thẻ",
            font=FONTS["button"],
            bg=COLORS["info"],
            fg=COLORS["white"],
            cursor="hand2",
            width=12,
            command=self.show_manage_tags_dialog,
        ).pack(side=tk.LEFT)

    def create_top_bar(self):
        """Create top navigation bar"""
        top_bar = tk.Frame(self, bg=COLORS["primary"], height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)

        tk.Label(
            top_bar,
            text="📞 PHONEBOOK",
            font=FONTS["title"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(side=tk.LEFT, padx=20)

        user_frame = tk.Frame(top_bar, bg=COLORS["primary"])
        user_frame.pack(side=tk.RIGHT, padx=20)

        tk.Label(
            user_frame,
            text=f"👤 {self.user_data['fullname']}",
            font=FONTS["normal"],
            bg=COLORS["primary"],
            fg=COLORS["white"],
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            user_frame,
            text="Đăng xuất",
            font=FONTS["small"],
            bg=COLORS["danger"],
            fg=COLORS["white"],
            cursor="hand2",
            command=self.on_logout,
        ).pack(side=tk.LEFT)

    def load_contacts(self):
        """Load contacts into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get search term
        search_term = self.search_entry.get().strip()

        # Get selected group filter
        selected_group = (
            self.filter_group_var.get()
            if hasattr(self, "filter_group_var")
            else "-- Tất cả --"
        )

        # Get selected tag filter
        selected_tag = (
            self.filter_tag_var.get()
            if hasattr(self, "filter_tag_var")
            else "-- Tất cả --"
        )

        # Load contacts
        if search_term:
            contacts = self.contact_controller.search_contacts(search_term)
        elif selected_tag != "-- Tất cả --":
            # Filter by tag
            tags = self.tag_controller.get_all_tags()
            tag_id = None
            for t in tags:
                if t.get("tag_name", "") == selected_tag:
                    tag_id = t.get("tag_id")
                    break
            if tag_id:
                contacts = self.contact_controller.filter_by_tag(tag_id)
            else:
                contacts = []
        elif selected_group != "-- Tất cả --":
            # Filter by group
            groups = self.group_controller.get_all_groups()
            group_id = None
            for g in groups:
                if g.get("group_name", "") == selected_group:
                    group_id = g.get("group_id")
                    break
            if group_id:
                contacts = self.contact_controller.filter_by_group(group_id)
            else:
                contacts = []
        else:
            contacts = self.contact_controller.get_all_contacts()

        # Populate treeview
        for contact in contacts:
            full_name = (
                f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
            )
            self.tree.insert(
                "",
                tk.END,
                text=contact.get("contact_id", ""),
                values=(
                    full_name,
                    contact.get("phone", ""),
                    contact.get("email", "") or "",
                    contact.get("group_name", "") or "",
                ),
            )

    def show_add_contact_dialog(self):
        """Show add contact dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Thêm liên hệ mới")
        dialog.geometry("400x500")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")

        form = tk.Frame(dialog, bg=COLORS["white"], padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        fields = {}
        row = 0

        for label, key in [
            ("Tên:", "first_name"),
            ("Họ:", "last_name"),
            ("Số điện thoại:", "phone"),
            ("Email:", "email"),
            ("Địa chỉ:", "address"),
            ("Ghi chú:", "notes"),
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

        groups = self.group_controller.get_all_groups()
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
        group_dropdown.grid(row=row + 1, column=0, pady=(0, 10))

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
                address=fields["address"].get().strip() or None,
                notes=fields["notes"].get().strip() or None,
                group_id=group_id,
            )

            if success:
                show_info("Thành công", "Đã thêm liên hệ mới")
                dialog.destroy()
                self.load_contacts()
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
        ).grid(row=row, column=0, pady=(10, 0))

    def show_edit_contact_dialog(self):
        """Show edit contact dialog"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn liên hệ cần sửa")
            return

        contact_id = int(self.tree.item(selected[0])["text"])
        contact = self.contact_controller.get_contact_by_id(contact_id)

        if not contact:
            show_error("Lỗi", "Không tìm thấy liên hệ")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Sửa liên hệ")
        dialog.geometry("400x500")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()

        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"+{x}+{y}")

        form = tk.Frame(dialog, bg=COLORS["white"], padx=30, pady=20)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        fields = {}
        row = 0

        for label, key, value in [
            ("Tên:", "first_name", contact["first_name"]),
            ("Họ:", "last_name", contact["last_name"]),
            ("Số điện thoại:", "phone", contact["phone"]),
            ("Email:", "email", contact["email"] or ""),
            ("Địa chỉ:", "address", contact["address"] or ""),
            ("Ghi chú:", "notes", contact["notes"] or ""),
        ]:
            tk.Label(form, text=label, font=FONTS["normal"], bg=COLORS["white"]).grid(
                row=row, column=0, sticky=tk.W, pady=(0, 5)
            )
            entry = tk.Entry(form, font=FONTS["normal"], width=30)
            entry.insert(0, value)
            entry.grid(row=row + 1, column=0, pady=(0, 10))
            fields[key] = entry
            row += 2

        def update_contact():
            data = {
                "first_name": fields["first_name"].get().strip(),
                "last_name": fields["last_name"].get().strip(),
                "phone": fields["phone"].get().strip(),
                "email": fields["email"].get().strip() or None,
                "address": fields["address"].get().strip() or None,
                "notes": fields["notes"].get().strip() or None,
            }

            success, result = self.contact_controller.update_contact(contact_id, data)

            if success:
                show_info("Thành công", "Đã cập nhật liên hệ")
                dialog.destroy()
                self.load_contacts()
            else:
                show_error("Lỗi", result)

        tk.Button(
            form,
            text="Cập nhật",
            font=FONTS["button"],
            bg=COLORS["info"],
            fg=COLORS["white"],
            cursor="hand2",
            width=15,
            command=update_contact,
        ).grid(row=row, column=0, pady=(10, 0))

    def delete_contact(self):
        """Delete selected contact"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn liên hệ cần xóa")
            return

        if not ask_yes_no("Xác nhận", "Bạn có chắc muốn xóa liên hệ này?"):
            return

        contact_id = int(self.tree.item(selected[0])["text"])
        success, message = self.contact_controller.delete_contact(contact_id)

        if success:
            show_info("Thành công", message)
            self.load_contacts()
        else:
            show_error("Lỗi", message)

    def delete_multiple_contacts(self):
        """Delete multiple selected contacts at once"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn ít nhất một liên hệ cần xóa")
            return

        count = len(selected)
        if not ask_yes_no("Xác nhận", f"Bạn có chắc muốn xóa {count} liên hệ đã chọn?"):
            return

        success_count = 0
        failed_count = 0

        for item in selected:
            contact_id = int(self.tree.item(item)["text"])
            success, _ = self.contact_controller.delete_contact(contact_id)
            if success:
                success_count += 1
            else:
                failed_count += 1

        # Show result
        if failed_count == 0:
            show_success(f"Đã xóa thành công {success_count} liên hệ!")
        else:
            show_info(
                "Hoàn thành",
                f"Xóa thành công: {success_count}\nThất bại: {failed_count}",
            )

        self.load_contacts()

    def show_manage_tags_dialog(self):
        """Show dialog to manage tags for selected contact"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn liên hệ để quản lý thẻ")
            return

        contact_id = int(self.tree.item(selected[0])["text"])
        contact_name = self.tree.item(selected[0])["values"][0]

        dialog = tk.Toplevel(self)
        dialog.title(f"Quản lý thẻ - {contact_name}")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(
            dialog,
            text=f"Quản lý thẻ cho: {contact_name}",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=20)

        # Get all tags and contact's current tags
        from controllers.tag_controller import TagController

        tag_controller = TagController(self.user_data["user_id"])
        all_tags = tag_controller.get_all_tags()

        from models.contact_model import ContactModel

        contact_tags = ContactModel.get_contact_tags(contact_id)
        contact_tag_ids = [tag["tag_id"] for tag in contact_tags]

        # Create canvas with scrollbar for tag list
        canvas_frame = tk.Frame(dialog, bg=COLORS["bg"])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Auto-save function when checkbox changes
        def on_tag_change(tag_id, var):
            """Auto-save when tag is checked/unchecked"""
            if var.get():
                # Add tag
                ContactModel.add_tag_to_contact(contact_id, tag_id)
            else:
                # Remove tag
                ContactModel.remove_tag_from_contact(contact_id, tag_id)
            self.load_contacts()  # Refresh contact list

        # Checkbuttons for each tag
        if not all_tags:
            tk.Label(
                scrollable_frame,
                text="Chưa có thẻ nào. Vui lòng tạo thẻ trước!",
                font=FONTS["normal"],
                bg=COLORS["bg"],
                fg=COLORS["danger"],
            ).pack(pady=20)
        else:
            for tag in all_tags:
                var = tk.BooleanVar(value=tag["tag_id"] in contact_tag_ids)

                cb = tk.Checkbutton(
                    scrollable_frame,
                    text=f"{tag['tag_name']} - {tag.get('description', '')}",
                    variable=var,
                    font=FONTS["normal"],
                    bg=COLORS["bg"],
                    command=lambda tid=tag["tag_id"], v=var: on_tag_change(tid, v),
                )
                cb.pack(anchor=tk.W, pady=5)

        # Info label at bottom
        info_label = tk.Label(
            dialog,
            text="💡 Thay đổi được lưu tự động. Đóng cửa sổ để hoàn tất.",
            font=FONTS["small"],
            bg=COLORS["bg"],
            fg=COLORS["info"],
        )
        info_label.pack(pady=10)

    def show_manage_groups_dialog(self):
        """Show dialog to manage groups for selected contact"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn liên hệ!")
            return

        contact_id = self.tree.item(selected[0])["text"]

        # Get current contact info
        contacts = self.contact_controller.get_all_contacts()
        contact = next(
            (c for c in contacts if c.get("contact_id") == int(contact_id)), None
        )
        if not contact:
            show_error("Lỗi", "Không tìm thấy liên hệ!")
            return

        contact_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
        current_group_id = contact.get("group_id")

        # Get all groups
        all_groups = self.group_controller.get_all_groups()

        # Create dialog
        dialog = tk.Toplevel(self)
        dialog.title(f"Quản lý nhóm - {contact_name}")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self)
        dialog.grab_set()

        # Title
        tk.Label(
            dialog,
            text=f"Chọn nhóm cho: {contact_name}",
            font=FONTS["heading"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=20)

        # Scrollable frame
        canvas_frame = tk.Frame(dialog, bg=COLORS["bg"])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Auto-save function when radio button changes
        def on_group_change(group_id):
            """Auto-save when group is selected"""
            data = {
                "first_name": contact.get("first_name", ""),
                "last_name": contact.get("last_name", ""),
                "phone": contact.get("phone", ""),
                "email": contact.get("email", ""),
                "address": contact.get("address", ""),
                "notes": contact.get("notes", ""),
                "group_id": group_id if group_id else None,
            }
            success, message = self.contact_controller.update_contact(
                int(contact_id), data
            )
            if success:
                self.load_contacts()  # Refresh contact list

        # Variable for selected group
        selected_group_var = tk.IntVar(
            value=current_group_id if current_group_id else 0
        )

        # Radio button for "No group"
        rb_none = tk.Radiobutton(
            scrollable_frame,
            text="-- Không chọn nhóm --",
            variable=selected_group_var,
            value=0,
            font=FONTS["normal"],
            bg=COLORS["bg"],
            command=lambda: on_group_change(None),
        )
        rb_none.pack(anchor=tk.W, pady=5)

        # Radio buttons for each group
        if not all_groups:
            tk.Label(
                scrollable_frame,
                text="Chưa có nhóm nào. Vui lòng tạo nhóm trước!",
                font=FONTS["normal"],
                bg=COLORS["bg"],
                fg=COLORS["danger"],
            ).pack(pady=20)
        else:
            for group in all_groups:
                rb = tk.Radiobutton(
                    scrollable_frame,
                    text=f"{group.get('group_name', '')} - {group.get('description', '')}",
                    variable=selected_group_var,
                    value=group.get("group_id", 0),
                    font=FONTS["normal"],
                    bg=COLORS["bg"],
                    command=lambda gid=group.get("group_id"): on_group_change(gid),
                )
                rb.pack(anchor=tk.W, pady=5)

        # Info label at bottom
        info_label = tk.Label(
            dialog,
            text="💡 Thay đổi được lưu tự động. Đóng cửa sổ để hoàn tất.",
            font=FONTS["small"],
            bg=COLORS["bg"],
            fg=COLORS["info"],
        )
        info_label.pack(pady=10)

    def export_to_csv(self):
        """Export displayed contacts to CSV"""
        # Get current filtered/searched contacts from treeview
        contacts_to_export = []

        for item in self.tree.get_children():
            # contact_id is stored in 'text' field of treeview item
            contact_id = self.tree.item(item)["text"]

            # Find full contact data
            all_contacts = self.contact_controller.get_all_contacts()
            for contact in all_contacts:
                if str(contact.get("contact_id")) == str(contact_id):
                    contacts_to_export.append(contact)
                    break

        if not contacts_to_export:
            show_info("Thông báo", "Không có liên hệ nào để xuất")
            return

        success, result = self.contact_controller.export_contacts_to_csv(
            contacts_to_export
        )

        if success:
            show_success(
                f"Đã xuất {len(contacts_to_export)} liên hệ ra file CSV!\n\nĐường dẫn: {result}"
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
                self.load_contacts()
            else:
                show_error("Lỗi", result)
