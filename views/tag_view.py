"""
Tag View - Tag Management
"""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS
from controllers.tag_controller import TagController
from views.components.messagebox_custom import show_error, show_success, ask_yes_no


class TagView(tk.Frame):
    def __init__(self, parent, user_data, on_logout, on_switch_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.user_data = user_data
        self.on_logout = on_logout
        self.on_switch_view = on_switch_view
        self.controller = TagController(user_data["user_id"])

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.load_tags()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg=COLORS["bg"])
        header_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(
            header_frame,
            text="QUẢN LÝ THẺ",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT)

        tk.Button(
            header_frame,
            text="+ Thêm thẻ",
            command=self.show_add_tag_dialog,
            bg=COLORS["success"],
            fg=COLORS["white"],
            font=FONTS["button"],
        ).pack(side=tk.RIGHT, padx=5)

        tk.Button(
            header_frame,
            text="Về trang chủ",
            command=lambda: self.on_switch_view("dashboard"),
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            font=FONTS["button"],
        ).pack(side=tk.RIGHT)

        # Tags list with scrollbar
        list_frame = tk.Frame(self, bg=COLORS["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Treeview (với selectmode extended để chọn nhiều)
        columns = ("Tên thẻ", "Mô tả", "Số liên hệ")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=15,
            selectmode="extended",
        )

        self.tree.heading("Tên thẻ", text="Tên thẻ")
        self.tree.heading("Mô tả", text="Mô tả")
        self.tree.heading("Số liên hệ", text="Số liên hệ")

        self.tree.column("Tên thẻ", width=200)
        self.tree.column("Mô tả", width=400)
        self.tree.column("Số liên hệ", width=100)

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
            text="Sửa",
            command=self.show_edit_tag_dialog,
            bg=COLORS["warning"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Xóa",
            command=self.delete_tag,
            bg=COLORS["danger"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="❌ Xóa nhiều đã chọn",
            command=self.delete_multiple_tags,
            bg="#c0392b",  # Màu đỏ đậm hơn
            fg=COLORS["white"],
            font=FONTS["button"],
            width=18,
        ).pack(side=tk.LEFT, padx=5)

    def load_tags(self):
        """Load tags from database"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        tags = self.controller.get_all_tags()
        for tag in tags:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    tag["tag_name"],
                    tag.get("description", ""),
                    tag.get("usage_count", 0),
                ),
                tags=(tag["tag_id"],),
            )

    def show_add_tag_dialog(self):
        """Show add tag dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("Thêm thẻ mới")
        dialog.geometry("400x250")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Form
        tk.Label(
            dialog,
            text="THÊM THẺ MỚI",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=20)

        form_frame = tk.Frame(dialog, bg=COLORS["bg"])
        form_frame.pack(padx=30)

        tk.Label(
            form_frame, text="Tên thẻ:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=0, column=0, sticky=tk.W, pady=10)
        name_entry = tk.Entry(form_frame, font=FONTS["normal"], width=25)
        name_entry.grid(row=0, column=1, pady=10, padx=(10, 0))

        tk.Label(form_frame, text="Mô tả:", font=FONTS["normal"], bg=COLORS["bg"]).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        desc_entry = tk.Entry(form_frame, font=FONTS["normal"], width=25)
        desc_entry.grid(row=1, column=1, pady=10, padx=(10, 0))

        def add_tag():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()

            if not name:
                show_error("Lỗi", "Vui lòng nhập tên thẻ")
                return

            success, message = self.controller.add_tag(
                name, description if description else None
            )

            if success:
                show_success(message)
                self.load_tags()
                dialog.destroy()
            else:
                show_error("Lỗi", message)

        button_frame = tk.Frame(dialog, bg=COLORS["bg"])
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Thêm",
            command=add_tag,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Hủy",
            command=dialog.destroy,
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

    def show_edit_tag_dialog(self):
        """Show edit tag dialog"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn thẻ cần sửa")
            return

        item = self.tree.item(selected[0])
        tag_id = item["tags"][0]
        current_values = item["values"]

        dialog = tk.Toplevel(self)
        dialog.title("Sửa thẻ")
        dialog.geometry("400x250")
        dialog.configure(bg=COLORS["bg"])
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")

        # Form
        tk.Label(
            dialog,
            text="SỬA THẺ",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["primary"],
        ).pack(pady=20)

        form_frame = tk.Frame(dialog, bg=COLORS["bg"])
        form_frame.pack(padx=30)

        tk.Label(
            form_frame, text="Tên thẻ:", font=FONTS["normal"], bg=COLORS["bg"]
        ).grid(row=0, column=0, sticky=tk.W, pady=10)
        name_entry = tk.Entry(form_frame, font=FONTS["normal"], width=25)
        name_entry.grid(row=0, column=1, pady=10, padx=(10, 0))
        name_entry.insert(0, current_values[0])

        tk.Label(form_frame, text="Mô tả:", font=FONTS["normal"], bg=COLORS["bg"]).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        desc_entry = tk.Entry(form_frame, font=FONTS["normal"], width=25)
        desc_entry.grid(row=1, column=1, pady=10, padx=(10, 0))
        desc_entry.insert(0, current_values[1])

        def update_tag():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()

            if not name:
                show_error("Lỗi", "Vui lòng nhập tên thẻ")
                return

            success, message = self.controller.update_tag(
                tag_id, name, description if description else None
            )

            if success:
                show_success(message)
                self.load_tags()
                dialog.destroy()
            else:
                show_error("Lỗi", message)

        button_frame = tk.Frame(dialog, bg=COLORS["bg"])
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Cập nhật",
            command=update_tag,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Hủy",
            command=dialog.destroy,
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            font=FONTS["button"],
            width=10,
        ).pack(side=tk.LEFT, padx=5)

    def delete_tag(self):
        """Delete selected tag"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn thẻ cần xóa")
            return

        item = self.tree.item(selected[0])
        tag_id = item["tags"][0]
        tag_name = item["values"][0]

        if ask_yes_no("Xác nhận", f"Bạn có chắc muốn xóa thẻ '{tag_name}'?"):
            success, message = self.controller.delete_tag(tag_id)

            if success:
                show_success(message)
                self.load_tags()
            else:
                show_error("Lỗi", message)

    def delete_multiple_tags(self):
        """Delete multiple selected tags at once"""
        selected = self.tree.selection()
        if not selected:
            show_error("Lỗi", "Vui lòng chọn ít nhất một thẻ cần xóa")
            return

        count = len(selected)
        if not ask_yes_no("Xác nhận", f"Bạn có chắc muốn xóa {count} thẻ đã chọn?"):
            return

        success_count = 0
        failed_count = 0

        for item in selected:
            tag_id = self.tree.item(item)["tags"][0]
            success, _ = self.controller.delete_tag(tag_id)
            if success:
                success_count += 1
            else:
                failed_count += 1

        # Show result
        if failed_count == 0:
            show_success(f"Đã xóa thành công {success_count} thẻ!")
        else:
            from views.components import show_info

            show_info(
                "Hoàn thành",
                f"Xóa thành công: {success_count}\nThất bại: {failed_count}",
            )

        self.load_tags()
