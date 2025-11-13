# PhoneBook Application

Ứng dụng quản lý danh bạ điện thoại được xây dựng bằng Python và MySQL với giao diện đồ họa Tkinter.

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Bảo mật](#bảo-mật)
- [Tài liệu](#tài-liệu)

## Giới thiệu

PhoneBook Application là một ứng dụng desktop giúp quản lý danh bạ điện thoại với đầy đủ các tính năng CRUD (Create, Read, Update, Delete), phân loại theo nhóm và tag, thống kê, sao lưu dữ liệu và nhiều tính năng khác.

## Tính năng

### Quản lý người dùng

- Đăng ký tài khoản mới với xác thực đầy đủ
- Đăng nhập/Đăng xuất an toàn
- Quản lý thông tin cá nhân
- Đổi mật khẩu với xác thực

### Quản lý danh bạ

- Thêm, sửa, xóa liên hệ
- Tìm kiếm liên hệ theo tên, số điện thoại, email
- Lọc liên hệ theo nhóm hoặc tag
- Xóa mềm (soft delete) với khả năng khôi phục
- Gắn nhiều tag cho mỗi liên hệ
- Phân loại liên hệ theo nhóm

### Quản lý nhóm và tag

- Tạo và quản lý các nhóm liên hệ
- Tạo và quản lý các tag
- Thống kê số lượng liên hệ theo nhóm/tag

### Thùng rác

- Xem danh sách liên hệ đã xóa
- Khôi phục liên hệ đơn lẻ hoặc nhiều liên hệ
- Xóa vĩnh viễn liên hệ
- Làm trống thùng rác

### Dashboard

- Thống kê tổng quan: số liên hệ, nhóm, tag
- Hiển thị liên hệ gần đây
- Truy cập nhanh các chức năng chính

### Sao lưu và khôi phục

- **Xuất danh bạ ra file CSV**: Xuất toàn bộ hoặc liên hệ đã lọc
- **Nhập danh bạ từ file CSV**: Import với validation đầy đủ, báo cáo chi tiết
- **Quick Add Contact**: Thêm nhanh liên hệ từ Dashboard
- **Tự động sao lưu định kỳ**: Backup tự động vào thư mục `data/backup/`

> **Xem thêm**: `HUONG_DAN_IMPORT_EXPORT.md` và `BAO_CAO_CHUC_NANG.md`

## Yêu cầu hệ thống

- **Python**: 3.10 trở lên
- **MySQL**: 8.0 trở lên
- **Hệ điều hành**: Windows, Linux, macOS
- **RAM**: Tối thiểu 2GB
- **Dung lượng ổ cứng**: 100MB

## Cài đặt

### 1. Clone hoặc tải xuống dự án

```bash
git clone https://github.com/yourusername/phonebook.git
cd phonebook
```

### 2. Tạo môi trường ảo (Virtual Environment)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

Các thư viện bao gồm:

- `mysql-connector-python==8.2.0` - Kết nối MySQL
- `bcrypt==4.1.1` - Mã hóa mật khẩu
- `Pillow==10.1.0` - Xử lý hình ảnh

### 4. Cài đặt và cấu hình MySQL

Đảm bảo MySQL Server đã được cài đặt và đang chạy:

```bash
# Windows - Kiểm tra service
Get-Service -Name "*mysql*"

# Linux
sudo systemctl status mysql

# macOS
brew services list | grep mysql
```

### 5. Tạo database

Database sẽ được tự động tạo khi chạy ứng dụng lần đầu tiên. Tuy nhiên, bạn có thể tạo thủ công:

```sql
CREATE DATABASE phonebook_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Cấu hình

### Cấu hình Database

Mở file `config.py` và chỉnh sửa thông tin kết nối MySQL:

```python
DB_CONFIG = {
    'host': 'localhost',      # Địa chỉ MySQL server
    'user': 'root',           # Tên đăng nhập MySQL
    'password': 'root',       # Mật khẩu MySQL (thay đổi theo cài đặt của bạn)
    'database': 'phonebook_db',
    'port': 3306
}
```

### Tùy chỉnh giao diện

Bạn có thể tùy chỉnh màu sắc và font chữ trong file `config.py`:

```python
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'success': '#27ae60',
    'danger': '#e74c3c',
    # ...
}

FONTS = {
    'title': ('Segoe UI', 18, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    # ...
}
```

## Sử dụng

### Khởi chạy ứng dụng

```bash
# Đảm bảo đang ở trong môi trường ảo
python main.py
```

### Quy trình sử dụng cơ bản

1. **Đăng ký tài khoản mới**

   - Nhấn "Đăng ký ngay" ở màn hình đăng nhập
   - Điền đầy đủ thông tin (họ tên, username, email, số điện thoại, địa chỉ)
   - Nhập mật khẩu và xác nhận mật khẩu

2. **Đăng nhập**

   - Nhập username và password
   - Nhấn "Đăng nhập"

3. **Thêm liên hệ mới**

   - Vào mục "Danh bạ"
   - Nhấn nút "Thêm liên hệ"
   - Điền thông tin liên hệ
   - Chọn nhóm (nếu có)

4. **Tạo nhóm và tag**

   - Vào mục "Nhóm" để tạo nhóm mới
   - Vào mục "Tag" để tạo tag mới
   - Gán nhóm/tag cho liên hệ

5. **Tìm kiếm và lọc**

   - Sử dụng thanh tìm kiếm ở mục "Danh bạ"
   - Lọc theo nhóm hoặc tag

6. **Quản lý thùng rác**
   - Xem liên hệ đã xóa trong mục "Thùng rác"
   - Khôi phục hoặc xóa vĩnh viễn

## Cấu trúc dự án

```
PhonebookPY/
├── config.py                 # Cấu hình ứng dụng
├── db.py                     # Quản lý kết nối database
├── main.py                   # File khởi chạy chính
├── requirements.txt          # Danh sách thư viện
│
├── models/                   # Lớp Model (Data layer)
│   ├── __init__.py
│   ├── base_model.py        # Model cơ sở
│   ├── user_model.py        # Model người dùng
│   ├── contact_model.py     # Model liên hệ
│   ├── group_model.py       # Model nhóm
│   └── tag_model.py         # Model tag
│
├── controllers/              # Lớp Controller (Business logic)
│   ├── auth_controller.py   # Xử lý đăng nhập/đăng ký
│   ├── contact_controller.py
│   ├── dashboard_controller.py
│   ├── group_controller.py
│   ├── tag_controller.py
│   ├── profile_controller.py
│   └── trash_controller.py
│
├── views/                    # Lớp View (Presentation layer)
│   ├── __init__.py
│   ├── login_view.py        # Màn hình đăng nhập
│   ├── register_view.py     # Màn hình đăng ký
│   ├── dashboard_view.py    # Màn hình tổng quan
│   ├── contact_view.py      # Màn hình danh bạ
│   ├── group_view.py        # Màn hình nhóm
│   ├── tag_view.py          # Màn hình tag
│   ├── trash_view.py        # Màn hình thùng rác
│   ├── profile_view.py      # Màn hình hồ sơ
│   └── components/          # Components tái sử dụng
│       ├── messagebox_custom.py
│       ├── navbar.py
│       └── sidebar.py
│
├── utils/                    # Tiện ích
│   ├── __init__.py
│   ├── logger.py            # Ghi log
│   ├── security.py          # Mã hóa mật khẩu
│   ├── validators.py        # Xác thực dữ liệu
│   ├── helpers.py           # Hàm tiện ích
│   └── backup.py            # Sao lưu/khôi phục
│
├── data/                     # Dữ liệu và log
│   ├── error_log.txt
│   ├── backup/              # Thư mục sao lưu
│   └── exports/             # Thư mục xuất file
│
├── assets/                   # Tài nguyên
│   ├── fonts/
│   ├── icons/
│   └── style/
│
└── docs/                     # Tài liệu
    ├── requirements.md
    ├── database_schema.sql
    ├── erd.drawio.png
    └── ...
```

## Công nghệ sử dụng

### Backend

- **Python 3.14**: Ngôn ngữ lập trình chính
- **MySQL 8.0**: Hệ quản trị cơ sở dữ liệu
- **mysql-connector-python**: Thư viện kết nối MySQL
- **bcrypt**: Mã hóa mật khẩu

### Frontend

- **Tkinter**: Framework GUI tích hợp sẵn trong Python
- **ttk**: Themed widgets cho Tkinter

### Kiến trúc

- **MVC Pattern**: Tách biệt Model-View-Controller
- **Singleton Pattern**: Quản lý kết nối database
- **Repository Pattern**: Truy xuất dữ liệu

## Bảo mật

### Mã hóa mật khẩu

- Sử dụng bcrypt với 12 rounds để hash mật khẩu
- Không lưu trữ mật khẩu dạng plain text

### Xác thực dữ liệu

- Validate email, số điện thoại, username
- Sanitize input để tránh SQL injection
- Kiểm tra độ mạnh mật khẩu

### Bảo vệ dữ liệu

- Foreign key constraints để đảm bảo tính toàn vẹn
- Soft delete cho khả năng khôi phục
- Transaction để đảm bảo ACID

### Quy tắc validation

- **Email**: Định dạng email hợp lệ
- **Số điện thoại**: 10-11 chữ số (định dạng Việt Nam)
- **Username**: 3-20 ký tự, chỉ chữ cái, số và dấu gạch dưới
- **Mật khẩu**: Tối thiểu 6 ký tự

## Tài liệu

### Database Schema

Chi tiết về cấu trúc database có trong file `docs/database_schema.sql`

**Các bảng chính:**

- `users`: Lưu thông tin người dùng
- `contacts`: Lưu thông tin liên hệ
- `my_groups`: Lưu nhóm liên hệ
- `tags`: Lưu tag
- `contact_tags`: Bảng liên kết contact và tag (many-to-many)

### API Documentation

Xem chi tiết các phương thức của Models và Controllers trong code docstrings.

### Diagrams

- **ERD**: `docs/erd.drawio.png` - Sơ đồ quan hệ thực thể
- **Use Case**: `docs/usecase.drawio.png` - Sơ đồ use case
- **Class Diagram**: `docs/class.drawio.png` - Sơ đồ lớp
- **DFD**: `docs/dfd0.drawio.png`, `docs/dfd1.drawio.png` - Sơ đồ luồng dữ liệu

##  Xử lý lỗi

### Log Files

Tất cả lỗi được ghi vào file `data/error_log.txt` với định dạng:

```
[2025-11-02 10:30:45] ERROR: Chi tiết lỗi...
```

### Các lỗi thường gặp

1. **Không kết nối được MySQL**

   - Kiểm tra MySQL service đang chạy
   - Kiểm tra thông tin đăng nhập trong `config.py`
   - Kiểm tra port 3306 không bị chặn

2. **ModuleNotFoundError**

   - Đảm bảo đã kích hoạt virtual environment
   - Chạy lại `pip install -r requirements.txt`

3. **Table already exists**
   - Ứng dụng tự động xử lý, không cần lo lắng
   - Database sẽ sử dụng bảng hiện có

## 📝 Ghi chú phát triển

### Conventions

- Tên biến: `snake_case`
- Tên class: `PascalCase`
- Tên hằng số: `UPPER_SNAKE_CASE`
- Docstrings: Google style

### Git Workflow

```bash
# Tạo branch mới cho feature
git checkout -b feature/ten-feature

# Commit changes
git add .
git commit -m "Add: mô tả feature"

# Push và tạo Pull Request
git push origin feature/ten-feature
```

##  Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork dự án
2. Tạo branch cho feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

Dự án này được phát hành dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## � Tài liệu bổ sung

- 📖 [Hướng dẫn Import/Export CSV](HUONG_DAN_IMPORT_EXPORT.md)
- 💾 [Hướng dẫn Backup và Khôi phục](HUONG_DAN_BACKUP.md)
- 📊 [Báo cáo Chức năng](BAO_CAO_CHUC_NANG.md)
- 🧪 [Testing Document](TESTING_DOCUMENT.md)
- 🔧 [Test Export Fix](docs/TEST_EXPORT_FIX.md)


