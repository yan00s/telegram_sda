from aiogram import types
from ..database_operations import find_accounts

async def other_msg(message: types.Message):
    """
    Handles messages other than the specified commands.

    Args:
        message (types.Message): The message object.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    textmsg = message.text.strip().lower()
    text, markup = find_accounts(textmsg)
    await bot.send_message(peerid, text, reply_markup=markup)
