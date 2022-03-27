"""Module for telegram implementation of assistant bot."""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Greet the user. Handler for /start command.

    Args:
        update: incoming update object.
        context: indicates that this is a callback function.
    """
    user = update.effective_user
    update.message.reply_text(f'Hello, {user.first_name}!')


def echo(update: Update, context: CallbackContext):
    """Send to the user his own message that he sent to the bot.

    Args:
        update: incoming update object.
        context: indicates that this is a callback function.
    """
    update.message.reply_text(update.message.text)


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
        Filters.text & ~Filters.command, echo,
    ))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
