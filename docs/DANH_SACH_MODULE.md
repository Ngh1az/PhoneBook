# DANH SÁCH MODULE VÀ THƯ VIỆN - PHONEBOOK APPLICATION

## 📦 TỔNG QUAN

Dự án PhoneBook sử dụng **RẤT ÍT module bên ngoài**, chủ yếu dựa vào thư viện tích hợp sẵn của Python.

⚠️ **CHÚ Ý**: Module `Pillow` trong `requirements.txt` **KHÔNG ĐƯỢC SỬ DỤNG** - có thể xóa để giảm dung lượng!

---

## 🔢 SỐ LƯỢNG

### Module cần cài đặt (requirements.txt):

```
Tổng số: 3 modules
  ✅ 2 modules đang được sử dụng (mysql-connector-python, bcrypt)
  ❌ 1 module KHÔNG sử dụng (Pillow) - có thể xóa
```

### Module tích hợp sẵn Python:

```
Tổng số: ~10+ modules (không cần cài)
```

---

## 📋 CHI TIẾT CÁC MODULE

### 1️⃣ Module CẦN CÀI ĐẶT (3 modules)

#### 1. **mysql-connector-python** v8.2.0

- **Công dụng**: Kết nối và tương tác với MySQL database
- **Cài đặt**: `pip install mysql-connector-python==8.2.0`
- **Dung lượng**: ~20MB
- **Sử dụng ở**:
  - `db.py` - Quản lý kết nối database
  - Tất cả các model files
- **Lý do cần**: Python không có driver MySQL tích hợp sẵn

#### 2. **bcrypt** v4.1.1

- **Công dụng**: Mã hóa (hash) mật khẩu an toàn
- **Cài đặt**: `pip install bcrypt==4.1.1`
- **Dung lượng**: ~1-2MB
- **Sử dụng ở**:
  - `utils/security.py` - Hash và verify password
  - `controllers/auth_controller.py` - Đăng ký/đăng nhập
- **Lý do cần**: Bcrypt là thuật toán hash mạnh mẽ, an toàn hơn MD5/SHA

#### 3. **Pillow** v10.1.0 ⚠️ KHÔNG SỬ DỤNG

- **Công dụng**: Xử lý hình ảnh (resize, crop, format...)
- **Cài đặt**: `pip install Pillow==10.1.0`
- **Dung lượng**: ~5-8MB
- **Tình trạng**:
  - ❌ **KHÔNG CÓ BẤT KỲ CODE NÀO SỬ DỤNG PILLOW**
  - ❌ **KHÔNG CÓ TÍNH NĂNG AVATAR/ẢNH TRONG DỰ ÁN**
  - ✅ Module được thêm vào `requirements.txt` để dự phòng
- **Quyết định**:
  - 💡 Có thể **XÓA** khỏi `requirements.txt` để giảm dung lượng
  - 💡 Hoặc **GIỮ LẠI** nếu dự định làm tính năng avatar/ảnh sau

---

### 2️⃣ Module TÍCH HỢP SẴN Python (Không cần cài)

#### Tkinter & ttk

```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
```

- **Công dụng**: Xây dựng giao diện đồ họa (GUI)
- **Tích hợp**: Python 3.x (Windows, macOS, Linux)
- **Sử dụng**: Tất cả các file view

#### CSV

```python
import csv
```

- **Công dụng**: Đọc/ghi file CSV (Export/Import)
- **Sử dụng**: `utils/backup.py`

#### OS

```python
import os
```

- **Công dụng**: Thao tác với file system, đường dẫn
- **Sử dụng**: `config.py`, `utils/backup.py`, `utils/logger.py`

#### Datetime

```python
from datetime import datetime
```

- **Công dụng**: Xử lý ngày tháng, timestamp
- **Sử dụng**: `models/base_model.py`, `utils/backup.py`

#### Re (Regular Expression)

```python
import re
```

- **Công dụng**: Kiểm tra pattern (email, phone, username)
- **Sử dụng**: `utils/validators.py`

#### Sys

```python
import sys
```

- **Công dụng**: System-specific parameters
- **Sử dụng**: `main.py`

#### Typing

```python
from typing import Optional, Dict, List, Tuple
```

- **Công dụng**: Type hints (tăng tính rõ ràng code)
- **Sử dụng**: Nhiều file (optional, không bắt buộc)

---

## 📊 BẢNG TỔNG HỢP

