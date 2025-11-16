# 🚀 HƯỚNG DẪN DEPLOY PHONEBOOK APPLICATION

## 📦 PHƯƠNG PHÁP 1: BUILD FILE .EXE BẰNG PYINSTALLER (KHUYẾN NGHỊ)

### Bước 1: Chuẩn bị môi trường

```bash
# Đảm bảo đã cài Python 3.10+ và MySQL
python --version
mysql --version

# Kích hoạt virtual environment (nếu chưa)
.venv\Scripts\activate      # Windows CMD
# HOẶC
.\.venv\Scripts\Activate.ps1  # PowerShell
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Bước 3: Build file .exe

#### **Cách A: Dùng script tự động (KHUYẾN NGHỊ)**

```bash
# Windows CMD
build.bat

# PowerShell
.\build.ps1
```

#### **Cách B: Build thủ công**

```bash
# Clean build cũ
pyinstaller --clean --noconfirm PhoneBook.spec

# HOẶC build từ đầu (không dùng .spec)
pyinstaller --onefile --windowed --name PhoneBook main.py
```

### Bước 4: Kiểm tra kết quả

```
dist/
  └── PhoneBook.exe     ← File thực thi (50-80 MB)
```

### Bước 5: Chạy ứng dụng

```bash
cd dist
PhoneBook.exe
```

---

## 📋 CẤU HÌNH FILE .SPEC

File `PhoneBook.spec` đã được tùy chỉnh để:

- ✅ Include thư mục `assets/` (icons, fonts, styles)
- ✅ Include file `config.py`
- ✅ Tối ưu kích thước (exclude Pillow, numpy, pandas)
- ✅ Hỗ trợ MySQL Connector và bcrypt
- ✅ Single file executable (dễ phân phối)

**Chỉnh sửa .spec file nếu cần**:

```python
# Ẩn console window (chỉ hiện GUI)
console=False,  # Thay vì True

# Thêm icon
icon='assets/icon.ico',  # Nếu có file .ico

# Thêm dữ liệu khác
datas=[
    ('assets', 'assets'),
    ('config.py', '.'),
    ('README.md', '.'),  # Ví dụ thêm file
],
```

---

## 🗂️ PHƯƠNG PHÁP 2: PHÂN PHỐI CODE (CHO DEVELOPER)

### Package toàn bộ source code

```bash
# Tạo thư mục phân phối
mkdir PhoneBook_Source
cp -r * PhoneBook_Source/
cd PhoneBook_Source

# Xóa file không cần thiết
rm -rf __pycache__ .venv build dist *.spec
```

### Hướng dẫn cho người nhận

1. Cài Python 3.10+
2. Chạy:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

---

## 💾 CẤU HÌNH DATABASE TRƯỚC KHI DEPLOY

### Chuẩn bị MySQL

```sql
-- 1. Tạo database
CREATE DATABASE IF NOT EXISTS phonebook_db;

-- 2. Tạo user (nếu cần)
CREATE USER 'phonebook_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON phonebook_db.* TO 'phonebook_user'@'localhost';
FLUSH PRIVILEGES;
```

### Cập nhật `config.py`

```python
# Cấu hình MySQL cho production
DB_CONFIG = {
    "host": "localhost",      # Hoặc IP server
    "user": "phonebook_user", # User thật
    "password": "your_password",
    "database": "phonebook_db",
    "port": 3306,
}
```

---

## 📦 DISTRIBUTION (Phân phối cho người dùng cuối)

### Tạo package đầy đủ

```
PhoneBook_v1.0/
  ├── PhoneBook.exe          ← Executable
  ├── README.txt             ← Hướng dẫn cài đặt
  ├── config_template.txt    ← Mẫu config MySQL
  └── database_setup.sql     ← Script tạo database
```

### File README.txt cho user

```
PHONEBOOK APPLICATION v1.0
==========================

CÀI ĐẶT:
1. Cài MySQL Server 8.0+
2. Chạy file database_setup.sql trong MySQL
3. Chỉnh sửa file config.py (nếu cần)
4. Double-click PhoneBook.exe

ĐĂNG NHẬP MẶC ĐỊNH:
Username: admin
Password: 123456

HỖ TRỢ:
Email: support@phonebook.com
```

---

## 🔧 TROUBLESHOOTING

### Lỗi "MySQL not found"

- **Nguyên nhân**: PyInstaller không tìm thấy mysql-connector
- **Giải pháp**: Thêm vào `hiddenimports` trong .spec:
  ```python
  hiddenimports=['mysql.connector.locales.eng.client_error'],
  ```

### File .exe quá lớn (>100MB)

- **Giải pháp**:
  ```python
  # Thêm vào excludes trong .spec
  excludes=['matplotlib', 'numpy', 'pandas', 'PIL'],
  ```

### Console window hiện ra

- **Giải pháp**: Đổi `console=False` trong .spec

### Import error khi chạy .exe

- **Kiểm tra**:
  ```bash
  pyinstaller --log-level DEBUG PhoneBook.spec
  # Xem log trong dist/PhoneBook/
  ```

---

## 📊 SO SÁNH PHƯƠNG PHÁP DEPLOY

| Phương pháp               | Ưu điểm                                | Nhược điểm                                | Kích thước |
| ------------------------- | -------------------------------------- | ----------------------------------------- | ---------- |
| **PyInstaller (onefile)** | ✅ Dễ phân phối<br>✅ Không cần Python | ❌ File lớn (50-80MB)<br>❌ Startup chậm  | ~70 MB     |
| **Source code**           | ✅ Nhẹ (5-10 MB)<br>✅ Dễ debug        | ❌ Cần cài Python<br>❌ Phức tạp cho user | ~8 MB      |
| **PyInstaller (onedir)**  | ✅ Startup nhanh<br>✅ Dễ update       | ❌ Nhiều file<br>❌ Khó phân phối         | ~100 MB    |

**KHUYẾN NGHỊ**: Dùng **PyInstaller onefile** cho end-users.

---

## 🚀 NÂNG CAO

### Auto-update mechanism

- Sử dụng `PyUpdater` hoặc tự code update checker
- Check version từ server khi khởi động

### Code signing (Windows)

```bash
signtool sign /f certificate.pfx /p password PhoneBook.exe
```

### Tạo installer với NSIS

```bash
# Tạo file .nsi và compile với NSIS
makensis phonebook_installer.nsi
```

---

## 📝 CHECKLIST TRƯỚC KHI DEPLOY

- [ ] Test ứng dụng trên máy sạch (không có Python)
- [ ] Kiểm tra kết nối MySQL
- [ ] Test import/export CSV
- [ ] Verify backup/restore functionality
- [ ] Kiểm tra tất cả views (login, dashboard, contacts, etc.)
- [ ] Đọc error logs (nếu có)
- [ ] Chuẩn bị documentation cho user
- [ ] Test trên Windows 10/11 khác nhau

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:

1. `data/error_log.txt` - Error logs của app
2. Console output khi chạy .exe
3. MySQL server status: `mysql -u root -p`

**Good luck with your deployment!** 🎉
