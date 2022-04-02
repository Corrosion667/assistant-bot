"""Module for interacting with DialogFlow API."""

import re

from google.cloud import dialogflow

RUSSIAN_LANGUAGE_CODE = 'ru'
ENGLISH_LANGUAGE_CODE = 'en'


def get_intent_answer(project_id, session_id, text) -> str:
    """Get answer from DialogFlow agent for the provided text.

    Args:
        project_id: google project id for DialogFlow agent.
        session_id: id of the conversation (user).
        text: message received from user.

    Returns:
        Text response for user.
    """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    language = detect_language(text=text)
    text_input = dialogflow.TextInput(text=text, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input},
    )
    return response.query_result.fulfillment_text


def detect_language(text):
    """Consider user's language message as russian if it has cyrillic symbols else as english.

    Args:
        text: message received from user.

    Returns:
        Language code: russian or english.
    """
    if bool(re.search('[\u0400-\u04FF]', text)):
        return RUSSIAN_LANGUAGE_CODE
    return ENGLISH_LANGUAGE_CODE
