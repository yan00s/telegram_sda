from aiogram.dispatcher import FSMContext
from aiogram import types

from ..steam import get_userses
from .state import States


async def inputpassw(message: types.Message, state: FSMContext):
    """
    Handle the input of the password during login.
    """
    from ..bot_main import bot

    # Initialize error message
    text = "An error occurred in inputpassw..."
    
    # Get the password from the message
    msg_text = message.text
    
    # Get the mafile name from the user's state
    mafile_name = States.waitpassw_data.get(message.from_user.id, "")
    
    # Get the user's ID
    peerid = message.from_user.id

    # Finish the state
    await state.finish()
    
    # Send a message indicating that the bot is trying to login
    await bot.send_message(peerid, 'Trying to login...')

    # Try to login with the provided password
    _, _, text = await get_userses(peerid, mafile_name, True, password=msg_text)
    
    # Send the result message
    await bot.send_message(peerid, text)
