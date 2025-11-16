═══════════════════════════════════════════════════════════════
         PHONEBOOK APPLICATION v1.0 - PACKAGE DISTRIBUTION
═══════════════════════════════════════════════════════════════

📦 NỘI DUNG PACKAGE
-------------------
📁 dist/
  ├── PhoneBook.exe              ← Ứng dụng chính (16 MB)
  ├── HUONG_DAN_SU_DUNG.txt      ← Hướng dẫn chi tiết cho người dùng
  ├── database_setup.sql         ← Script tạo database MySQL
  └── README.txt                 ← File này

═══════════════════════════════════════════════════════════════

🚀 HƯỚNG DẪN NHANH (5 PHÚT)
---------------------------

BƯỚC 1: Cài MySQL Server
-------------------------
▸ Tải từ: https://dev.mysql.com/downloads/mysql/
▸ Cài đặt với cấu hình mặc định
▸ Ghi nhớ root password!

BƯỚC 2: Tạo Database
---------------------
▸ Mở MySQL Command Line Client (hoặc Workbench)
▸ Đăng nhập với root password
▸ Copy-paste nội dung file: database_setup.sql
▸ Nhấn Enter để chạy

BƯỚC 3: Chạy PhoneBook
-----------------------
▸ Double-click: PhoneBook.exe
▸ Đăng nhập:
  Username: admin
  Password: 123456

═══════════════════════════════════════════════════════════════

✅ KIỂM TRA KẾT NỐI
--------------------
Sau khi chạy PhoneBook.exe:

▸ Nếu thấy màn hình đăng nhập → ✅ THÀNH CÔNG!
▸ Nếu báo lỗi "Cannot connect to database":
  → Kiểm tra MySQL Server đang chạy (Services → MySQL80)
  → Kiểm tra đã chạy file database_setup.sql chưa

═══════════════════════════════════════════════════════════════

📖 TÀI LIỆU CHI TIẾT
---------------------
Đọc file: HUONG_DAN_SU_DUNG.txt

Bao gồm:
✓ Yêu cầu hệ thống
✓ Hướng dẫn cài đặt chi tiết
✓ Cách sử dụng từng tính năng
✓ Xử lý sự cố
✓ Backup & Restore

═══════════════════════════════════════════════════════════════

⚙️ CẤU HÌNH TÙY CHỈNH (CHO NGƯỜI DÙNG NÂNG CAO)
-----------------------------------------------

Nếu MySQL của bạn KHÁC cấu hình mặc định:

1. Tạo file config.txt cùng thư mục với PhoneBook.exe
2. Nội dung:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password_here
   DB_NAME=phonebook_db
   DB_PORT=3306

3. Khởi động lại PhoneBook.exe

⚠️ LƯU Ý: Chỉ cần làm điều này nếu bạn dùng:
- MySQL trên server khác (không phải localhost)
- User/password khác root
- Port khác 3306

═══════════════════════════════════════════════════════════════

🔒 BẢO MẬT
-----------
▸ Đổi password admin ngay sau lần đăng nhập đầu!
▸ Không chia sẻ file PhoneBook.exe cho người không tin cậy
▸ Backup dữ liệu định kỳ bằng tính năng Export CSV

═══════════════════════════════════════════════════════════════

📞 HỖ TRỢ
---------
Email: support@phonebook.com
Website: https://phonebook.com

═══════════════════════════════════════════════════════════════

© 2025 PhoneBook Team - Group 10
Phát triển bởi sinh viên Khoa CNTT

═══════════════════════════════════════════════════════════════
