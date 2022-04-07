"""Module for vkontakte implementation of assistant bot."""

import logging
import os
import random
import time

from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.longpoll import Event, VkEventType, VkLongPoll
from vk_api.vk_api import VkApiMethod

from bots.bot_logging import VkontakteLogsHandler, log_unrecognised_message
from bots.dialogflow import get_intent_answer

UNEXPECTED_ERROR_TIMEOUT = 100

UNEXPECTED_ERROR_LOG = '{exception}\nUnexpected error happened! Retrying in {timeout} seconds.'

logger = logging.getLogger(__name__)


def send_answer(event: Event, vk_api_method: VkApiMethod):
    """Send answer to user using replies from Dialog Flow API.

    Args:
        event: event from server.
        vk_api_method: instance of VK Api Method.
    """
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    chat_id = event.user_id
    incoming_message = event.text
    reply_message = get_intent_answer(
        project_id=project_id,
        session_id=chat_id,
        text=incoming_message,
    )
    if reply_message:
        vk_api_method.messages.send(
            user_id=chat_id,
            message=reply_message,
            random_id=random.randint(1, 1000),
        )
    else:
        log_unrecognised_message(
            logger=logger,
            incoming_message=incoming_message,
            chat_id=chat_id,
        )


def interact_longpoll(vk_long_poll: VkLongPoll, vk_api_method: VkApiMethod):
    """Interact with VK longpoll server.

    Args:
        vk_long_poll: instance of VK Long Poll.
        vk_api_method: instance of VK Api Method.
    """
    for event in vk_long_poll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(event, vk_api_method)


def main():
    """Run the bot as script."""
    logging.basicConfig(
        format='VKONTAKTE_BOT %(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO,
    )
    load_dotenv()
    vk_token = os.getenv('VKONTAKTE_TOKEN')
    admin_chat_id = os.getenv('VKONTAKTE_ADMIN_ID')
    vk_api = VkApi(token=vk_token)
    vk_api_method = vk_api.get_api()
    vkontakte_logs_handler = VkontakteLogsHandler(vk_api_method, admin_chat_id)
    vkontakte_logs_handler.setLevel(logging.WARNING)
    logger.addHandler(vkontakte_logs_handler)
    vk_long_poll = VkLongPoll(vk_api)
    logger.info('Bot started.')
    while True:
        try:
            interact_longpoll(vk_long_poll=vk_long_poll, vk_api_method=vk_api_method)
        except Exception as exc:
            error_message = UNEXPECTED_ERROR_LOG.format(
                exception=exc, timeout=UNEXPECTED_ERROR_TIMEOUT,
            )
            logger.error(error_message)
            time.sleep(UNEXPECTED_ERROR_TIMEOUT)
            continue


if __name__ == '__main__':
    main()
