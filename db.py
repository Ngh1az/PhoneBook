"""
Database connection module for PhoneBook Application
Handles SQLite database connections and operations (Portable - No installation needed!)
"""

import sqlite3
import os
from config import DB_PATH, BACKUP_FOLDER, EXPORT_FOLDER, LOG_FILE
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
            # Create data directory if not exists
            db_dir = os.path.dirname(DB_PATH)
            os.makedirs(db_dir, exist_ok=True)

            # Create other required directories
            os.makedirs(BACKUP_FOLDER, exist_ok=True)
            os.makedirs(EXPORT_FOLDER, exist_ok=True)
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

            if self._connection is None:
                self._connection = sqlite3.connect(DB_PATH, check_same_thread=False)
                self._connection.row_factory = (
                    sqlite3.Row
                )  # Enable dictionary-like access
                # Enable foreign keys
                self._connection.execute("PRAGMA foreign_keys = ON")
                print(f"✓ Kết nối database thành công: {DB_PATH}")
                return self._connection
            return self._connection
        except sqlite3.Error as e:
            error_msg = f"Lỗi kết nối database: {e}"
            log_error(error_msg)
            print(f"✗ {error_msg}")
            return None

    def get_connection(self):
        """Get current database connection"""
        if self._connection is None:
            return self.connect()
        return self._connection

    def close(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            print("✓ Đã đóng kết nối database")

    def execute_query(self, query, params=None, fetch=False, max_retries=3):
        """
        Execute a SQL query with automatic retry for database lock errors

        Args:
            query (str): SQL query to execute
            params (tuple): Parameters for the query
            fetch (bool): Whether to fetch results
            max_retries (int): Maximum number of retry attempts for database lock

        Returns:
            Results if fetch=True, dict with affected_rows and last_id if fetch=False
        """
        retry_count = 0

        while retry_count <= max_retries:
            try:
                connection = self.get_connection()
                if connection is None:
                    return None

                cursor = connection.cursor()
                cursor.execute(query, params or ())

                if fetch:
                    # Convert Row objects to dictionaries
                    rows = cursor.fetchall()
                    results = [dict(row) for row in rows]
                    cursor.close()
                    return results
                else:
                    connection.commit()
                    affected_rows = cursor.rowcount
                    last_id = cursor.lastrowid
                    cursor.close()
                    return {"affected_rows": affected_rows, "last_id": last_id}

            except sqlite3.OperationalError as e:
                # Check if it's a database locked error
                if "database is locked" in str(e) and retry_count < max_retries:
                    retry_count += 1
                    wait_time = 0.1 * retry_count  # Exponential backoff
                    print(
                        f"⚠️ Database locked, retry {retry_count}/{max_retries} sau {wait_time}s..."
                    )
                    time.sleep(wait_time)
                    continue  # Retry the query
                else:
                    error_msg = f"Lỗi thực thi query: {e}\nQuery: {query}"
                    log_error(error_msg)
                    print(f"✗ {error_msg}")
                    return None

            except sqlite3.Error as e:
                error_msg = f"Lỗi thực thi query: {e}\nQuery: {query}"
                log_error(error_msg)
                print(f"✗ {error_msg}")
                return None

        return None

    def execute_many(self, query, data, max_retries=3):
        """
        Execute a query with multiple rows of data with automatic retry for database lock

        Args:
            query (str): SQL query to execute
            data (list): List of tuples containing data
            max_retries (int): Maximum number of retry attempts for database lock

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

            except sqlite3.OperationalError as e:
                # Check if it's a database locked error
                if "database is locked" in str(e) and retry_count < max_retries:
                    retry_count += 1
                    wait_time = 0.1 * retry_count
                    print(
                        f"⚠️ Database locked trong executemany, retry {retry_count}/{max_retries} sau {wait_time}s..."
                    )
                    time.sleep(wait_time)
                    continue  # Retry the query
                else:
                    error_msg = f"Lỗi thực thi executemany: {e}"
                    log_error(error_msg)
                    print(f"✗ {error_msg}")
                    return 0

            except sqlite3.Error as e:
                error_msg = f"Lỗi thực thi executemany: {e}"
                log_error(error_msg)
                print(f"✗ {error_msg}")
                return 0

        return 0

    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            connection = self.connect()
            if connection is None:
                return False

            cursor = connection.cursor()

            # Enable foreign keys
            cursor.execute("PRAGMA foreign_keys = ON")

            # Create tables
            tables = self._get_table_schemas()

            for table_name, table_schema in tables.items():
                try:
                    cursor.execute(table_schema)
                    print(f"✓ Bảng {table_name} đã sẵn sàng")
                except sqlite3.Error as tbl_err:
                    if "already exists" in str(tbl_err):
                        print(f"✓ Bảng {table_name} đã tồn tại")
                    else:
                        raise

            connection.commit()
            cursor.close()
            print("✓ Khởi tạo database hoàn tất!")
            return True

        except sqlite3.Error as e:
            error_msg = f"Lỗi khởi tạo database: {e}"
            log_error(error_msg)
            print(f"✗ {error_msg}")
            return False

    def _get_table_schemas(self):
        """Get all table creation schemas for SQLite"""
        return {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    fullname TEXT NOT NULL,
                    phone TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "my_groups": """
                CREATE TABLE IF NOT EXISTS my_groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    group_name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE(user_id, group_name)
                )
            """,
            "contacts": """
                CREATE TABLE IF NOT EXISTS contacts (
                    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    address TEXT,
                    notes TEXT,
                    group_id INTEGER,
                    is_deleted INTEGER DEFAULT 0,
                    deleted_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (group_id) REFERENCES my_groups(group_id) ON DELETE SET NULL
                )
            """,
            "tags": """
                CREATE TABLE IF NOT EXISTS tags (
                    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    tag_name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE(user_id, tag_name)
                )
            """,
            "contact_tags": """
                CREATE TABLE IF NOT EXISTS contact_tags (
                    contact_id INTEGER NOT NULL,
                    tag_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (contact_id, tag_id),
                    FOREIGN KEY (contact_id) REFERENCES contacts(contact_id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
                )
            """,
        }


# Create singleton instance
db = Database()
