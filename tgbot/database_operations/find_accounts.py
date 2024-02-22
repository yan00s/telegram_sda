from typing import Tuple
from .database_connector import execute_query
from aiogram import types

def find_accounts(text: str) -> Tuple[str, types.InlineKeyboardMarkup]:
    """
    Find accounts by text.

    Args:
        text (str): The text to search for in account names.

    Returns:
        tuple: A tuple containing the response text and the keyboard.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    query = "SELECT account_name, steamid FROM manifest WHERE account_name LIKE ?"
    results = execute_query(query, [text + '%'])

    if not results:
        response_text = 'There are no such accounts. Enter the first letters of a steam login. Available commands: /help'
        return response_text, keyboard

    response_text = 'Results:'
    buttons = [
        types.InlineKeyboardButton(text=acc_name, callback_data=f"select_{acc_name}:{steamid}")
        for index, (acc_name, steamid) in enumerate(results, start=1)
    ]

    for i in range(0, len(buttons), 3):
        keyboard.row(*buttons[i:i+3])

    return response_text, keyboard