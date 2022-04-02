"""Module for interacting with DialogFlow API."""

from google.cloud import dialogflow


def get_intent_answer(project_id, session_id, text, language_code) -> str:
    """Get answer from DialogFlow agent for the provided text.

    Args:
        project_id: google project id for DialogFlow agent.
        session_id: id of the conversation (user).
        text: message received from user.
        language_code: the language of the conversational query.

    Returns: text response for user.
    """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )
    return response.text
