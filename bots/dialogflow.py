"""Module for interacting with DialogFlow API."""

import json
import os
import re
from collections.abc import Iterable
from dotenv import load_dotenv
from google.cloud import dialogflow

RUSSIAN_LANGUAGE_CODE = 'ru'
ENGLISH_LANGUAGE_CODE = 'en'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

INTENTS_PATHS = (
    os.path.join(BASE_DIR, 'intents/russian.json'),
    os.path.join(BASE_DIR, 'intents/english.json'),
)


def get_intent_answer(project_id: str, session_id: str, text: str) -> str:
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


def detect_language(text: str) -> str:
    """Consider message or intent language as russian if it has cyrillic symbols else as english.

    Args:
        text: phrase for checking.

    Returns:
        Language code which is russian or english.
    """
    if bool(re.search('[\u0400-\u04FF]', text)):
        return RUSSIAN_LANGUAGE_CODE
    return ENGLISH_LANGUAGE_CODE


def create_intents_from_json(project_id: str, file_path: str):
    """Create intents for DialogFlow agent from JSON file with intents.

    Args:
        project_id: google project id for DialogFlow agent.
        file_path: path to the file with intents.
    """
    with open(file_path) as parsed_json:
        intents = json.load(parsed_json)
    for intent in intents.keys():
        language = detect_language(text=intent)
        training_phrases = intents.get(intent).get('questions')
        answers = intents.get(intent).get('answers')
        create_intent(
            project_id=project_id,
            display_name=intent,
            training_phrases_parts=training_phrases,
            answers=answers,
            language=language,
        )


def create_intent(
    project_id: str, display_name: str, training_phrases_parts: list, answers: list, language: str,
):
    """Create DialogFlow agent intent with the given parameters.

    Args:
        project_id: google project id for DialogFlow agent.
        display_name: name of the intent.
        training_phrases_parts: phrases you can expect from users, that will trigger the intent.
        answers: phrases which agent will deliver to user in response.
        language: Language code which is russian or english
    """
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=answers)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message],
    )
    intents_client.create_intent(
        parent=parent, intent=intent, language_code=language,
    )


def teach_agent(intents_paths: Iterable[str]):
    """Script for teaching DialogFlow Agent with intents in JSONs.

    Args:
        intents_paths: collection with paths to JSON files.
    """
    load_dotenv()
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    for path in intents_paths:
        create_intents_from_json(
            project_id, path,
        )


if __name__ == '__main__':
    teach_agent(INTENTS_PATHS)
