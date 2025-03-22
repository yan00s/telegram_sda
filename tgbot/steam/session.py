import json
import time
from typing import Union, Tuple

import requests
from fake_headers import Headers

from ..database_operations import (
    update_cookies,
    update_refresh_token,
    get_cookies,
    get_refresh_token,
    need_check_alive,
    update_check_alive
)
from ..mafile_operations import pars_mafile_data
from .login import LoginExecutor
from log import LOGGER


def get_mafile(mafile_name: str) -> dict:
    with open('./data//' + mafile_name, 'r') as f:
        mafile: dict = json.load(f)
    return mafile


def create_session(headers: dict = {}, cookies: dict = {}) -> requests.Session:
    session_initial = requests.session()
    session_initial.headers.update(headers)
    session_initial.cookies.update(cookies)
    return session_initial


def login_steam(**kwargs) -> Tuple[Union[LoginExecutor, None], str]:
    username: str = kwargs.get('username', "")
    password: str = kwargs.get('password', "")
    shared_secret = kwargs.get('shared_secret', "")
    steamid = kwargs.get('steamid', "")

    if kwargs.get('new_session', False):
        update_cookies("{}", username)
        cookies = {}
    else:
        cookies = get_cookies(username)

    if len(cookies) > 3:
        ses = create_session(Headers().generate(), json.loads(cookies))
        exec_login = LoginExecutor(username, "", shared_secret, ses)
        exec_login.refresh_token = get_refresh_token(username)
        exec_login.steamid = steamid
        need_check = need_check_alive(username)
        text = "anything err"
        if need_check:
            valid_session = exec_login.check_valid_session()
        else:
            valid_session = True

        if valid_session:
            if need_check:
                text = f"STEAM: {username} successfully logged in to steam (cookies), Cookies have expired, updating..."
                keys_cookies = exec_login.session.cookies.keys()
                values_cookies = exec_login.session.cookies.values()
                cookies = dict(zip(keys_cookies, values_cookies))
                update_cookies(json.dumps(cookies), username)
            else:
                text = f"STEAM: {username} successfully logged in to steam (cookies), cookies do not expire"
            LOGGER.info(text)
        else:
            exec_login = None
            text = "Invalid session" ######## NEED UPDATE IN GITHUB!!!!
        return exec_login, text
    else:
        if len(password) < 3:
            return None, "Invalid session"
        try:
            ses = create_session(Headers().generate())
            exec_login = LoginExecutor(username, password, shared_secret, ses)
            update_session = exec_login.login()
            response = update_session.get("https://steamcommunity.com/", timeout=20)

            if username.lower() in response.text:
                text = f"STEAM: {username} successfully logged in to steam"
                LOGGER.info(text)

                keys_cookies = update_session.cookies.keys()
                values_cookies = update_session.cookies.values()
                cookies = dict(zip(keys_cookies, values_cookies))
                deadline = time.time() + 3600 * 24

                update_cookies(json.dumps(cookies), username)
                update_refresh_token(exec_login.refresh_token, username)
                update_check_alive(deadline, username)
            else:
                text = f"STEAM: {username} can't log in! status = {response.status_code}"
            return exec_login, text
        except Exception:
            err = f"[{username}] unknown err in login_steam"
            LOGGER.exception(err)
    return None, "unknown err, check logs..."


async def get_userses(peerid: int, mafile_name: str, new_session: bool, **kwargs) -> Tuple[
    Union[LoginExecutor, None], dict, str]:
    from ..bot_main import bot
    from ..handlers import States, get_cancel_inline
    mafile = get_mafile(mafile_name)
    success, mafile_data = pars_mafile_data(mafile)
    if new_session:
        mafile_data["new_session"] = True
        passw_arg = kwargs.get("password", False)
        if passw_arg:
            mafile_data["password"] = passw_arg
        if not mafile_data.get('password', False):
            await bot.send_message(peerid, "Input password:", reply_markup=get_cancel_inline())
            await States.waitpassw.set()
            States.waitpassw_data[peerid] = mafile_name
            return "", "", "Input password:"
    if success:
        user, text = login_steam(**mafile_data)
    else:
        text = mafile_data
    return user, mafile_data, text
