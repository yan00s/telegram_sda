from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types


async def cancel_action(call: types.CallbackQuery, state: FSMContext):
    from ..bot_main import bot
    peerid = call.from_user.id
    current_state = await state.get_state()
    await state.finish()
    await call.message.delete()
    if current_state is None:
        return
    return await bot.send_message(peerid, 'Action canceled')

def get_cancel_inline() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn0 = dict(types.InlineKeyboardButton(text='Cancel action', callback_data=f'back'))
    keyboard.add(btn0)
    return keyboard