| Loại             | Số lượng | Cần cài? | Dung lượng |
| ---------------- | -------- | -------- | ---------- |
| **Cần cài đặt**  | 3        | ✅ Có    | ~25-30MB   |
| **Tích hợp sẵn** | 10+      | ❌ Không | 0MB        |
| **TỔNG**         | 13+      | -        | ~25-30MB   |

---

## 💾 DUNG LƯỢNG TỔNG THỂ

```
┌─────────────────────────────────────┐
│ Source code:           ~500 KB      │
│ Python modules:        ~25-30 MB    │
│ MySQL:                 ~200 MB      │
│ Database data:         ~1-10 MB     │
│ ─────────────────────────────────   │
│ TỔNG:                  ~230-245 MB  │
└─────────────────────────────────────┘
```

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Cách 1: Cài tất cả cùng lúc (Khuyến nghị)

```bash
pip install -r requirements.txt
```

### Cách 2: Cài từng module

```bash
pip install mysql-connector-python==8.2.0
pip install bcrypt==4.1.1
pip install Pillow==10.1.0
```

### Kiểm tra đã cài đặt chưa

```bash
pip list | findstr "mysql bcrypt Pillow"
```

### Kiểm tra version

```bash
pip show mysql-connector-python
pip show bcrypt
pip show Pillow
```

---

## 🔍 CHI TIẾT SỬ DỤNG

### mysql-connector-python

**File sử dụng:**

- `db.py` (main usage)
- `models/base_model.py`
- `models/user_model.py`
- `models/contact_model.py`
- `models/group_model.py`
- `models/tag_model.py`

**Code mẫu:**

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="phonebook_db"
)
```

---

### bcrypt

**File sử dụng:**

- `utils/security.py` (main usage)
- `controllers/auth_controller.py`

**Code mẫu:**

```python
import bcrypt

# Hash password
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify password
is_valid = bcrypt.checkpw(password.encode(), hashed)
```

---

### Pillow

**File sử dụng:**

- (Dự phòng, chưa sử dụng nhiều)

**Code mẫu (future):**

```python
from PIL import Image

# Resize avatar
img = Image.open("avatar.png")
img = img.resize((100, 100))
img.save("avatar_small.png")
```

---

## 📈 SO SÁNH VỚI CÁC DỰ ÁN KHÁC

| Framework/App   | Số modules | Dung lượng   |
| --------------- | ---------- | ------------ |
| PhoneBook (này) | **3**      | **~25MB** ✅ |
| Django App      | 50+        | ~200MB       |
| Flask App       | 20-30      | ~100MB       |
| React App       | 1000+      | ~500MB       |
| Electron App    | 500+       | ~300MB       |

➡️ **Kết luận**: Dự án này **RẤT NHẸ** và đơn giản!

---

## 💡 TẠI SAO CHỈ 3 MODULES?

### Ưu điểm:

✅ **Nhẹ nhàng**: Dễ cài đặt, ít dependencies  
✅ **Nhanh chóng**: Setup trong vài phút  
✅ **Ổn định**: Ít conflict giữa các thư viện  
✅ **Bảo mật**: Ít rủi ro từ third-party  
✅ **Portable**: Dễ di chuyển giữa các máy

### Nhược điểm:

❌ Giao diện không hiện đại như web frameworks  
❌ Không có fancy features như React/Vue  
❌ Tkinter có hạn chế về styling

---

## 🔧 TROUBLESHOOTING

### Lỗi: "No module named 'mysql'"

```bash
# Giải pháp:
pip install mysql-connector-python
```

### Lỗi: "No module named 'bcrypt'"

```bash
# Giải pháp:
pip install bcrypt
```

### Lỗi: "No module named 'PIL'"

```bash
# Giải pháp:
pip install Pillow
```

### Lỗi: "Microsoft Visual C++ required" (Windows)

```bash
# Giải pháp:
# Tải và cài: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Hoặc dùng wheel file pre-compiled
```

---

## 🎯 KẾT LUẬN

Dự án PhoneBook sử dụng:

- ✅ **Chỉ 3 modules bên ngoài**
- ✅ **Tổng dung lượng ~25-30MB**
- ✅ **Setup trong < 5 phút**
- ✅ **Tương thích đa nền tảng**

**➡️ Đây là một dự án MINIMALIST, tập trung vào chức năng core!**

---

**Cập nhật:** 11/11/2025  
**Version:** 1.0
