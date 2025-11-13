"""
Script để đổ dữ liệu giả vào database
"""

from db import db
from utils.security import hash_password
import random


def create_user_account():
    """Tạo tài khoản user mặc định"""
    print("\n" + "=" * 50)
    print("TẠO TÀI KHOẢN USER")
    print("=" * 50)

    # Tài khoản mặc định
    username = "admin"
    password = "123456"
    email = "admin@phonebook.com"
    fullname = "Quản Trị Viên"
    phone = "0123456789"
    address = "Hà Nội, Việt Nam"

    # Kiểm tra user đã tồn tại chưa
    check_query = "SELECT user_id FROM users WHERE username = %s"
    existing = db.execute_query(check_query, (username,), fetch=True)

    if existing:
        print(f"✓ Tài khoản '{username}' đã tồn tại!")
        return existing[0]["user_id"]

    # Hash password
    password_hash = hash_password(password)

    # Insert user
    query = """
        INSERT INTO users (username, email, password_hash, fullname, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    result = db.execute_query(
        query, (username, email, password_hash, fullname, phone, address)
    )

    if result and result["last_id"]:
        print(f"✓ Đã tạo tài khoản thành công!")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Email: {email}")
        return result["last_id"]
    else:
        print("✗ Lỗi khi tạo tài khoản!")
        return None


def seed_groups(user_id):
    """Tạo dữ liệu giả cho bảng my_groups"""
    print("\n" + "=" * 50)
    print("TẠO DỮ LIỆU NHÓM")
    print("=" * 50)

    groups = [
        ("Gia đình", "Thành viên trong gia đình"),
        ("Bạn bè", "Bạn bè thân thiết"),
        ("Đồng nghiệp", "Đồng nghiệp làm việc cùng"),
        ("Khách hàng", "Danh sách khách hàng"),
        ("Đối tác", "Đối tác kinh doanh"),
        ("Học sinh", "Danh sách học sinh"),
        ("Khẩn cấp", "Số điện thoại khẩn cấp"),
    ]

    query = """
        INSERT INTO my_groups (user_id, group_name, description)
        VALUES (%s, %s, %s)
    """

    group_ids = []
    for group_name, description in groups:
        # Kiểm tra group đã tồn tại chưa
        check_query = (
            "SELECT group_id FROM my_groups WHERE user_id = %s AND group_name = %s"
        )
        existing = db.execute_query(check_query, (user_id, group_name), fetch=True)

        if existing:
            print(f"✓ Nhóm '{group_name}' đã tồn tại")
            group_ids.append(existing[0]["group_id"])
        else:
            result = db.execute_query(query, (user_id, group_name, description))
            if result and result["last_id"]:
                print(f"✓ Đã tạo nhóm: {group_name}")
                group_ids.append(result["last_id"])

    return group_ids


def seed_tags(user_id):
    """Tạo dữ liệu giả cho bảng tags"""
    print("\n" + "=" * 50)
    print("TẠO DỮ LIỆU TAG")
    print("=" * 50)

    tags = [
        ("VIP", "Khách hàng VIP"),
        ("Quan trọng", "Liên hệ quan trọng"),
        ("Yêu thích", "Liên hệ yêu thích"),
        ("Công việc", "Liên quan công việc"),
        ("Cá nhân", "Liên hệ cá nhân"),
        ("Sinh nhật", "Cần chúc mừng sinh nhật"),
        ("Nợ tiền", "Danh sách nợ tiền"),
        ("Cho vay", "Đã cho vay tiền"),
    ]

    query = """
        INSERT INTO tags (user_id, tag_name, description)
        VALUES (%s, %s, %s)
    """

    tag_ids = []
    for tag_name, description in tags:
        # Kiểm tra tag đã tồn tại chưa
        check_query = "SELECT tag_id FROM tags WHERE user_id = %s AND tag_name = %s"
        existing = db.execute_query(check_query, (user_id, tag_name), fetch=True)

        if existing:
            print(f"✓ Tag '{tag_name}' đã tồn tại")
            tag_ids.append(existing[0]["tag_id"])
        else:
            result = db.execute_query(query, (user_id, tag_name, description))
            if result and result["last_id"]:
                print(f"✓ Đã tạo tag: {tag_name}")
                tag_ids.append(result["last_id"])

    return tag_ids


def seed_contacts(user_id, group_ids):
    """Tạo dữ liệu giả cho bảng contacts"""
    print("\n" + "=" * 50)
    print("TẠO DỮ LIỆU LIÊN HỆ")
    print("=" * 50)

    contacts = [
        # Gia đình
        (
            "Nguyễn Văn",
            "An",
            "0901234567",
            "an.nguyen@gmail.com",
            "123 Đường ABC, Hà Nội",
            "Bố",
            0,
        ),
        (
            "Trần Thị",
            "Bình",
            "0902345678",
            "binh.tran@gmail.com",
            "123 Đường ABC, Hà Nội",
            "Mẹ",
            0,
        ),
        (
            "Nguyễn Văn",
            "Cường",
            "0903456789",
            "cuong.nguyen@gmail.com",
            "456 Đường DEF, Hà Nội",
            "Anh trai",
            0,
        ),
        # Bạn bè
        (
            "Lê Thị",
            "Dung",
            "0904567890",
            "dung.le@gmail.com",
            "789 Đường GHI, Hà Nội",
            "Bạn thân từ cấp 3",
            1,
        ),
        (
            "Phạm Văn",
            "Em",
            "0905678901",
            "em.pham@gmail.com",
            "321 Đường JKL, Hà Nội",
            "Bạn đại học",
            1,
        ),
        (
            "Hoàng Thị",
            "Phượng",
            "0906789012",
            "phuong.hoang@gmail.com",
            "654 Đường MNO, Hà Nội",
            "Bạn cùng lớp",
            1,
        ),
        # Đồng nghiệp
        (
            "Vũ Văn",
            "Giang",
            "0907890123",
            "giang.vu@company.com",
            "Tòa nhà ABC, Hà Nội",
            "Trưởng phòng",
            2,
        ),
        (
            "Đỗ Thị",
            "Hương",
            "0908901234",
            "huong.do@company.com",
            "Tòa nhà ABC, Hà Nội",
            "Đồng nghiệp phòng kế toán",
            2,
        ),
        (
            "Bùi Văn",
            "Inh",
            "0909012345",
            "inh.bui@company.com",
            "Tòa nhà ABC, Hà Nội",
            "Nhân viên IT",
            2,
        ),
        # Khách hàng
        (
            "Ngô Thị",
            "Kim",
            "0910123456",
            "kim.ngo@business.com",
            "Công ty XYZ, Hà Nội",
            "Khách hàng từ 2020",
            3,
        ),
        (
            "Đinh Văn",
            "Long",
            "0911234567",
            "long.dinh@enterprise.com",
            "Công ty ABC, Hồ Chí Minh",
            "Khách hàng VIP",
            3,
        ),
        (
            "Trịnh Thị",
            "Mai",
            "0912345678",
            "mai.trinh@shop.com",
            "Cửa hàng Mai, Đà Nẵng",
            "Khách hàng thường xuyên",
            3,
        ),
        # Đối tác
        (
            "Lý Văn",
            "Nam",
            "0913456789",
            "nam.ly@partner.com",
            "Văn phòng Nam, Hải Phòng",
            "Đối tác logistics",
            4,
        ),
        (
            "Võ Thị",
            "Oanh",
            "0914567890",
            "oanh.vo@supplier.com",
            "Nhà máy Oanh, Bình Dương",
            "Nhà cung cấp",
            4,
        ),
        # Học sinh
        (
            "Mai Văn",
            "Phúc",
            "0915678901",
            "phuc.mai@student.edu",
            "123 Đường Học Sinh, Hà Nội",
            "Học sinh lớp 10A",
            5,
        ),
        (
            "Cao Thị",
            "Quỳnh",
            "0916789012",
            "quynh.cao@student.edu",
            "456 Đường Học Sinh, Hà Nội",
            "Học sinh lớp 11B",
            5,
        ),
        # Khẩn cấp
        (
            "Bệnh viện",
            "Bạch Mai",
            "0243869731",
            "info@bachmai.gov.vn",
            "78 Giải Phóng, Hà Nội",
            "Bệnh viện đa khoa",
            6,
        ),
        (
            "Công an",
            "Phường 1",
            "0911234567",
            "",
            "Trụ sở công an phường",
            "Số khẩn cấp",
            6,
        ),
        ("Cứu hỏa", "114", "114", "", "", "Số điện thoại cứu hỏa", 6),
    ]

    query = """
        INSERT INTO contacts (user_id, first_name, last_name, phone, email, address, notes, group_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    contact_ids = []
    for first_name, last_name, phone, email, address, notes, group_idx in contacts:
        # Kiểm tra contact đã tồn tại chưa
        check_query = (
            "SELECT contact_id FROM contacts WHERE user_id = %s AND phone = %s"
        )
        existing = db.execute_query(check_query, (user_id, phone), fetch=True)

        if existing:
            print(f"✓ Liên hệ '{first_name} {last_name}' đã tồn tại")
            contact_ids.append(existing[0]["contact_id"])
        else:
            group_id = group_ids[group_idx] if group_idx < len(group_ids) else None
            result = db.execute_query(
                query,
                (
                    user_id,
                    first_name,
                    last_name,
                    phone,
                    email,
                    address,
                    notes,
                    group_id,
                ),
            )
            if result and result["last_id"]:
                print(f"✓ Đã tạo liên hệ: {first_name} {last_name}")
                contact_ids.append(result["last_id"])

    return contact_ids


def seed_contact_tags(contact_ids, tag_ids):
    """Gán tags ngẫu nhiên cho contacts"""
    print("\n" + "=" * 50)
    print("GÁN TAG CHO LIÊN HỆ")
    print("=" * 50)

    # Kiểm tra tags đã tồn tại trước khi insert
    check_query = """
        SELECT COUNT(*) as count FROM contact_tags 
        WHERE contact_id = %s AND tag_id = %s
    """

    insert_query = """
        INSERT INTO contact_tags (contact_id, tag_id)
        VALUES (%s, %s)
    """

    count = 0
    skipped = 0

    for contact_id in contact_ids:
        # Mỗi contact có 1-3 tags ngẫu nhiên
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(tag_ids, min(num_tags, len(tag_ids)))

        for tag_id in selected_tags:
            # Kiểm tra xem tag đã được gán chưa
            existing = db.execute_query(check_query, (contact_id, tag_id), fetch=True)

            if existing and existing[0]["count"] == 0:
                # Chưa tồn tại, insert mới
                result = db.execute_query(insert_query, (contact_id, tag_id))
                if result and result["affected_rows"] > 0:
                    count += 1
            else:
                skipped += 1

    print(f"✓ Đã gán {count} tags mới cho các liên hệ")
    if skipped > 0:
        print(f"  (Bỏ qua {skipped} tags đã tồn tại)")


def seed_deleted_contacts(user_id, group_ids):
    """Tạo một số liên hệ đã xóa (trong thùng rác)"""
    print("\n" + "=" * 50)
    print("TẠO DỮ LIỆU THÙNG RÁC")
    print("=" * 50)

    deleted_contacts = [
        ("Người", "Lạ", "0920000001", "stranger@unknown.com", "", "Số spam", None),
        (
            "Công ty",
            "Cũ",
            "0920000002",
            "old@company.com",
            "Công ty cũ",
            "Không làm nữa",
            None,
        ),
        ("Bạn", "Cũ", "0920000003", "oldfrend@email.com", "", "Không liên lạc nữa", 1),
    ]

    query = """
        INSERT INTO contacts (user_id, first_name, last_name, phone, email, address, notes, group_id, is_deleted, deleted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW())
    """

    for (
        first_name,
        last_name,
        phone,
        email,
        address,
        notes,
        group_id,
    ) in deleted_contacts:
        # Kiểm tra đã tồn tại chưa
        check_query = (
            "SELECT contact_id FROM contacts WHERE user_id = %s AND phone = %s"
        )
        existing = db.execute_query(check_query, (user_id, phone), fetch=True)

        if existing:
            print(f"✓ Liên hệ đã xóa '{first_name} {last_name}' đã tồn tại")
        else:
            result = db.execute_query(
                query,
                (
                    user_id,
                    first_name,
                    last_name,
                    phone,
                    email,
                    address,
                    notes,
                    group_id,
                ),
            )
            if result and result["last_id"]:
                print(f"✓ Đã tạo liên hệ đã xóa: {first_name} {last_name}")


def main():
    """Chạy toàn bộ quá trình seed data"""
    print("\n" + "=" * 50)
    print("BẮT ĐẦU ĐỔ DỮ LIỆU GIẢ VÀO DATABASE")
    print("=" * 50)

    # 1. Tạo tài khoản user
    user_id = create_user_account()
    if not user_id:
        print("\n✗ Không thể tạo user, dừng lại!")
        return

    # 2. Tạo groups
    group_ids = seed_groups(user_id)
    if not group_ids:
        print("\n✗ Không thể tạo groups, dừng lại!")
        return

    # 3. Tạo tags
    tag_ids = seed_tags(user_id)
    if not tag_ids:
        print("\n✗ Không thể tạo tags, dừng lại!")
        return

    # 4. Tạo contacts
    contact_ids = seed_contacts(user_id, group_ids)
    if not contact_ids:
        print("\n✗ Không thể tạo contacts, dừng lại!")
        return

    # 5. Gán tags cho contacts
    seed_contact_tags(contact_ids, tag_ids)

    # 6. Tạo contacts đã xóa
    seed_deleted_contacts(user_id, group_ids)

    print("\n" + "=" * 50)
    print("HOÀN THÀNH ĐỔ DỮ LIỆU!")
    print("=" * 50)
    print("\nTHỐNG KÊ:")
    print(f"  ✓ Tài khoản: 1")
    print(f"  ✓ Nhóm: {len(group_ids)}")
    print(f"  ✓ Tag: {len(tag_ids)}")
    print(f"  ✓ Liên hệ: {len(contact_ids)}")
    print(f"  ✓ Thùng rác: 3")

    print("\nTHÔNG TIN ĐĂNG NHẬP:")
    print("  Username: admin")
    print("  Password: 123456")
    print("\nBạn có thể đăng nhập vào ứng dụng với thông tin trên!")


if __name__ == "__main__":
    main()
