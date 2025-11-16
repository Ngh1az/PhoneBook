-- =====================================================
-- PHONEBOOK DATABASE SETUP SCRIPT
-- Tạo database và tables cho PhoneBook Application
-- =====================================================

-- 1. Tạo database
CREATE DATABASE IF NOT EXISTS phonebook_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Sử dụng database
USE phonebook_db;

-- 2. Tạo user cho ứng dụng (tùy chọn - để bảo mật)
-- Nếu bạn muốn dùng root thì bỏ qua bước này
CREATE USER IF NOT EXISTS 'phonebook_user'@'localhost' IDENTIFIED BY 'phonebook123';
GRANT ALL PRIVILEGES ON phonebook_db.* TO 'phonebook_user'@'localhost';
FLUSH PRIVILEGES;

-- 3. Tạo bảng users
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Tạo bảng groups
CREATE TABLE IF NOT EXISTS `groups` (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    group_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_group (user_id, group_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Tạo bảng tags
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tag_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_tag (user_id, tag_name),
    INDEX idx_user_tag (user_id, tag_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Tạo bảng contacts
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    group_id INT,
    notes TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES `groups`(group_id) ON DELETE SET NULL,
    INDEX idx_user_contact (user_id, is_deleted),
    INDEX idx_phone (phone),
    INDEX idx_name (first_name, last_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Tạo bảng contact_tags (many-to-many relationship)
CREATE TABLE IF NOT EXISTS contact_tags (
    contact_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (contact_id, tag_id),
    FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Tạo user admin mặc định (password: 123456)
-- Password đã được hash bằng bcrypt
INSERT IGNORE INTO users (username, password, fullname, email) 
VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqDqvqhfJ2',
    'Administrator',
    'admin@phonebook.com'
);

-- =====================================================
-- HOÀN TẤT CÀI ĐẶT!
-- =====================================================

-- Kiểm tra kết quả:
SELECT 'Database setup completed successfully!' AS Status;

-- Hiển thị thông tin đăng nhập:
SELECT 
    'admin' AS Username,
    '123456' AS Password,
    'Đổi mật khẩu sau khi đăng nhập!' AS Note;

-- Kiểm tra các bảng đã tạo:
SHOW TABLES;

-- =====================================================
-- GHI CHÚ:
-- - Mật khẩu mặc định: 123456 (đã được mã hóa bcrypt)
-- - Nên đổi mật khẩu ngay sau khi đăng nhập lần đầu
-- - Database hỗ trợ UTF-8 (tiếng Việt có dấu)
-- - Soft delete được kích hoạt cho contacts (is_deleted)
-- =====================================================
