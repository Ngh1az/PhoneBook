-- ====================================================
-- PhoneBook Application - Database Schema
-- MySQL 8.0+
-- ====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS phonebook_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE phonebook_db;

-- ====================================================
-- Table: users
-- Description: Stores user account information
-- ====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- Table: groups
-- Description: Stores contact groups for each user
-- ====================================================
CREATE TABLE IF NOT EXISTS groups (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    group_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_group_per_user (user_id, group_name),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- Table: contacts
-- Description: Stores contact information
-- Supports soft delete (is_deleted flag)
-- ====================================================
CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    notes TEXT,
    group_id INT,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_fullname (first_name, last_name),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- Table: tags
-- Description: Stores tags for categorizing contacts
-- ====================================================
CREATE TABLE IF NOT EXISTS tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tag_name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_tag_per_user (user_id, tag_name),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- Table: contact_tags
-- Description: Many-to-many relationship between contacts and tags
-- ====================================================
CREATE TABLE IF NOT EXISTS contact_tags (
    contact_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (contact_id, tag_id),
    FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,
    INDEX idx_contact_id (contact_id),
    INDEX idx_tag_id (tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ====================================================
-- Sample Data (Optional - for testing)
-- ====================================================

-- Insert sample user (password: 123456)
-- Password hash for '123456' using bcrypt
INSERT IGNORE INTO users (username, email, password_hash, fullname, phone, address) 
VALUES (
    'admin',
    'admin@phonebook.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuQq3jZ9Oy',
    'Administrator',
    '0123456789',
    'Hanoi, Vietnam'
);

-- Get the user_id for sample data
SET @user_id = (SELECT user_id FROM users WHERE username = 'admin' LIMIT 1);

-- Insert sample groups
INSERT IGNORE INTO groups (user_id, group_name, description) VALUES
(@user_id, 'Gia đình', 'Các thành viên trong gia đình'),
(@user_id, 'Bạn bè', 'Bạn bè thân thiết'),
(@user_id, 'Công việc', 'Đồng nghiệp và đối tác');

-- Insert sample tags
INSERT IGNORE INTO tags (user_id, tag_name, description) VALUES
(@user_id, 'Quan trọng', 'Người liên hệ quan trọng'),
(@user_id, 'VIP', 'Khách hàng VIP'),
(@user_id, 'Khẩn cấp', 'Liên hệ khẩn cấp');

-- ====================================================
-- Views for easy querying (Optional)
-- ====================================================

-- View: Active contacts with group information
CREATE OR REPLACE VIEW v_active_contacts AS
SELECT 
    c.*,
    g.group_name,
    u.username as owner_username,
    CONCAT(c.first_name, ' ', c.last_name) as full_name
FROM contacts c
LEFT JOIN groups g ON c.group_id = g.group_id
LEFT JOIN users u ON c.user_id = u.user_id
WHERE c.is_deleted = FALSE;

-- View: Deleted contacts (trash)
CREATE OR REPLACE VIEW v_trash_contacts AS
SELECT 
    c.*,
    g.group_name,
    u.username as owner_username,
    CONCAT(c.first_name, ' ', c.last_name) as full_name
FROM contacts c
LEFT JOIN groups g ON c.group_id = g.group_id
LEFT JOIN users u ON c.user_id = u.user_id
WHERE c.is_deleted = TRUE;

-- View: Contact statistics per user
CREATE OR REPLACE VIEW v_user_stats AS
SELECT 
    u.user_id,
    u.username,
    u.fullname,
    COUNT(DISTINCT c.contact_id) as total_contacts,
    COUNT(DISTINCT CASE WHEN c.is_deleted = FALSE THEN c.contact_id END) as active_contacts,
    COUNT(DISTINCT CASE WHEN c.is_deleted = TRUE THEN c.contact_id END) as deleted_contacts,
    COUNT(DISTINCT g.group_id) as total_groups,
    COUNT(DISTINCT t.tag_id) as total_tags
FROM users u
LEFT JOIN contacts c ON u.user_id = c.user_id
LEFT JOIN groups g ON u.user_id = g.user_id
LEFT JOIN tags t ON u.user_id = t.user_id
GROUP BY u.user_id;

-- ====================================================
-- Stored Procedures (Optional)
-- ====================================================

-- Procedure: Permanently delete old trash items (older than 30 days)
DELIMITER //
CREATE PROCEDURE sp_cleanup_old_trash()
BEGIN
    DELETE FROM contacts 
    WHERE is_deleted = TRUE 
    AND deleted_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
    
    SELECT ROW_COUNT() as deleted_count;
END //
DELIMITER ;

-- Procedure: Get contact with all tags
DELIMITER //
CREATE PROCEDURE sp_get_contact_details(IN p_contact_id INT)
BEGIN
    -- Get contact info
    SELECT 
        c.*,
        g.group_name,
        GROUP_CONCAT(t.tag_name SEPARATOR ', ') as tags
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.group_id
    LEFT JOIN contact_tags ct ON c.contact_id = ct.contact_id
    LEFT JOIN tags t ON ct.tag_id = t.tag_id
    WHERE c.contact_id = p_contact_id
    GROUP BY c.contact_id;
END //
DELIMITER ;

-- ====================================================
-- Triggers (Optional)
-- ====================================================

-- Trigger: Auto-update deleted_at when is_deleted changes
DELIMITER //
CREATE TRIGGER trg_contact_soft_delete
BEFORE UPDATE ON contacts
FOR EACH ROW
BEGIN
    IF NEW.is_deleted = TRUE AND OLD.is_deleted = FALSE THEN
        SET NEW.deleted_at = NOW();
    ELSEIF NEW.is_deleted = FALSE AND OLD.is_deleted = TRUE THEN
        SET NEW.deleted_at = NULL;
    END IF;
END //
DELIMITER ;

-- ====================================================
-- Database Information
-- ====================================================
SELECT 'Database schema created successfully!' as message;
SELECT VERSION() as mysql_version;
SELECT DATABASE() as current_database;

-- Show all tables
SHOW TABLES;
