import logging
from aiogram import types
from steampy.guard import generate_one_time_code
import json
import os

async def get_two_factor_authentication(call: types.CallbackQuery):
    """
    Retrieves the two-factor authentication code for a Steam account.

    Args:
        call (types.CallbackQuery): The callback query.
        bot: The bot instance.
    """
    from ..bot_main import bot
    peerid = call.from_user.id
    mafile_name = call.data.split('get2fa_')[-1]
    
    # Construct the path to the .mafile
    mafile_path = os.path.join('./data/', mafile_name)
    
    try:
        with open(mafile_path, 'r') as f:
            mafile = json.load(f)
    except FileNotFoundError:
        logging.warning(f"File '{mafile_name}' not found")
        return await bot.send_message(peerid, 'File not found')

    shared_secret = mafile.get('shared_secret')
    if not shared_secret:
        text = 'Key error getting 2FA'
        logging.warning(f'{text} {mafile_name}')
    else:
        text = generate_one_time_code(shared_secret)
    
    return await bot.send_message(peerid, text)
