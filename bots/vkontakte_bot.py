"""Module for vkontakte implementation of assistant bot."""

import os
from dotenv import load_dotenv

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def main():
    """Run the bot as script."""
    load_dotenv()
    vk_token = os.getenv('VKONTAKTE_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()
