from ai_client import generate_text
from prompts import LEARNING_PATH_PROMPT


def get_learning_recommendations(topic: str):

    prompt = LEARNING_PATH_PROMPT.format(
        topic=topic
    )

    return generate_text(
        prompt,
        max_output_tokens=1800
    )