from aiogram import types

async def start_msg(message: types.Message):
    """
    Sends a welcome message to users when they start interacting with the bot.

    Args:
        message (types.Message): The message object.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    text = 'Hello, enter the first letters of steam login'
    await bot.send_message(peerid, text, reply_markup=types.ReplyKeyboardRemove())
