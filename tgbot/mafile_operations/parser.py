from os.path import exists
import re

def pars_mafile_data(mafile: dict) -> tuple[bool, dict|str]:
    """Parse maFile data and return a tuple indicating success and the parsed data."""
    maf_session = mafile.get('Session', {})
    if not maf_session:
        return False, "Didn't find 'Session' in maFile"

    username = mafile.get('account_name', '')
    shared_secret = mafile.get('shared_secret', '')
    identity_secret = mafile.get('identity_secret', '')
    oauth = maf_session.get('OAuthToken', '')
    steamid = maf_session.get('SteamID', '')

    data = {
        "username": username,
        "password": get_password(username),
        "identity_secret": identity_secret,
        "oauth": oauth,
        "steamid": steamid,
        "shared_secret": shared_secret
    }

    is_valid = steamid and (username or identity_secret)
    return is_valid, data


def get_password(username: str) -> str:
    """Get the password for the given username from accounts.txt."""
    password = ''
    if exists('accounts.txt'):
        with open('accounts.txt', 'r') as file:
            accounts = file.read()
            match = re.search(rf'{username}[:|;](.*?)(\s|$)', accounts)
            if match:
                password = match.group(1).strip()
    return password
