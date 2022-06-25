"""Module for logging adjustment of the project."""

import logging
import random
from contextlib import suppress

import telegram
from requests.exceptions import ReadTimeout
from vk_api.vk_api import VkApiMethod

UNRECOGNISED_MESSAGE_WARNING = 'Got unrecognised message "{0}" from user with id {1}.'


class TelegramLogsHandler(logging.Handler):
    """Class for handler of logs to send them to TG admin."""

    def __init__(self, telegram_token: str, admin_chat_id: str):
        """Initiate handler instance.

        Args:
            telegram_token: bot token from @BotFather in telegram.
            admin_chat_id: id of the admin from @userinfobot to send him notifications.
        """
        super().__init__()
        self.tg_bot = telegram.Bot(token=telegram_token)
        self.admin_chat_id = admin_chat_id

    def emit(self, record: logging.LogRecord):
        """Send log record to telegram chat.

        Args:
            record: text log to be sent.
        """
        log_entry = self.format(record)
        with suppress(telegram.error.NetworkError):
            self.tg_bot.send_message(chat_id=self.admin_chat_id, text=log_entry)


class VkontakteLogsHandler(logging.Handler):
    """Class for handler of logs to send them to VK."""

    def __init__(self, vk_api_connector: VkApiMethod, admin_chat_id: str):
        """Initiate handler instance.

        Args:
            vk_api_connector: instance of VK Api Method to interact with VKApi methods.
            admin_chat_id: id of the admin in VK.com to send him notifications.
        """
        super().__init__()
        self.vk_api_connector = vk_api_connector
        self.admin_chat_id = admin_chat_id

    def emit(self, record: logging.LogRecord):
        """Send log record to VK chat.

        Args:
            record: text log to be sent.
        """
        log_entry = self.format(record)
        # do not try to send logs when connection lost
        with suppress(ReadTimeout, ConnectionError):
            self.vk_api_connector.messages.send(
                user_id=self.admin_chat_id,
                message=log_entry,
                random_id=random.randint(1, 1000),
            )
