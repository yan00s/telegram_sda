from pysteamauth.pb.steammessages_auth.steamclient_pb2 import CAuthentication_UpdateAuthSessionWithMobileConfirmation_Request
from steampy.exceptions import InvalidCredentials, CaptchaRequired
from steampy import guard
from google.protobuf import message as _message
from log import LOGGER

import requests
import base64
import hmac
import hashlib
import json
import rsa

from .models_update import SteamUrl

class LoginExecutor:

    def __init__(self, username: str, password: str, shared_secret: str, session: requests.Session) -> None:
        self.username = username
        self.password = password
        self.one_time_code = ''
        self.shared_secret = shared_secret
        self.session = session
        self.client_id = ''
        self.steamid = ''
        self.request_id = ''
        self.refresh_token = ''
        self.access_token = ''
        self.nonce_store = ''
        self.auth_store = ''
        self.nonce_com = ''
        self.auth_com = ''

    def login(self) -> requests.Session:
        login_response = self._send_login_request()
        self._update_stem_guard(login_response)
        self._pool_sessions_steam()
        finallized_response = self._finallez_login()
        self._setstokens(finallized_response)
        self.set_sessionid_cookies()
        return self.session

    def _send_login_request(self) -> requests.Response:
        rsa_params = self._fetch_rsa_params()
        encrypted_password = self._encrypt_password(rsa_params)
        rsa_timestamp = rsa_params['rsa_timestamp']
        request_data = self._prepare_login_request_data(encrypted_password, rsa_timestamp)
        response = self.session.post(SteamUrl.BeginAuthSessionViaCredentials_URL, data=request_data)
        return response

    def set_sessionid_cookies(self):
        sessionid = self.session.cookies.get_dict()['sessionid']
        community_domain = SteamUrl.COMMUNITY_URL[8:]
        store_domain = SteamUrl.STORE_URL[8:]
        community_cookie = self._create_session_id_cookie(sessionid, community_domain)
        store_cookie = self._create_session_id_cookie(sessionid, store_domain)
        self.session.cookies.set(**community_cookie)
        self.session.cookies.set(**store_cookie)

    @staticmethod
    def _create_session_id_cookie(sessionid: str, domain: str) -> dict:
        return {"name": "sessionid",
                "value": sessionid,
                "domain": domain}

    def _fetch_rsa_params(self, current_number_of_repetitions: int = 0) -> dict:
        maximal_number_of_repetitions = 5
        self.session.post(SteamUrl.COMMUNITY_URL)
        response = self.session.get(SteamUrl.GetPasswordRSAPublicKey_URL + self.username)
        key_response = json.loads(response.text)
        try:
            rsa_mod = int(key_response["response"]['publickey_mod'], 16)
            rsa_exp = int(key_response["response"]['publickey_exp'], 16)
            rsa_timestamp = key_response["response"]['timestamp']
            return {'rsa_key': rsa.PublicKey(rsa_mod, rsa_exp),
                    'rsa_timestamp': rsa_timestamp}
        except KeyError:
            if current_number_of_repetitions < maximal_number_of_repetitions:
                return self._fetch_rsa_params(current_number_of_repetitions + 1)
            else:
                raise ValueError('Could not obtain rsa-key')

    def _encrypt_password(self, rsa_params: dict) -> str:
        return base64.b64encode(rsa.encrypt(self.password.encode('utf-8'), rsa_params['rsa_key']))

    def _prepare_login_request_data(self, encrypted_password: str, rsa_timestamp: str) -> dict:
        return {
            'persistence': "1",
            'encrypted_password': encrypted_password,
            'account_name': self.username,
            'encryption_timestamp': rsa_timestamp,
        }

    @staticmethod
    def _check_for_captcha(login_response: requests.Response) -> None:
        if login_response.json().get('captcha_needed', False):
            raise CaptchaRequired('Captcha required')

    def _enter_steam_guard_if_necessary(self, login_response: requests.Response) -> requests.Response:
        if login_response.json()['requires_twofactor']:
            self.one_time_code = guard.generate_one_time_code(self.shared_secret)
            return self._send_login_request()
        return login_response

    @staticmethod
    def _assert_valid_credentials(login_response: requests.Response) -> None:
        if not login_response.json()['response']["client_id"]:
            raise InvalidCredentials(login_response.json()["response"]['extended_error_message'])

    def _perform_redirects(self, response_dict: dict) -> None:
        parameters = response_dict.get('transfer_parameters')
        if parameters is None:
            raise Exception('Cannot perform redirects after login, no parameters fetched')
        for url in response_dict['transfer_urls']:
            self.session.post(url, parameters)

    def _fetch_home_page(self, session: requests.Session) -> requests.Response:
        return session.post(SteamUrl.COMMUNITY_URL + '/my/home/')

    def _update_stem_guard(self, login_response):
        response_json = json.loads(login_response.text)
        self.client_id = response_json["response"]["client_id"]
        self.steamid = response_json["response"]["steamid"]
        self.request_id = response_json["response"]["request_id"]
        code_type = 3
        code = guard.generate_one_time_code(self.shared_secret)

        update_data = {
            'client_id': self.client_id,
            'steamid': self.steamid,
            'code_type': code_type,
            'code': code
        }

        response = self.session.post(SteamUrl.UpdateAuthSessionWithSteamGuardCode_URL, data=update_data)

    def _pool_sessions_steam(self):

        pool_data = {
            'client_id': self.client_id,
            'request_id': self.request_id
        }

        response = self.session.post(SteamUrl.PollAuthSessionStatus_URL, data=pool_data)
        response_json = json.loads(response.text)
        self.refresh_token = response_json["response"]["refresh_token"]

    def _finallez_login(self):
        sessionid = self.session.cookies["sessionid"]
        redir = "https://steamcommunity.com/login/home/?goto="

        finallez_data = {
            'nonce': self.refresh_token,
            'sessionid': sessionid,
            'redir': redir
        }

        response = self.session.post("https://login.steampowered.com/jwt/finalizelogin", data=finallez_data)
        return response

    def _setstokens(self, fin_resp):
        response_json = json.loads(fin_resp.text)
        self.nonce_store = response_json["transfer_info"][0]["params"]["nonce"]
        self.auth_store = response_json["transfer_info"][0]["params"]["auth"]
        self.nonce_com = response_json["transfer_info"][1]["params"]["nonce"]
        self.auth_com = response_json["transfer_info"][1]["params"]["auth"]

        ##com_token:
        com_data = {
            'nonce': self.nonce_com,
            'auth': self.auth_com,
            'steamID': self.steamid
        }
        _ = self.session.post(SteamUrl.Settoken_community_URL, data=com_data)

    def check_valid_session(self) -> bool:

        params = {  # # for store:  'https://store.steampowered.com/',
            'redir': 'https://steamcommunity.com',
        }

        try:
            response = self.session.get('https://login.steampowered.com/jwt/refresh', params=params, timeout=15)
            if len(response.history) == 1:
                return False
            if self.username.lower() in response.text:
                return True
        except Exception:
            err = f"[{self.username}] unknown err in refresh token"
            LOGGER.exception(err)

        return False

    def _build_signature(self, shared_secret, steam_id: int, client_id: int, version: int):
        msg = (
                version.to_bytes(2, 'little') +
                client_id.to_bytes(8, 'little') +
                steam_id.to_bytes(8, 'little')
        )
        signature = hmac.new(key=shared_secret, msg=msg, digestmod=hashlib.sha256).digest()
        return signature

    def _pbmessage_to_request(self, msg: _message.Message) -> str:
        return str(base64.b64encode(msg.SerializeToString()), 'utf8')

    def approve_qr(self, url: str):
        self._set_steamid_access_token()

        steam_id = int(self.steamid)
        shared_secret = self.shared_secret

        version, client_id = map(int, url.split("/")[-2:])
        decoded_secret = base64.standard_b64decode(shared_secret)
        signature = self._build_signature(decoded_secret, steam_id, int(client_id), int(version))

        res = {
            "client_id": client_id,
            "version": version,
            "steamid": steam_id,
            "confirm": True,
            "signature": signature,
            "persistence": 1
        }

        message = CAuthentication_UpdateAuthSessionWithMobileConfirmation_Request(
            client_id=client_id,
            version=version,
            steamid=steam_id,
            confirm=True,
            signature=signature,
            persistence=1
        )

        msgneed = self._pbmessage_to_request(message)
        res = {"input_protobuf_encoded": msgneed}

        return self.send_reqqr(res)

    def _set_steamid_access_token(self):
        token: str = self.session.cookies.get("steamLoginSecure", "")
        steamid, access_token = token.split("%7C%7C")
        self.steamid = steamid
        self.access_token = access_token

    def send_reqqr(self, data):
        url = "https://api.steampowered.com/IAuthenticationService/UpdateAuthSessionWithMobileConfirmation/v1"
        params = {"access_token": self.access_token}

        try:
            resp = self.session.post(url, params=params, data=data)
            if resp.status_code == 200:
                return "Successfully logined by QR"
            else:
                return f"unknown response in login by QR {resp.text}"
        except:
            text = f"unknown error in login by QR check logs"
            LOGGER.exception(text)
            return text
