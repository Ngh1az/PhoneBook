"""
Script thêm dữ liệu mẫu vào database SQLite
Chạy sau khi đã có tài khoản admin
"""

import sqlite3
import os
import sys

# Xác định đường dẫn database
# Sử dụng database trong dist/data (nơi app .exe sử dụng)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dist", "data", "phonebook.db")

print(f"\n{'='*60}")
print("THÊM DỮ LIỆU MẪU VÀO PHONEBOOK")
print(f"{'='*60}")
print(f"Database: {DB_PATH}\n")

# Kết nối database
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Lấy user_id của admin
cursor.execute("SELECT user_id FROM users WHERE username = ?", ("admin",))
user = cursor.fetchone()

if not user:
    print("✗ Không tìm thấy user 'admin'. Vui lòng chạy app trước để tạo user!")
    conn.close()
    sys.exit(1)

user_id = user[0]
print(f"✓ Tìm thấy user: admin (ID: {user_id})")

# 1. TẠO NHÓM
print(f"\n{'-'*60}")
print("ĐANG TẠO NHÓM...")
print(f"{'-'*60}")

groups = [
    ("Gia đình", "Các thành viên trong gia đình"),
    ("Bạn bè", "Danh sách bạn bè thân thiết"),
    ("Công việc", "Đồng nghiệp và đối tác"),
    ("Khách hàng", "Danh sách khách hàng"),
    ("Nhà cung cấp", "Các nhà cung cấp dịch vụ"),
]

group_ids = []
for group_name, description in groups:
    # Kiểm tra đã tồn tại chưa
    cursor.execute(
        "SELECT group_id FROM my_groups WHERE user_id = ? AND group_name = ?",
        (user_id, group_name),
    )
    existing = cursor.fetchone()

    if existing:
        group_ids.append(existing[0])
        print(f"  ⊙ Nhóm '{group_name}' đã tồn tại")
    else:
        cursor.execute(
            "INSERT INTO my_groups (user_id, group_name, description) VALUES (?, ?, ?)",
            (user_id, group_name, description),
        )
        group_ids.append(cursor.lastrowid)
        print(f"  ✓ Tạo nhóm '{group_name}'")

conn.commit()
print(f"\n✓ Tổng số nhóm: {len(group_ids)}")

# 2. TẠO THẺ TAG
print(f"\n{'-'*60}")
print("ĐANG TẠO THẺ TAG...")
print(f"{'-'*60}")

tags = [
    ("VIP", "Khách hàng quan trọng nhất"),
    ("Quan trọng", "Liên hệ cần ưu tiên"),
    ("Ưu tiên", "Cần liên lạc thường xuyên"),
    ("Thường xuyên", "Liên hệ đều đặn"),
    ("Mới", "Liên hệ mới thêm"),
    ("Yêu thích", "Những người yêu quý"),
]

tag_ids = []
for tag_name, description in tags:
    cursor.execute(
        "SELECT tag_id FROM tags WHERE user_id = ? AND tag_name = ?",
        (user_id, tag_name),
    )
    existing = cursor.fetchone()

    if existing:
        tag_ids.append(existing[0])
        print(f"  ⊙ Tag '{tag_name}' đã tồn tại")
    else:
        cursor.execute(
            "INSERT INTO tags (user_id, tag_name, description) VALUES (?, ?, ?)",
            (user_id, tag_name, description),
        )
        tag_ids.append(cursor.lastrowid)
        print(f"  ✓ Tạo tag '{tag_name}'")

conn.commit()
print(f"\n✓ Tổng số tag: {len(tag_ids)}")

# 3. TẠO LIÊN HỆ
print(f"\n{'-'*60}")
print("ĐANG TẠO LIÊN HỆ...")
print(f"{'-'*60}")

