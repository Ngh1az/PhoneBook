# HƯỚNG DẪN SAO LƯU (BACKUP) - PHONEBOOK APPLICATION

## 📦 TỔNG QUAN HỆ THỐNG BACKUP

Ứng dụng PhoneBook có 2 hệ thống sao lưu:

### 1. **Sao lưu Thủ công (Manual Backup)**

- ✅ Xuất CSV từ Dashboard
- ✅ Xuất CSV từ trang Quản lý liên hệ
- ✅ Người dùng kiểm soát hoàn toàn

### 2. **Sao lưu Tự động (Auto Backup)**

- ⚠️ Hiện chưa được kích hoạt
- 🔧 Đang trong kế hoạch phát triển

---

## 📤 CÁC CÁCH SAO LƯU

### Phương pháp 1: Xuất CSV từ Dashboard

**Các bước:**

1. Đăng nhập vào ứng dụng
2. Ở trang chủ (Dashboard)
3. Tìm mục **"Sao lưu & Khôi phục"**
4. Nhấn nút **"📤 Xuất ra CSV"**
5. File sẽ được lưu tự động vào: `data/exports/contacts_backup_YYYYMMDD_HHMMSS.csv`

**Ưu điểm:**

- ✅ Xuất toàn bộ liên hệ
- ✅ Bao gồm thông tin nhóm và thẻ
- ✅ Tên file có timestamp, dễ theo dõi
- ✅ Thông báo đường dẫn file sau khi xuất

**File CSV bao gồm:**

```csv
first_name,last_name,phone,email,address,notes,group_name,tags
Nguyễn,Văn A,0123456789,email@example.com,Hà Nội,Ghi chú,Bạn bè,Important;Work
```

---

### Phương pháp 2: Xuất CSV từ Trang Quản lý Liên hệ

**Các bước:**

1. Vào trang **"Quản lý liên hệ"**
2. (Tùy chọn) Tìm kiếm hoặc lọc theo nhóm/thẻ
3. Nhấn nút **"📤 Xuất CSV"** ở góc trên
4. File được lưu vào `data/exports/`

**Ưu điểm:**

- ✅ Có thể xuất chỉ một phần liên hệ (đã lọc)
- ✅ Linh hoạt hơn
- ✅ Phù hợp khi muốn backup theo nhóm cụ thể

**Ví dụ:**

- Lọc nhóm "Gia đình" → Xuất → Chỉ có liên hệ gia đình
- Tìm kiếm "Nguyễn" → Xuất → Chỉ có liên hệ có tên Nguyễn

---

### Phương pháp 3: Backup Thủ công qua Database

**Cho người dùng nâng cao:**

```bash
# Backup MySQL database
mysqldump -u root -p phonebook_db > backup_phonebook_YYYYMMDD.sql

# Restore từ backup
mysql -u root -p phonebook_db < backup_phonebook_YYYYMMDD.sql
```

---

## 📂 CẤU TRÚC THƯ MỤC BACKUP

```
PhonebookPY/
├── data/
│   ├── exports/              # CSV xuất bằng tay
│   │   ├── contacts_backup_20251111_143022.csv
│   │   ├── contacts_backup_20251111_150145.csv
│   │   └── ...
│   │
│   └── backup/               # CSV backup tự động (future)
│       ├── auto_backup_20251111_080000.csv
│       ├── auto_backup_20251112_080000.csv
│       └── ...
```

---

## 🔄 KHÔI PHỤC TỪ BACKUP

### Từ file CSV:

**Các bước:**

1. Chuẩn bị file CSV backup (từ `data/exports/` hoặc `data/backup/`)
2. Vào Dashboard hoặc trang Quản lý liên hệ
3. Nhấn **"📥 Nhập từ CSV"**
4. Chọn file backup cần khôi phục
5. Xác nhận nhập
6. Xem báo cáo: số liên hệ imported, skipped, lỗi

**Lưu ý:**

- ⚠️ Liên hệ có số điện thoại trùng sẽ bị bỏ qua
- ✅ Nhóm sẽ được tự động tìm theo tên (nếu tồn tại)
- ✅ Liên hệ không hợp lệ sẽ bị skip với báo lỗi

---

