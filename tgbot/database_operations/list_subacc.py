from typing import Dict
from .database_connector import execute_query


def get_listsub() -> Dict[int, int]:
    """
    Get the list of subaccounts.

    Returns:
        dict: A dictionary containing peerid as keys and access as values.
    """
    query = "SELECT peerid, access FROM subaccs"
    result_raw = execute_query(query)
    result = {res[0]: res[1] for res in result_raw}
    return result