contacts = [
    # Gia đình (group_ids[0])
    (
        "Nguyễn",
        "Văn An",
        "0901234567",
        "nguyenvanan@gmail.com",
        "123 Đường ABC, Hà Nội",
        "Bố, sinh 01/01/1975",
        group_ids[0],
    ),
    (
        "Trần",
        "Thị Bình",
        "0902345678",
        "tranthibinh@gmail.com",
        "123 Đường ABC, Hà Nội",
        "Mẹ, sinh 15/05/1978",
        group_ids[0],
    ),
    (
        "Nguyễn",
        "Văn Cường",
        "0903456789",
        "nguyencuong@gmail.com",
        "456 Đường XYZ, Hồ Chí Minh",
        "Anh trai, sinh 20/08/2000",
        group_ids[0],
    ),
    # Bạn bè (group_ids[1])
    (
        "Lê",
        "Thị Dung",
        "0904567890",
        "ledung@yahoo.com",
        "789 Đường DEF, Đà Nẵng",
        "Bạn thân từ cấp 3, Instagram: @ledung",
        group_ids[1],
    ),
    (
        "Phạm",
        "Minh Đức",
        "0905678901",
        "phamminhduc@outlook.com",
        "321 Đường GHI, Hải Phòng",
        "Bạn đại học, sinh 25/07/1996",
        group_ids[1],
    ),
    (
        "Hoàng",
        "Thu Hà",
        "0906789012",
        "hoangha@gmail.com",
        "654 Đường JKL, Cần Thơ",
        "Bạn cùng phòng, Telegram: @hoangha",
        group_ids[1],
    ),
    # Công việc (group_ids[2])
    (
        "Vũ",
        "Đình Hùng",
        "0907890123",
        "vuhung@company.com",
        "111 Lê Lợi, Hà Nội",
        "Trưởng phòng, Slack: @vuhung",
        group_ids[2],
    ),
    (
        "Đặng",
        "Thị Lan",
        "0908901234",
        "danglan@company.com",
        "222 Trần Hưng Đạo, Hà Nội",
        "Đồng nghiệp",
        group_ids[2],
    ),
    (
        "Bùi",
        "Văn Minh",
        "0909012345",
        "buiminh@company.com",
        "333 Nguyễn Trãi, Hà Nội",
        "Giám đốc, Teams: buiminh",
        group_ids[2],
    ),
    # Khách hàng (group_ids[3])
    (
        "Công ty",
        "TNHH ABC",
        "0241234567",
        "contact@abc.com.vn",
        "555 Hoàng Quốc Việt, Hà Nội",
        "Khách hàng VIP, Website: abc.com.vn",
        group_ids[3],
    ),
    (
        "Nguyễn",
        "Văn Nam",
        "0910123456",
        "nvnam@xyz.com",
        "666 Cầu Giấy, Hà Nội",
        "Giám đốc công ty XYZ",
        group_ids[3],
    ),
    # Nhà cung cấp (group_ids[4])
    (
        "Công ty",
        "CP DEF",
        "0281234567",
        "sale@def.vn",
        "777 Láng Hạ, Hà Nội",
        "Nhà cung cấp thiết bị, Hotline: 1900xxxx",
        group_ids[4],
    ),
    (
        "Trần",
        "Văn Phong",
        "0911234567",
        "tranphong@supplier.com",
        "888 Đê La Thành, Hà Nội",
        "Đại diện nhà cung cấp",
        group_ids[4],
    ),
]

contact_ids = []
for first_name, last_name, phone, email, address, notes, group_id in contacts:
    # Kiểm tra đã tồn tại chưa
    cursor.execute(
        "SELECT contact_id FROM contacts WHERE user_id = ? AND phone = ?",
        (user_id, phone),
    )
    existing = cursor.fetchone()

    if existing:
        contact_ids.append(existing[0])
        print(f"  ⊙ Liên hệ '{first_name} {last_name}' đã tồn tại")
    else:
        cursor.execute(
            """INSERT INTO contacts 
            (user_id, group_id, first_name, last_name, phone, email, address, notes, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)""",
            (user_id, group_id, first_name, last_name, phone, email, address, notes),
        )
        contact_ids.append(cursor.lastrowid)
        print(f"  ✓ Tạo liên hệ '{first_name} {last_name}'")

conn.commit()
print(f"\n✓ Tổng số liên hệ: {len(contact_ids)}")

# 4. GÁN TAG CHO LIÊN HỆ
print(f"\n{'-'*60}")
print("ĐANG GÁN TAG CHO LIÊN HỆ...")
print(f"{'-'*60}")

# Gán tag ngẫu nhiên cho các contact
import random

random.seed(42)  # Để kết quả nhất quán

tag_assignments = 0
for contact_id in contact_ids[:8]:  # Chỉ gán tag cho 8 contact đầu
    num_tags = random.randint(1, 3)  # Mỗi contact có 1-3 tag
    selected_tags = random.sample(tag_ids, num_tags)

    for tag_id in selected_tags:
        # Kiểm tra đã tồn tại chưa
        cursor.execute(
            "SELECT * FROM contact_tags WHERE contact_id = ? AND tag_id = ?",
            (contact_id, tag_id),
        )
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO contact_tags (contact_id, tag_id) VALUES (?, ?)",
                (contact_id, tag_id),
            )
            tag_assignments += 1

            # Lấy tên tag
            cursor.execute("SELECT tag_name FROM tags WHERE tag_id = ?", (tag_id,))
            tag_name = cursor.fetchone()[0]

            # Lấy tên contact
            cursor.execute(
                "SELECT first_name, last_name FROM contacts WHERE contact_id = ?",
                (contact_id,),
            )
            contact = cursor.fetchone()
            print(f"  ✓ Gán tag '{tag_name}' cho '{contact[0]} {contact[1]}'")

conn.commit()
print(f"\n✓ Tổng số tag đã gán: {tag_assignments}")

# Đóng kết nối
conn.close()

# Thống kê cuối cùng
print(f"\n{'='*60}")
print("HOÀN TẤT THÊM DỮ LIỆU MẪU!")
print(f"{'='*60}")
print(
    f"""
THỐNG KÊ:
  • Nhóm: {len(group_ids)}
  • Tag: {len(tag_ids)}
  • Liên hệ: {len(contact_ids)}
  • Tag đã gán: {tag_assignments}

Bạn có thể đăng nhập vào app với:
  Username: admin
  Password: 123456
  
Giờ đây app đã có đầy đủ dữ liệu mẫu để test!
"""
)
