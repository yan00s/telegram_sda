from .database_connector import execute_query
import time

def update_cookies(cookies: str, username: str) -> bool:
    """
    Update cookies for a given username.

    Args:
        cookies (str): The new cookies value.
        username (str): The username to update.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    result = execute_query('UPDATE manifest SET cookies = ? WHERE account_name = ?', [cookies, username])
    return bool(result)

def update_refresh_token(token: str, username: str) -> bool:
    """
    Update refresh token for a given username.

    Args:
        token (str): The new refresh token.
        username (str): The username to update.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    result = execute_query('UPDATE manifest SET refresh_token = ? WHERE account_name = ?', [token, username])
    return bool(result)

def update_check_alive(aliveto: int, username: str) -> bool:
    """
    Update the check alive time for a given username.

    Args:
        aliveto (int): The new alive time.
        username (str): The username to update.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    result = execute_query('UPDATE manifest SET aliveto = ? WHERE account_name = ?', [aliveto, username])
    return bool(result)

def get_cookies(username: str) -> str:
    """
    Get cookies for a given username.

    Args:
        username (str): The username to retrieve cookies for.

    Returns:
        str: The cookies value.
    """
    result = execute_query('SELECT cookies FROM manifest WHERE account_name = ?', [username])
    return result[0][0] if result else ''

def get_refresh_token(username: str) -> str:
    """
    Get refresh token for a given username.

    Args:
        username (str): The username to retrieve refresh token for.

    Returns:
        str: The refresh token value.
    """
    result = execute_query('SELECT refresh_token FROM manifest WHERE account_name = ?', [username])
    return result[0][0] if result else ''

def need_check_alive(username: str) -> bool:
    """
    Check if the alive time for a given username has expired.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the alive time has expired, False otherwise.
    """
    deadline = execute_query('SELECT aliveto FROM manifest WHERE account_name = ?', [username])
    return bool(deadline and deadline[0][0] < int(time.time()) - 3600)