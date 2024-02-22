from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from pyzbar.pyzbar import decode
import cv2 as cv
import os
from random import choice

from ..steam import get_userses
from .cancel_button import get_cancel_inline
from .state import States


def decode_qr(photo_path: str) -> tuple[bool, str]:
    img = cv.imread(photo_path)
    objs = decode(img)
    os.remove(photo_path)
    if objs:
        dataqr = objs[0].data.decode('utf-8')
        return True, dataqr
    return False, "Can't find QR code"


def generate_namefile() -> str:
    symb = "12345678900qwertyuiopasdfghjklzxcvbnm"
    name = "".join(choice(symb) for _ in range(7))
    return f"./{name}.jpg"


async def save_photo(fileID: str) -> tuple[bool, str]:
    from ..bot_main import bot
    try:
        file = await bot.get_file(fileID)
        file_path = file.file_path
        name_file = generate_namefile()
        await bot.download_file(file_path, name_file)
        return True, name_file
    except Exception as e:
        return False, str(e)


async def handle_approve_qr(call: types.CallbackQuery) -> None:
    peerid = call.from_user.id
    text = "Send me a photo with the Steam QR code."
    await States.approve_qr.set()
    States.approve_qr_data[peerid] = call.data.split('=')[1].replace("select_", "")
    await call.message.reply(text, reply_markup=get_cancel_inline())


async def handle_qr_photo(message: types.Message, state: FSMContext) -> None:
    from ..bot_main import bot
    peerid = message.from_user.id
    mafile_name = States.approve_qr_data.get(peerid, "")

    if message.content_type != "photo":
        text = "You need to send a photo to log in to the account."
        await bot.send_message(peerid, text, reply_markup=get_cancel_inline())
        return

    fileID = message.photo[-1].file_id
    success, file_path = await save_photo(fileID)
    if success:
        success_find_qr, url = decode_qr(file_path)
        if success_find_qr:
            user, _, text = await get_userses(peerid, mafile_name, False)
            if user:
                text = user.approve_qr(url)
    await bot.send_message(peerid, text)
    await state.finish()
