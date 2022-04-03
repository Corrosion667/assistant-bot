"""Module for vkontakte implementation of assistant bot."""

import os
import random

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll


def echo(event, vk_session_api):
    """Reply to user with the message he sent to bot.

    Args:
        event: event from server.
        vk_session_api: current instance of API.
    """
    vk_session_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000),  # noqa: S311
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
            echo(event, vk_session_api)


if __name__ == '__main__':
    main()
