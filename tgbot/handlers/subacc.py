from ..database_operations import ( get_listsub,
  add_dbsub,
  dell_dbsub,
)

from .cancel_button import get_cancel_inline
from .state import States

from aiogram.dispatcher import FSMContext
from aiogram import types
import re

    
async def dell_subaccfinal(message: types.Message, state: FSMContext) -> None:
    """
    Deletes a subaccount from the database.

    Args:
        message (types.Message): User message object.
        state (FSMContext): Finite state machine context.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    msg_text = message.text
    result = re.findall(r"^\d{9}", msg_text)
    if len(result) == 0:
        text = "not indexed"
        return await bot.send_message(peerid, text)
    peeridsub = result[0]
    text = "Deleted from base successfully"
    dell_dbsub(peeridsub)
    await state.finish()
    return await bot.send_message(peerid, text)


async def add_subaccfinal(message: types.Message, state: FSMContext) -> None:
    """
    Adds a subaccount to the database.

    Args:
        message (types.Message): User message object.
        state (FSMContext): Finite state machine context.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    msg_text = message.text
    result = re.findall(r"^\d{8,11} \d", msg_text)
    if len(result) == 0:
        text = "not indexed"
        return await bot.send_message(peerid, text)
    peeridsub, acccode = result[0].split(" ")
    await state.finish()
    text = "Added to base successfully"
    add_dbsub(peeridsub, acccode)
    return await bot.send_message(peerid, text)


async def add_subaccfirst(message: types.Message) -> None:
    """
    Starts the process of adding a new subaccount.

    Args:
        message (types.Message): User message object.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    text = 'Enter the peerid acc with code access, for example:\n'\
            '345000101 2\n'\
            'peerid is 345000101\n' \
            'code:\n0 = No access\n1 = Access 2fa codes + QR login\n2 = Access codes+trades\n'\
            'you can get peerid from this bot @ShowJsonBot\n'
    await States.add_subacc.set()
    await bot.send_message(peerid, text, reply_markup=get_cancel_inline())


async def dell_subaccfirst(message: types.Message) -> None:
    """
    Starts the process of deleting a subaccount.

    Args:
        message (types.Message): User message object.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    text = 'Enter the peerid for delete, example:'\
            '345000101'
    await States.dell_subacc.set()
    await bot.send_message(peerid, text, reply_markup=get_cancel_inline())


async def list_subacc(message: types.Message) -> None:
    """
    Displays a list of subaccounts.

    Args:
        message (types.Message): User message object.
    """
    from ..bot_main import bot
    peerid = message.from_user.id
    text = "None sub accounts"
    result = get_listsub()
    if len(result) > 0:
        text_raw = []
        for res in result:
            res = f"peerid: {res} code: {result[res]}"
            text_raw.append(res)
        text = "\n".join(text_raw)
    await bot.send_message(peerid, text)
