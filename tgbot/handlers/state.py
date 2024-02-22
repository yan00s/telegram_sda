from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    """
    Defines states used in the bot's conversation flow.
    """
    waitpassw = State()  # State for waiting for password input
    waitpassw_data = {}  # Data associated with the waitpassw state
    add_2fa = State()  # State for adding two-factor authentication
    dell_2fa = State()  # State for deleting two-factor authentication
    add_subacc = State()  # State for adding a sub-account
    dell_subacc = State()  # State for deleting a sub-account
    approve_qr = State()  # State for approving QR code login
    approve_qr_data = {}  # Data associated with the approve_qr state