## 📋 CHIẾN LƯỢC BACKUP KHUYẾN NGHỊ

### Cho người dùng cá nhân:

- **Hàng tuần**: Xuất CSV toàn bộ liên hệ
- **Trước khi nhập CSV**: Luôn backup trước
- **Sau khi chỉnh sửa nhiều**: Tạo backup ngay

### Cho tổ chức:

- **Hàng ngày**: Backup database MySQL
- **Hàng tuần**: Xuất CSV để lưu trữ
- **Hàng tháng**: Sao lưu ra ổ đĩa ngoài hoặc cloud

---

## 🛠️ TÍNH NĂNG BACKUP TỰ ĐỘNG (ĐANG PHÁT TRIỂN)

### Kế hoạch:

**Auto Backup khi:**

- ✅ Khởi động ứng dụng (1 lần/ngày)
- ✅ Thoát ứng dụng (nếu có thay đổi)
- ✅ Sau khi nhập CSV lớn
- ✅ Định kỳ mỗi tuần

**Cấu hình (future):**

```python
# config.py
AUTO_BACKUP_ENABLED = True
AUTO_BACKUP_FREQUENCY = "daily"  # daily, weekly, on_exit
MAX_BACKUP_FILES = 30  # Giữ tối đa 30 file backup
```

---

## 💡 MẸO VÀ THỦ THUẬT

### 1. Đặt tên file backup có ý nghĩa:

Khi xuất CSV, bạn có thể đổi tên file:

```
contacts_backup_20251111_143022.csv
↓
gia_dinh_backup_2025_11_11.csv
```

### 2. Lưu backup ở nhiều nơi:

- ✅ Trong máy: `data/exports/`
- ✅ USB/Ổ cứng ngoài
- ✅ Cloud: Google Drive, OneDrive, Dropbox

### 3. Kiểm tra backup định kỳ:

- Mở file CSV bằng Excel
- Đảm bảo dữ liệu đầy đủ
- Test restore trên môi trường thử nghiệm

### 4. Backup trước khi update:

- Trước khi cập nhật ứng dụng
- Xuất CSV toàn bộ
- Backup database MySQL

---

## ❓ FAQ - CÂU HỎI THƯỜNG GẶP

**Q: File backup lưu ở đâu?**
A: Mặc định trong `data/exports/` với tên `contacts_backup_YYYYMMDD_HHMMSS.csv`

**Q: Có thể backup tự động không?**
A: Hiện tại chưa có, đang trong kế hoạch phát triển. Bạn có thể xuất CSV thủ công.

**Q: Backup có bao gồm ảnh liên hệ không?**
A: Không, chỉ backup thông tin text (tên, SĐT, email, địa chỉ, ghi chú, nhóm, thẻ).

**Q: File backup có giới hạn dung lượng?**
A: Không, phụ thuộc vào số lượng liên hệ. 1000 liên hệ ≈ 150-200KB.

**Q: Có thể chỉnh sửa file backup không?**
A: Có, mở bằng Excel, chỉnh sửa, lưu lại, rồi import vào ứng dụng.

**Q: Nếu import file bị lỗi?**
A: Ứng dụng sẽ báo chi tiết từng dòng lỗi. Sửa file và import lại.

**Q: Backup có xóa dữ liệu cũ không?**
A: KHÔNG! Backup chỉ xuất ra file, không ảnh hưởng database.

**Q: Có thể backup database MySQL không?**
A: Có, dùng `mysqldump` hoặc MySQL Workbench để backup toàn bộ database.

---

## 🔐 BẢO MẬT FILE BACKUP

### Khuyến nghị:

1. ✅ Không chia sẻ file backup công khai
2. ✅ Mã hóa USB/ổ đĩa chứa backup
3. ✅ Sử dụng mật khẩu khi lưu trên cloud
4. ✅ Xóa file backup cũ không cần thiết
5. ✅ Backup chứa thông tin cá nhân - cần bảo vệ

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề về backup:

1. Kiểm tra file `data/error_log.txt`
2. Đọc lại hướng dẫn trong `HUONG_DAN_IMPORT_EXPORT.md`
3. Liên hệ nhóm phát triển

---

**Cập nhật lần cuối:** 11/11/2025  
**Version:** 1.0
