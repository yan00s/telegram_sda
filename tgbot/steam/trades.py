from .login import LoginExecutor

from steampy.guard import generate_confirmation_key, generate_device_id
from aiogram import types
from log import LOGGER

import time


def accept_trade(user: LoginExecutor, mafile_data):
    username = mafile_data.get('username')
    steamid = mafile_data.get('steamid')
    cid = mafile_data.get('cid')
    ck = mafile_data.get('ck')
    identity_secret = mafile_data.get('identity_secret')
    try:
        response = user.session.get("https://steamcommunity.com/mobileconf/getlist", params={
            "p": generate_device_id(str(steamid)),
            "a": steamid,
            "k": generate_confirmation_key(identity_secret=identity_secret, tag="conf", timestamp=int(time.time())),
            "t": int(time.time()),
            "m": 'react',
            "tag": "conf"
        })
        respjson = response.json()
        if not respjson.get("success", False):
            text = 'Invalid Steam Guard file'
            LOGGER.error(text)
            return text
        params = {
            "op": "allow",
            "p": generate_device_id(str(steamid)),
            "a": steamid,
            "k": generate_confirmation_key(identity_secret=identity_secret, tag="allow", timestamp=int(time.time())),
            "t": int(time.time()),
            "m": 'react',
            "tag": "allow",
            "cid": cid,
            "ck": ck
        }
        user.session.headers.update({"Connection": "keep-alive"})
        user.session.headers.update({'X-Requested-With': 'com.valvesoftware.android.steam.community'})
        response = user.session.get('https://steamcommunity.com/mobileconf/ajaxop', params=params)
        respjson = response.json()
        success = respjson.get("success", False)
        if success:
            text = "Action confirmation successful!"
        else:
            text = f"Success: {success}"
    except Exception as e:
        text = f"[ACCEPTTRADE] {username} unknown error, check logs"
        LOGGER.exception(text)
    return text


def cancel_trade(user: LoginExecutor, username, creator_id, steamid):
    upd_cook = {
        "Referer": f"https://steamcommunity.com/profiles/{steamid}/tradeoffers",
        "Origin": "https://steamcommunity.com"
    }
    user.session.cookies.update(upd_cook)
    try:
        url = f"https://steamcommunity.com/tradeoffer/{creator_id}/cancel"
        resp = user.session.post(url, data={
            "sessionid": user.session.cookies.get("sessionid")
        })
        respjson = resp.json()
        success = respjson.get("tradeofferid", False)
        if success:
            text = "The trade was successfully canceled!"
        else:
            text = f"Success: {success}"
    except Exception as e:
        text = f"[CANCELTRADE] {username} unknown error, check logs"
        LOGGER.exception(text)
    return text


def five_trades(user: LoginExecutor, **kwargs):
    from ..bot_main import About_trades

    keyboard = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    username = kwargs.get('username')
    steamid = kwargs.get('steamid')
    identity_secret = kwargs.get('identity_secret')
    try:
        confirmations_page = user.session.get("https://steamcommunity.com/mobileconf/getlist", params={
            "p": generate_device_id(str(steamid)),
            "a": steamid,
            "k": generate_confirmation_key(identity_secret=identity_secret, tag="conf", timestamp=int(time.time())),
            "t": int(time.time()),
            "m": 'react',
            "tag": "conf"
        })
        confPageJson = confirmations_page.json()
        if not confPageJson.get("success", False):
            text = f"FIVETRADES: {username} success False {confPageJson}"
            LOGGER.exception(text)
            return
        trades = confPageJson.get("conf", [])
        About_trades.data[username] = {}
        for index, trade in enumerate(trades):
            name_to = trade["headline"]
            summar = "\n".join(trade["summary"])
            text = f"{name_to}, {summar}"
            creator_id = trade['creator_id']
            cid = trade['id']
            nonce = trade['nonce']
            About_trades.data[username][index] = {
                "text": text,
                "cid": cid,
                "ck": nonce,
                "creator_id": creator_id
            }
            btn = dict(types.InlineKeyboardButton(text=text, callback_data=f'about_trade_{username};{index}'))
            keyboard.add(btn)
        return keyboard
    except Exception as e:
        text = f"FIVETRADES: {username} unknown error, check logs"
        LOGGER.exception(text)


def confirm_all_trades(user: LoginExecutor, **kwargs) -> str:
    from ..bot_main import About_trades

    try:
        username = kwargs.get('username')
        steamid = kwargs.get('steamid')
        identity_secret = kwargs.get('identity_secret')
        confirmations_page = user.session.get("https://steamcommunity.com/mobileconf/getlist", params={
            "p": generate_device_id(str(steamid)),
            "a": steamid,
            "k": generate_confirmation_key(identity_secret=identity_secret, tag="conf", timestamp=int(time.time())),
            "t": int(time.time()),
            "m": 'react',
            "tag": "conf"
        })
        confPageJson = confirmations_page.json()
        if not confPageJson.get("success", False):
            text = f"[ALLTRADES] {username} success False {confPageJson}"
            LOGGER.exception(text)
            return text

        trades = confPageJson.get("conf", [])
        About_trades.data[username] = {}
        cids = []
        cks = []
        for trade in trades:
            name_to = trade["headline"]
            summar = "\n".join(trade["summary"])
            text = f"{name_to}, {summar}"
            cid = trade['id']
            ck = trade['nonce']
            cids.append(cid)
            cks.append(ck)

        if len(cids) < 1:
            return "No trades"
        params0 = [
            ("op", "allow"),
            ("p", generate_device_id(str(steamid))),
            ("a", steamid),
            ("k", generate_confirmation_key(identity_secret=identity_secret, tag="allow", timestamp=int(time.time()))),
            ("t", int(time.time())),
            ("m", 'react'),
            ("tag", "allow")
        ]
        for cid in cids:
            ck = cks[cids.index(cid)]
            params0.append(("cid[]", cid))
            params0.append(("ck[]", ck))
        user.session.headers.update({"Connection": "keep-alive"})
        user.session.headers.update({'X-Requested-With': 'com.valvesoftware.android.steam.community'})
        response = user.session.post('https://steamcommunity.com/mobileconf/multiajaxop', data=params0)
        respjson = response.json()
        success = respjson.get("success", "Err")
        if success:
            text = "Successfully confirmed all trades!"
        else:
            text = f"Success: {success}"
        return text
    except Exception as e:
        text = f"ALLTRADES: {username} unknown error, check logs"
        LOGGER.exception(text)
        return text