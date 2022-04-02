"""Module for telegram implementation of assistant bot."""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from bots.dialogflow import get_intent_answer

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Greet the user. Handler for /start command.

    Args:
        update: incoming update object.
        context: indicates that this is a callback function.
    """
    user = update.effective_user
    update.message.reply_text(f'Hello, {user.first_name}!')


def send_answer(update: Update, context: CallbackContext):
    """Send answer to user using replies from Dialog Flow API.

    Args:
        update: incoming update object.
        context: indicates that this is a callback function.
    """
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    chat_id = update.message.chat_id
    reply_message = get_intent_answer(
        project_id=project_id,
        session_id=chat_id,
        text=update.message.text,
    )
    update.message.reply_text(reply_message)


def main():
    """Run the bot as script."""
    logging.basicConfig(
        format='%(name)s %(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO,
    )
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, send_answer,
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
