"""Module for logging adjustment of the project."""

import logging
import random

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
        # do not try to send logs when connection lost
        try:
            self.tg_bot.send_message(chat_id=self.admin_chat_id, text=log_entry)
        except telegram.error.NetworkError:
            pass


class VkontakteLogsHandler(logging.Handler):
    """Class for handler of logs to send them to VK."""

    def __init__(self, vk_api_method: VkApiMethod, admin_chat_id: str):
        """Initiate handler instance.

        Args:
            vk_api_method: instance of VK Api Method.
            admin_chat_id: id of the admin in VK.com to send him notifications.
        """
        super().__init__()
        self.vk_api_method = vk_api_method
        self.admin_chat_id = admin_chat_id

    def emit(self, record: logging.LogRecord):
        """Send log record to VK chat.

        Args:
            record: text log to be sent.
        """
        log_entry = self.format(record)
        # do not try to send logs when connection lost
        try:
            self.vk_api_method.messages.send(
                user_id=self.admin_chat_id,
                message=log_entry,
                random_id=random.randint(1, 1000),
            )
        except ReadTimeout:
            pass


def log_unrecognised_message(logger: logging.Logger, incoming_message: str, chat_id: int):
    """Create log about receiving unrecognised message from the specific user.

    Args:
        logger: instance of Logger class.
        incoming_message: unrecognised message received from user.
        chat_id: id of the user in Telegram or Vkontakte which sent the message.

    """
    log_message = UNRECOGNISED_MESSAGE_WARNING.format(
        incoming_message, chat_id,
    )
    logger.warning(log_message)
