from aiogram import types
from log import LOGGER
from ..steam import get_userses, five_trades, confirm_all_trades, cancel_trade, accept_trade

async def get_accept_trade(call: types.CallbackQuery):
    """
    Handle accepting a trade.
    """
    peerid = call.from_user.id
    trade_data = call.data.split("accept=")[1].split(";")
    username, cid, ck = trade_data
    
    mafile_name = f"{username}.maFile"
    user, mafile_data, text = await get_userses(peerid, mafile_name, False)
    
    mafile_data["cid"] = cid
    mafile_data["ck"] = ck
    text = accept_trade(user, mafile_data)
    return await call.message.edit_text(text)


async def get_cancel_trade(call: types.CallbackQuery):
    """
    Handle canceling a trade.
    """
    peerid = call.from_user.id
    trade_data = call.data.split("cancel=")[1].split(";")
    username, creator_id = trade_data
    
    mafile_name = f"{username}.maFile"
    user, mdata, _ = await get_userses(peerid, mafile_name, False)
    steamid = mdata.get("steamid", 0)
    text = cancel_trade(user, username, creator_id, steamid)
    
    return await call.message.edit_text(text)


async def about_trade(call: types.CallbackQuery):
    """
    Show details about a trade.
    """
    from ..bot_main import About_trades
    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    trade_data = call.data.split("about_trade_")[1].split(";")
    username, tradenum = trade_data
    trades = About_trades.data.get(username, None)
    
    if trades:
        trade = trades.get(int(tradenum), None)
        text_trade = trade.get("text", "unknown1") if trade else "unknown0"
        
        if "unknown" not in text_trade:
            creator_id = trade.get("creator_id","")
            cid = trade.get("cid","")
            ck = trade.get("ck","")
            
            btn0 = dict(types.InlineKeyboardButton(text="Accept", callback_data=f'accept={username};{cid};{ck}'))
            btn1 = dict(types.InlineKeyboardButton(text="Cancel", callback_data=f'cancel={username};{creator_id}'))
            keyboard.add(btn0)
            keyboard.add(btn1)
        
        await call.message.edit_text(text_trade)
        await call.message.edit_reply_markup(reply_markup=keyboard)


async def confirm_all_trades_all(call: types.CallbackQuery):
    """
    Confirm all trades.
    """
    from ..bot_main import bot
    peerid = call.from_user.id
    mafile_name = call.data.split('confirm_all_trades_')[-1]
    user, mafile_data, text = await get_userses(peerid, mafile_name, False)
    
    if user:
        text = confirm_all_trades(user, **mafile_data)
    
    await bot.send_message(peerid, text)


async def get_five_trades(call: types.CallbackQuery):
    """
    Get the last five trades.
    """
    from ..bot_main import bot
    keyboard = None
    peerid = call.from_user.id
    mafile_name = call.data.split('get_last_five_trade_')[-1]
    user, mafile_data, text = await get_userses(peerid, mafile_name, False)
    if user:
        keyboard = five_trades(user, **mafile_data)
        if keyboard is None:
            text = "Error getting five trades"
        elif len(keyboard["inline_keyboard"]) == 0:
            text = "No trades"
        else:
            text = 'list of trades:'
    await bot.send_message(peerid, text, reply_markup = keyboard)