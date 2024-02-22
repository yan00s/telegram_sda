from .database_connector import execute_query, get_connection
from sqlite3 import IntegrityError
from log import LOGGER
from typing import List
import os
import shutil
import json

def filter_mafile(file: str) -> bool:
    """
    Filters files by the .mafile extension.

    Args:
        file (str): The filename.

    Returns:
        bool: True if the file has a .mafile extension, otherwise False.
    """
    return file.lower().endswith('.mafile')

def load_manifest() -> None:
    """
    Loads the manifest from .mafile files into the database.
    """
    mafiles_directory = './data/'
    db_path = './data/data_base.db'

    mafiles = [file for file in os.listdir(mafiles_directory) if filter_mafile(file)]

    if os.path.exists(db_path):
        accs_names = [row[0] for row in execute_query("SELECT account_name FROM manifest")]
        need_new = len(mafiles) != len(accs_names)
    else:
        need_new = True

    if need_new:
        if os.path.exists(db_path):
            os.remove(db_path)
        new_manifest(mafiles_directory, mafiles)

def new_manifest(mafiles_directory: str, mafiles: List[str]) -> None:
    """
    Creates a new manifest from .mafile files.

    Args:
        mafiles_directory (str): The directory containing the .mafile files.
        mafiles (list): List of .mafile filenames.
    """
    conn = get_connection()

    try:
        with conn:
            conn.execute("CREATE TABLE manifest (account_name TEXT, name_file TEXT, steamid INTEGER, cookies TEXT, refresh_token TEXT, aliveto INTEGER)")
            conn.execute("CREATE TABLE subaccs (peerid INT, access INT)")
    except IntegrityError:
        LOGGER.exception("Error creating tables")
        exit()

    for mafile in mafiles:
        try:
            with open(os.path.join(mafiles_directory, mafile), "r") as f:
                mafile_data = json.load(f)

            steamid = mafile_data.get('Session', {}).get('SteamID', 'none')
            account_name = str(mafile_data.get('account_name', '')).lower()

            req = "INSERT INTO manifest VALUES (?, ?, ?, ?, ?, ?)"
            try:
                with conn:
                    conn.execute(req, [account_name, mafile, steamid, '{}', '', 0])
            except IntegrityError:
                LOGGER.exception(f"Error inserting data for {mafile}")
                move_err_mafile(mafiles_directory, mafile)
        except Exception as e:
            LOGGER.exception(f"Error processing mafile {mafile}: {e}")
            move_err_mafile(mafiles_directory, mafile)

    conn.close()

def move_err_mafile(mafiles_directory: str, mafile: str) -> None:
    """
    Moves the .mafile to the directory for erroneous files.

    Args:
        mafiles_directory (str): The directory containing the .mafile files.
        mafile (str): The .mafile filename.
    """
    err_directory = './err_mafiles/'

    if not os.path.exists(err_directory):
        os.mkdir(err_directory)

    shutil.move(os.path.join(mafiles_directory, mafile), os.path.join(err_directory, mafile))
