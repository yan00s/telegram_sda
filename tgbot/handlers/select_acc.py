from aiogram import types

async def select_account(call: types.CallbackQuery):
    """
    Handles the selection of an account from the callback query.

    Args:
        call (types.CallbackQuery): The callback query object.
    """
    from ..bot_main import bot
    peerid = call.from_user.id
    acc_name, steamid = call.data.split(':')  # Extract account name and SteamID from the callback data
    acc_name = acc_name.replace('select_', '')
    name_file = f"{acc_name}.maFile"

    # Create an InlineKeyboardMarkup for account actions
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(
        types.InlineKeyboardButton(text='Get 2FA code', callback_data=f'get2fa_{name_file}'),
        types.InlineKeyboardButton(text='Login by QR', callback_data=f'approveqr={name_file}'),
        types.InlineKeyboardButton(text='Confirm all trades', callback_data=f'confirm_all_trades_{name_file}'),
        types.InlineKeyboardButton(text='Get 5 last trades for confirm', callback_data=f'get_last_five_trade_{name_file}'),
        types.InlineKeyboardButton(text='Update session', callback_data=f'update_session_{name_file}'),
        # types.InlineKeyboardButton(text='Deactivate 2FA', callback_data='get2fasasdas')
    )

    # Format account information message
    text = f'Account data:\nName: {acc_name}\nSteamID: {steamid}'

    await bot.send_message(peerid, text, reply_markup=keyboard)
