import sqlite3 as sql
from typing import List, Optional, Tuple
from log import LOGGER

def execute_query(query: str, parameters: List = []) -> Optional[List[Tuple]]:
    """
    Execute a query on the database.

    Args:
        query (str): The SQL query to execute.
        parameters (list): Optional parameters for the query.

    Returns:
        list or None: A list of tuples containing the results of the query, or None if an error occurred.
    """
    connection = get_connection()
    try:
        with connection:
            cursor = connection.execute(query, parameters)
            results = cursor.fetchall()
            return results
    except sql.Error as e:
        LOGGER.exception(f"Error executing SQL query")
        return None
    finally:
        connection.close()


def get_connection() -> sql.Connection:
    """
    Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    db_path = './data/data_base.db'
    return sql.connect(db_path)