"""Module for vkontakte implementation of assistant bot."""

import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from bots.dialogflow import get_intent_answer


def send_answer(event, vk_session_api):
    """Send answer to user using replies from Dialog Flow API.

    Args:
        event: event from server.
        vk_session_api: current instance of API.
    """
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    chat_id = event.user_id
    reply_message = get_intent_answer(
        project_id=project_id,
        session_id=chat_id,
        text=event.text,
    )
    if reply_message:
        vk_session_api.messages.send(
            user_id=chat_id,
            message=reply_message,
            random_id=random.randint(1, 1000),
        )


def main():
    """Run the bot as script."""
    load_dotenv()
    vk_token = os.getenv('VKONTAKTE_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    vk_session_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_answer(event, vk_session_api)


if __name__ == '__main__':
    main()
