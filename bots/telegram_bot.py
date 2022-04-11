"""Module for telegram implementation of assistant bot."""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from bots.bot_logging import UNRECOGNISED_MESSAGE_WARNING, TelegramLogsHandler
from bots.dialogflow import get_intent_response

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
    incoming_message = update.message.text
    dialogflow_response = get_intent_response(
        project_id=project_id,
        session_id=chat_id,
        text=incoming_message,
    )
    reply_message = dialogflow_response.query_result.fulfillment_text
    update.message.reply_text(reply_message)
    if dialogflow_response.query_result.intent.is_fallback:
        log_message = UNRECOGNISED_MESSAGE_WARNING.format(
            incoming_message, chat_id,
        )
        logger.warning(log_message)


def error_handler(update: object, context: CallbackContext):
    """Log the error which will be sent as telegram message to notify the developer.

    Args:
        update: incoming update object.
        context: indicates that this is a callback function.
    """
    logger.error(msg='Exception while handling an update:', exc_info=context.error)


def main():
    """Run the bot as script."""
    logging.basicConfig(
        format='TELEGRAM_BOT %(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO,
    )
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    admin_chat_id = os.getenv('TELEGRAM_ADMIN_ID')
    telegram_logs_handler = TelegramLogsHandler(telegram_token, admin_chat_id)
    telegram_logs_handler.setLevel(logging.WARNING)
    logger.addHandler(telegram_logs_handler)
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, send_answer,
    ))
    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    logger.info('Bot started.')
    updater.idle()


if __name__ == '__main__':
    main()
