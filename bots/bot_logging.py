"""Module for logging adjustment of the project."""

import logging
import random

import telegram


class TelegramLogsHandler(logging.Handler):
    """Class for handler of logs to send them to TG admin."""

    def __init__(self, telegram_token, admin_chat_id):
        """Initiate handler instance.

        Args:
            telegram_token: bot token from @BotFather in telegram.
            admin_chat_id: id of the admin from @userinfobot to send him notifications.
        """
        super().__init__()
        self.tg_bot = telegram.Bot(token=telegram_token)
        self.admin_chat_id = admin_chat_id

    def emit(self, record):
        """Send log record to telegram chat.

        Args:
            record: text log to be sent.
        """
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.admin_chat_id, text=log_entry)


class VkontakteLogsHandler(logging.Handler):
    """Class for handler of logs to send them to VK."""

    def __init__(self, vk_session_api, admin_chat_id):
        """Initiate handler instance.

        Args:
            vk_session_api: instance of VK session api.
            admin_chat_id: id of the admin in VK.com to send him notifications.
        """
        super().__init__()
        self.vk_session_api = vk_session_api
        self.admin_chat_id = admin_chat_id

    def emit(self, record):
        """Send log record to VK chat.

        Args:
            record: text log to be sent.
        """
        log_entry = self.format(record)
        self.vk_session_api.messages.send(
            user_id=self.admin_chat_id,
            message=log_entry,
            random_id=random.randint(1, 1000),
        )
