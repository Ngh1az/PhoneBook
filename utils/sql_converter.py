"""
SQL Query Converter Utility
Converts MySQL-style queries to SQLite-compatible format
"""


def mysql_to_sqlite(query):
    """
    Convert MySQL query syntax to SQLite syntax

    Changes:
    - %s → ?
    - INSERT IGNORE → INSERT OR IGNORE
    - AUTO_INCREMENT → AUTOINCREMENT
    - BOOLEAN → INTEGER
    - ` backticks → removed
    """
    # Replace parameter placeholder
    query = query.replace("%s", "?")

    # Replace INSERT IGNORE
    query = query.replace("INSERT IGNORE", "INSERT OR IGNORE")

    # Replace AUTO_INCREMENT
    query = query.replace("AUTO_INCREMENT", "AUTOINCREMENT")

    # Replace BOOLEAN
    query = query.replace("BOOLEAN", "INTEGER")

    # Remove backticks
    query = query.replace("`", "")

    return query
