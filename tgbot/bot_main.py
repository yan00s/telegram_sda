from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv, find_dotenv
import os

# Import functions from other modules
from .database_operations import check_access, load_manifest
from .handlers import (
    start_msg,
    help_msg,
    other_msg,
    list_subacc,
    add_subaccfirst,
    add_subaccfinal,
    dell_subaccfirst,
    dell_subaccfinal,
    select_account,
    handle_approve_qr,
    handle_qr_photo,
    update_session,
    cancel_action,
    get_two_factor_authentication,
    inputpassw,
    get_five_trades,
    confirm_all_trades_all,
    about_trade,
    get_cancel_trade,
    get_accept_trade,
    States,
)


# Class for storing trade data
class About_trades:
    data = {}

# Load environment variables from the .env file
load_dotenv(find_dotenv())
API_TOKEN = os.getenv("API_TGBOT")

# Create bot and dispatcher objects
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Register handlers
dp.register_message_handler(check_access(help_msg), commands="help", state="*")
dp.register_message_handler(check_access(start_msg), commands="start", state="*")
dp.register_message_handler(check_access(list_subacc), commands="list_subacc", state="*")
dp.register_message_handler(check_access(add_subaccfirst), commands="add_subacc", state="*")
dp.register_message_handler(check_access(dell_subaccfirst), commands="delete_subacc", state="*")

# Register handlers for Inline buttons
dp.register_callback_query_handler(check_access(select_account), Text(startswith="select_"), state="*")
dp.register_callback_query_handler(check_access(get_two_factor_authentication), Text(startswith="get2fa_"), state="*")
dp.register_callback_query_handler(check_access(handle_approve_qr), Text(startswith="approveqr="), state="*")
dp.register_callback_query_handler(check_access(confirm_all_trades_all), Text(startswith="confirm_all_trades_"))
dp.register_callback_query_handler(check_access(get_five_trades), Text(startswith="get_last_five_trade_"))
dp.register_callback_query_handler(check_access(update_session), Text(startswith="update_session_"))
dp.register_callback_query_handler(check_access(about_trade), Text(startswith="about_trade_"))
dp.register_callback_query_handler(check_access(get_cancel_trade), Text(startswith="cancel="))
dp.register_callback_query_handler(check_access(get_accept_trade), Text(startswith="accept="))
dp.register_callback_query_handler(cancel_action, Text(startswith="back"), state="*")

# Register handlers for bot states
dp.register_message_handler(inputpassw, state=States.waitpassw)
dp.register_message_handler(handle_qr_photo, state=States.approve_qr, content_types=["text",'photo'])
dp.register_message_handler(add_subaccfinal, state=States.add_subacc)
dp.register_message_handler(dell_subaccfinal, state=States.dell_subacc)
dp.register_message_handler(check_access(other_msg), state="*")

# Start the bot
def main():
    from aiogram import executor
    # Load the list of accounts on startup
    load_manifest()
    # Start polling for updates
    executor.start_polling(dp, skip_updates=True)
