# Telegram Steam Account Manager (telegram_sda)

## Description

Telegram Steam Account Manager (telegram_sda) is a versatile bot designed for managing Steam accounts through Telegram. It empowers administrators to add sub-users who can handle logins via QR code or receive two-factor authentication (2FA) codes. Additionally, sub-users can confirm or cancel trades. Future plans include adding new accounts through the bot and configuring accounts without 2FA.

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python 3.9+ installed.
3. Install dependencies using `pip install -r requirements.txt`.

## Setting Environment Variables

1. Create a `.env` file in the project's root directory.
2. Specify your Telegram bot API key and your peerid from the Telegram bot https://t.me/ShowJsonBot in the `.env` file, following the example:
    ```plaintext
    API_TGBOT="your_API_key"
    ADMIN_PEERID=your_peerid
    ```
3. Move your maFiles to "data" folder

## Usage
- The bot can automatically log in and update the session without requiring manual password input, simply by creating a file named `accounts.txt` and adding accounts in the format `username:password` separated by a new line.
- An administrator can add a sub-user using the command `/add_subacc`.
- Sub-users can manage logins via QR code or receive 2FA codes for login, as well as confirm or cancel trades.

## Planned Additions

- Adding new accounts through the bot.
- Configuring accounts without 2FA installed.

## Running the Bot

Start the bot using the command: `python main.py`




## На русском:

### Установка:

1. Клонируйте репозиторий на свой компьютер.
2. Убедитесь, что у вас установлен Python версии 3.9+.
3. Установите зависимости с помощью `pip install -r requirements.txt`.


### Настройка:

1. Создайте файл `.env` в корневой директории проекта.
2. Укажите ваш API ключ от Telegram бота и ваш peerid из [Telegram бота](https://t.me/ShowJsonBot)  в файле `.env`, следуя примеру:
    ```plaintext
    API_TGBOT="your_API_key"
    ADMIN_PEERID=your_peerid
    ```
3. Переместите свои maFiles в папку "data"
    
## Использование
- Бот может автоматически входить и обновлять сеанс без необходимости вручную вводить пароль, просто создав файл с именем accounts.txt и добавив аккаунты в формате username:password, разделяя их новой строкой.
- Администратор может добавить суб-пользователя с помощью команды /add_subacc.
- Суб-пользователи могут управлять входами через QR-код или получать коды 2FA для входа, а также подтверждать или отменять сделки.

## В планах

- Добавление аккаунтов через бота.
- Настройка и добавление аккаунтов на которых не установлен аутентификатор.


### Запуск:

1. Запустите бота с помощью команды `python main.py`.
2. Бот готов к использованию!


### Помощь и поддержка

Если у вас возникли вопросы или проблемы, не стесняйтесь обращаться к нам: [Telegram](https://t.me/yan00s)


### Лицензия

Этот проект лицензирован по лицензии MIT. См. файл LICENSE для получения дополнительной информации.
