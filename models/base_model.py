"""
Base Model class for PhoneBook Application
Provides common database operations for all models
"""

from db import db


def mysql_to_sqlite(query):
    """Convert MySQL query syntax to SQLite syntax"""
    query = query.replace("?", "?")
    query = query.replace("INSERT OR IGNORE", "INSERT OR IGNORE")
    query = query.replace("", "")
    return query


class BaseModel:
    """Base model class with common CRUD operations"""

    table_name = None  # To be defined in child classes

    @classmethod
    def find_by_id(cls, id_field, id_value):
        """
        Find a record by ID

        Args:
            id_field (str): Name of the ID field
            id_value: Value of the ID

        Returns:
            dict: Record data or None
        """
        query = mysql_to_sqlite(f"SELECT * FROM {cls.table_name} WHERE {id_field} = ?")
        results = db.execute_query(query, (id_value,), fetch=True)

        if results and len(results) > 0:
            return results[0]
        return None

    @classmethod
    def find_all(cls, conditions=None):
        """
        Find all records with optional conditions

        Args:
            conditions (dict): Optional WHERE conditions

        Returns:
            list: List of records
        """
        query = f"SELECT * FROM {cls.table_name}"
        params = ()

        if conditions:
            where_clauses = []
            params_list = []

            for key, value in conditions.items():
                where_clauses.append(f"{key} = ?")
                params_list.append(value)

            query += " WHERE " + " AND ".join(where_clauses)
            params = tuple(params_list)

        return db.execute_query(query, params, fetch=True) or []

    @classmethod
    def create(cls, data):
        """
        Create a new record

        Args:
            data (dict): Record data

        Returns:
            int: ID of created record or None
        """
        fields = list(data.keys())
        placeholders = ", ".join(["?"] * len(fields))
        fields_str = ", ".join(fields)

        query = f"INSERT INTO {cls.table_name} ({fields_str}) VALUES ({placeholders})"
        values = tuple(data.values())

        result = db.execute_query(query, values)

        if result:
            return result["last_id"]
        return None

    @classmethod
    def update(cls, id_field, id_value, data):
        """
        Update a record

        Args:
            id_field (str): Name of the ID field
            id_value: Value of the ID
            data (dict): Data to update

        Returns:
            bool: True if successful, False otherwise
        """
        set_clauses = []
        values = []

        for key, value in data.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)

        values.append(id_value)

        query = (
            f"UPDATE {cls.table_name} SET {', '.join(set_clauses)} WHERE {id_field} = ?"
        )

        result = db.execute_query(query, tuple(values))

        return result is not None and result["affected_rows"] > 0

    @classmethod
    def delete(cls, id_field, id_value):
        """
        Delete a record

        Args:
            id_field (str): Name of the ID field
            id_value: Value of the ID

        Returns:
            bool: True if successful, False otherwise
        """
        query = f"DELETE FROM {cls.table_name} WHERE {id_field} = ?"
        result = db.execute_query(query, (id_value,))

        return result is not None and result["affected_rows"] > 0

    @classmethod
    def count(cls, conditions=None):
        """
        Count records with optional conditions

        Args:
            conditions (dict): Optional WHERE conditions

        Returns:
            int: Number of records
        """
        query = f"SELECT COUNT(*) as count FROM {cls.table_name}"
        params = ()

        if conditions:
            where_clauses = []
            params_list = []

            for key, value in conditions.items():
                where_clauses.append(f"{key} = ?")
                params_list.append(value)

            query += " WHERE " + " AND ".join(where_clauses)
            params = tuple(params_list)

        results = db.execute_query(query, params, fetch=True)

        if results and len(results) > 0:
            return results[0]["count"]
        return 0
