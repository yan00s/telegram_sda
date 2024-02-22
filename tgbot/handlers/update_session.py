from aiogram import types
from ..steam import get_userses


async def update_session(call: types.CallbackQuery):
    """
    Update the session for a selected account.
    """
    from ..bot_main import bot
    peerid = call.from_user.id
    mafile_name = call.data.split('update_session_')[-1]
    _, _, text = await get_userses(peerid, mafile_name, True)
    
    if text == "Input password:":
        return
    
    await bot.send_message(peerid, text)
