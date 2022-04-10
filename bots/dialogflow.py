"""Module for interacting with DialogFlow API."""

import json
import os
import re
from collections.abc import Iterable
from typing import Union

from dotenv import load_dotenv
from google.cloud import dialogflow
from samples.snippets.intent_management import delete_intent

RUSSIAN_LANGUAGE_CODE = 'ru'
ENGLISH_LANGUAGE_CODE = 'en'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

INTENTS_PATHS = (
    os.path.join(BASE_DIR, 'intents/russian.json'),
    os.path.join(BASE_DIR, 'intents/english.json'),
)


def get_intent_answer(project_id: str, session_id: int, text: str) -> Union[str, None]:
    """Get answer from DialogFlow agent for the provided text.

    Args:
        project_id: google project id for DialogFlow agent.
        session_id: id of the conversation (user).
        text: message received from user.

    Returns:
        Text response for user or None if message unrecognized.
    """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    language = detect_language(text=text)
    text_input = dialogflow.TextInput(text=text, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input},
    )
    if response.query_result.intent.is_fallback:
        return None
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
    """Create or override intents for DialogFlow agent from JSON file with intents.

    Args:
        project_id: google project id for DialogFlow agent.
        file_path: path to the file with intents.
    """
    with open(file_path) as parsed_json:
        intents = json.load(parsed_json)
    for intent in intents.keys():
        current_intent_id = get_intent_id(project_id=project_id, display_name=intent)
        if current_intent_id:
            delete_intent(project_id=project_id, intent_id=current_intent_id)
        training_phrases = intents.get(intent).get('questions')
        answers = intents.get(intent).get('answers')
        create_intent(
            project_id=project_id,
            display_name=intent,
            training_phrases_parts=training_phrases,
            answers=answers,
        )


def get_intent_id(project_id: str, display_name: str) -> Union[str, None]:
    """Get id of intent from DialogFlow agent by the name of intent.

    Args:
        project_id: google project id for DialogFlow agent.
        display_name: name of the intent.

    Returns:
        ID of intent from DialogFlow agent or None if it doesn't exist.
    """
    intents_client = dialogflow.IntentsClient()
    parent_link = dialogflow.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={'parent': parent_link})
    intent_names = [
        intent.name for intent in intents if intent.display_name == display_name
    ]
    try:
        intent_id = [intent_name.split('/')[-1] for intent_name in intent_names][0]
    except IndexError:
        intent_id = None
    return intent_id


def create_intent(
    project_id: str, display_name: str, training_phrases_parts: list, answers: list,
):
    """Create DialogFlow agent intent with the given parameters.

    Args:
        project_id: google project id for DialogFlow agent.
        display_name: name of the intent.
        training_phrases_parts: phrases you can expect from users, that will trigger the intent.
        answers: phrases which agent will deliver to user in response.
    """
    intents_client = dialogflow.IntentsClient()
    parent_link = dialogflow.AgentsClient.agent_path(project_id)
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
    language = detect_language(text=display_name)
    intents_client.create_intent(
        parent=parent_link, intent=intent, language_code=language,
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


def main():
    """Run the script of agent teaching."""
    teach_agent(INTENTS_PATHS)
