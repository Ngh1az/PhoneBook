# Hướng Dẫn Sử Dụng Tính Năng Import/Export CSV

## 📤 XUẤT LIÊN HỆ RA FILE CSV (Export)

### Từ Dashboard:
1. Đăng nhập vào ứng dụng
2. Ở trang Dashboard, tìm mục "Sao lưu & Khôi phục"
3. Nhấn nút **"📤 Xuất ra CSV"**
4. File CSV sẽ được tự động tạo trong thư mục `data/exports/`
5. Thông báo sẽ hiển thị đường dẫn file đã xuất

### Từ Trang Quản Lý Liên Hệ:
1. Vào trang "Quản lý liên hệ"
2. (Tùy chọn) Sử dụng tìm kiếm hoặc lọc để chọn liên hệ cần xuất
3. Nhấn nút **"📤 Xuất CSV"** ở góc trên bên phải
4. Chỉ các liên hệ đang hiển thị sẽ được xuất ra file

### Định dạng file CSV xuất ra:
```csv
first_name,last_name,phone,email,address,notes,group_name,tags
Nguyễn,Văn A,0123456789,email@example.com,Hà Nội,Ghi chú,Bạn bè,Important;Work
```

---

## 📥 NHẬP LIÊN HỆ TỪ FILE CSV (Import)

### Từ Dashboard:
1. Chuẩn bị file CSV theo đúng format (xem bên dưới)
2. Ở trang Dashboard, tìm mục "Sao lưu & Khôi phục"
3. Nhấn nút **"📥 Nhập từ CSV"**
4. Chọn file CSV từ máy tính
5. Xác nhận nhập dữ liệu
6. Xem kết quả: số liên hệ đã nhập, bỏ qua, và các lỗi (nếu có)

### Từ Trang Quản Lý Liên Hệ:
1. Vào trang "Quản lý liên hệ"
2. Nhấn nút **"📥 Nhập CSV"** ở góc trên bên phải
3. Chọn file CSV và xác nhận
4. Xem báo cáo kết quả nhập

### Format File CSV để nhập:

**File mẫu:** `sample_import.csv` (có sẵn trong thư mục gốc)

```csv
first_name,last_name,phone,email,address,notes,group_name,tags
Nguyễn,Văn A,0123456789,nguyenvana@gmail.com,Hà Nội,Bạn cũ,Bạn bè,Important
Trần,Thị B,0987654321,tranthib@gmail.com,TP.HCM,Đồng nghiệp,Công việc,Work
Lê,Văn C,0901234567,levanc@gmail.com,Đà Nẵng,Họ hàng,Gia đình,
```

**Lưu ý quan trọng:**
- Dòng đầu tiên PHẢI là header (tên các cột)
- Các cột bắt buộc: `first_name`, `last_name`, `phone`
- Các cột tùy chọn: `email`, `address`, `notes`, `group_name`, `tags`
- Số điện thoại phải có 10-11 chữ số
- Email phải đúng định dạng (nếu có)
- Nếu `group_name` không tồn tại, liên hệ sẽ không được gán nhóm
- Tags có thể được phân tách bằng dấu chấm phẩy (;)
- Các liên hệ có số điện thoại trùng lặp sẽ bị bỏ qua

### Xử lý lỗi:
- **Số điện thoại trùng**: Bỏ qua, không nhập
- **Email sai định dạng**: Bỏ qua dòng đó
- **Thiếu thông tin bắt buộc**: Bỏ qua dòng đó
- **Nhóm không tồn tại**: Nhập liên hệ nhưng không gán nhóm

---

## ➕ THÊM NHANH LIÊN HỆ (Quick Add Contact)

### Từ Dashboard:
1. Ở trang Dashboard, tìm mục "Sao lưu & Khôi phục"
2. Nhấn nút **"➕ Thêm nhanh liên hệ"**
3. Điền thông tin vào form:
   - Tên (bắt buộc)
   - Họ (bắt buộc)
   - Số điện thoại (bắt buộc, 10-11 chữ số)
   - Email (tùy chọn, phải đúng định dạng)
   - Nhóm (tùy chọn, chọn từ danh sách)
4. Nhấn nút **"Lưu"**
5. Dashboard sẽ tự động cập nhật thống kê

**Lợi ích:**
- Thêm liên hệ nhanh chóng mà không cần chuyển sang trang Quản lý liên hệ
- Form đơn giản, chỉ có các trường cần thiết
- Tiết kiệm thời gian khi cần thêm nhiều liên hệ

---

## 🔍 MỘT SỐ TIPS HỮU ÍCH

1. **Backup định kỳ**: Xuất CSV thường xuyên để sao lưu dữ liệu
2. **Chỉnh sửa hàng loạt**: Xuất CSV → Sửa bằng Excel → Nhập lại
3. **Di chuyển dữ liệu**: Dễ dàng chia sẻ danh bạ giữa các máy
4. **Format nhất quán**: Sử dụng file mẫu để đảm bảo không lỗi
5. **Kiểm tra trước khi nhập**: Mở file CSV bằng Excel để xem trước

---

## ❓ TROUBLESHOOTING

**Q: File CSV không nhập được?**
A: Kiểm tra:
- File có đúng format không?
- Dòng đầu có phải là header không?
- Encoding của file (nên dùng UTF-8)

**Q: Tại sao một số liên hệ bị bỏ qua?**
A: Xem báo cáo chi tiết sau khi nhập, thường do:
- Số điện thoại trùng lặp
- Thiếu thông tin bắt buộc
- Email hoặc số điện thoại sai định dạng

**Q: Làm sao xuất chỉ một số liên hệ?**
A: 
- Vào trang "Quản lý liên hệ"
- Sử dụng tìm kiếm hoặc lọc theo nhóm/tag
- Nhấn "Xuất CSV" → chỉ liên hệ đang hiển thị được xuất

**Q: File CSV xuất ra lưu ở đâu?**
A: Mặc định trong thư mục `data/exports/` của ứng dụng
