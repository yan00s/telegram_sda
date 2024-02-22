from .list_subacc import get_listsub
from aiogram import types
from os import environ


def whitelist_data(code: int) -> list:
    """Return a list of allowed commands based on the code."""
    if code == 1:
        return ["select_", "get2fa_", "approveqr="]
    elif code == 2:
        return ["select_", "get2fa_", "update_session_", "get_last_five_trade_", "confirm_all_trades_", "approveqr="]
    return []


def check_data(code: int, data: str) -> bool:
    """Check if the provided data is allowed based on the code."""
    whitelist = whitelist_data(code)
    return any(command in data for command in whitelist)


def is_allow_command(code: int, text: str, data: str) -> bool:
    """Check if the command is allowed based on the code, text, and data."""
    if code in [1, 2]:
        if text == "/start":
            return True
        if "/" in text:
            return False
        if text:
            return True
        return check_data(code, data)
    return False


def check_access(fn):
    async def wrapped(message: types.Message):
        user_id = message.from_user.id
        subaccounts = get_listsub()
        if user_id in subaccounts:
            if hasattr(message, "text"):
                text = message.text
                data = ""
            elif hasattr(message, "data"):
                data = message.data
                text = ""
            code = subaccounts[user_id]
            if not is_allow_command(code, text, data):
                return
        elif user_id != int(environ.get('ADMIN_PEERID')):
            return
        return await fn(message)
    return wrapped