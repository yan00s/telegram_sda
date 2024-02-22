from aiogram import types

async def help_msg(message: types.Message):
    """
    Sends a help message to the user.

    Args:
        message (types.Message): The message object.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    text = (
        'List of commands:\n'
        # '/set_new_account - sets up 2FA on a new account\n'
        '/add_subacc - add a sub-Telegram account with access to your accounts\n'
        '/delete_subacc - delete a sub-Telegram account\n'
        '/list_subacc - list sub-Telegram accounts'
    )
    await bot.send_message(peerid, text, reply_markup=types.ReplyKeyboardRemove())
