"""
Database connection module for PhoneBook Application
Handles MySQL database connections and operations
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from utils.logger import log_error
import time


class Database:
    """Database connection class using Singleton pattern"""

    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """Establish database connection"""
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**DB_CONFIG)
                print(" Kết nối database thành công!")
                return self._connection
            return self._connection
        except Error as e:
            error_msg = f"Lỗi kết nối database: {e}"
            log_error(error_msg)
            print(f" {error_msg}")
            return None

    def get_connection(self):
        """Get current database connection"""
        if self._connection is None or not self._connection.is_connected():
            return self.connect()
        return self._connection

    def close(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print(" Đã đóng kết nối database")

    def execute_query(self, query, params=None, fetch=False, max_retries=3):
        """
        Execute a SQL query with automatic retry for deadlock errors

        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            fetch (bool): Whether to fetch results
            max_retries (int): Maximum number of retry attempts for deadlock

        Returns:
            Results if fetch=True, affected rows count if fetch=False
        """
        retry_count = 0

        while retry_count <= max_retries:
            try:
                connection = self.get_connection()
                if connection is None:
                    return None

                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())

                if fetch:
                    results = cursor.fetchall()
                    cursor.close()
                    return results
                else:
                    connection.commit()
                    affected_rows = cursor.rowcount
                    last_id = cursor.lastrowid
                    cursor.close()
                    return {"affected_rows": affected_rows, "last_id": last_id}

            except Error as e:
                # Check if it's a deadlock error (1213)
                if e.errno == 1213 and retry_count < max_retries:
                    retry_count += 1
                    wait_time = (
                        0.1 * retry_count
                    )  # Exponential backoff: 0.1s, 0.2s, 0.3s
                    print(
                        f" ⚠️ Deadlock detected, retry {retry_count}/{max_retries} sau {wait_time}s..."
                    )
                    time.sleep(wait_time)

                    # Rollback transaction before retry
                    try:
                        if connection:
                            connection.rollback()
                    except Error:
                        pass

                    continue  # Retry the query
                else:
                    # Log error and return None for other errors or max retries exceeded
                    error_msg = f"Lỗi thực thi query: {e}\nQuery: {query}"
                    if e.errno == 1213:
                        error_msg += f"\nĐã thử {max_retries} lần nhưng vẫn bị deadlock"
                    log_error(error_msg)
                    print(f" {error_msg}")

                    # Rollback transaction
                    try:
                        if connection:
                            connection.rollback()
                    except Error:
                        pass

                    return None

        return None

    def execute_many(self, query, data, max_retries=3):
        """
        Execute a query with multiple rows of data with automatic retry for deadlock

        Args:
            query (str): SQL query to execute
            data (list): List of tuples containing data
            max_retries (int): Maximum number of retry attempts for deadlock

        Returns:
            Number of affected rows
        """
        retry_count = 0

        while retry_count <= max_retries:
            try:
                connection = self.get_connection()
                if connection is None:
                    return 0

                cursor = connection.cursor()
                cursor.executemany(query, data)
                connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows

            except Error as e:
                # Check if it's a deadlock error (1213)
                if e.errno == 1213 and retry_count < max_retries:
                    retry_count += 1
                    wait_time = 0.1 * retry_count
                    print(
                        f" ⚠️ Deadlock detected trong executemany, retry {retry_count}/{max_retries} sau {wait_time}s..."
                    )
                    time.sleep(wait_time)

                    # Rollback transaction before retry
                    try:
                        if connection:
                            connection.rollback()
                    except Error:
                        pass

                    continue  # Retry the query
                else:
                    # Log error for other errors or max retries exceeded
                    error_msg = f"Lỗi thực thi executemany: {e}"
                    if e.errno == 1213:
                        error_msg += f"\nĐã thử {max_retries} lần nhưng vẫn bị deadlock"
                    log_error(error_msg)
                    print(f" {error_msg}")

                    # Rollback transaction
                    try:
                        if connection:
                            connection.rollback()
                    except Error:
                        pass

                    return 0

        return 0

    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            # First connect without specifying database
            temp_config = DB_CONFIG.copy()
            db_name = temp_config.pop("database")

            connection = mysql.connector.connect(**temp_config)
            cursor = connection.cursor()

            # Create database if not exists (ignore if exists)
            try:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            except Error as db_err:
                # Ignore database exists error
                if db_err.errno != 1007:  # 1007 = database exists
                    raise

            cursor.execute(f"USE {db_name}")

            # Create tables
            tables = self._get_table_schemas()

            for table_name, table_schema in tables.items():
                try:
                    cursor.execute(table_schema)
                    print(f" Bảng {table_name} đã sẵn sàng")
                except Error as tbl_err:
                    # Ignore table exists error
                    if tbl_err.errno == 1050:  # 1050 = table exists
                        print(f" Bảng {table_name} đã tồn tại")
                    else:
                        raise

            connection.commit()
            cursor.close()
            connection.close()

            # Now connect with database
            self.connect()
            print(" Khởi tạo database hoàn tất!")
            return True

        except Error as e:
            error_msg = f"Lỗi khởi tạo database: {e}"
            log_error(error_msg)
            print(f" {error_msg}")
            return False

    def _get_table_schemas(self):
        """Get all table creation schemas"""
        return {
            "users": """CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) UNIQUE NOT NULL,email VARCHAR(100) UNIQUE NOT NULL,password_hash VARCHAR(255) NOT NULL,fullname VARCHAR(100) NOT NULL,phone VARCHAR(20),address TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,INDEX idx_username (username),INDEX idx_email (email)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            "my_groups": """CREATE TABLE IF NOT EXISTS my_groups (group_id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,group_name VARCHAR(50) NOT NULL,description TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,UNIQUE KEY unique_group_per_user (user_id, group_name),INDEX idx_user_id (user_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            "contacts": """CREATE TABLE IF NOT EXISTS contacts (contact_id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,first_name VARCHAR(50) NOT NULL,last_name VARCHAR(50) NOT NULL,phone VARCHAR(20) NOT NULL,email VARCHAR(100),address TEXT,notes TEXT,group_id INT,is_deleted BOOLEAN DEFAULT FALSE,deleted_at TIMESTAMP NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,INDEX idx_user_id (user_id),INDEX idx_is_deleted (is_deleted),INDEX idx_fullname (first_name, last_name)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            "tags": """CREATE TABLE IF NOT EXISTS tags (tag_id INT AUTO_INCREMENT PRIMARY KEY,user_id INT NOT NULL,tag_name VARCHAR(50) NOT NULL,description TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,UNIQUE KEY unique_tag_per_user (user_id, tag_name),INDEX idx_user_id (user_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
            "contact_tags": """CREATE TABLE IF NOT EXISTS contact_tags (contact_id INT NOT NULL,tag_id INT NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (contact_id, tag_id),FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE,FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,INDEX idx_contact_id (contact_id),INDEX idx_tag_id (tag_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
        }


db = Database()
