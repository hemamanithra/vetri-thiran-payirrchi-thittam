from ai_client import generate_text
from prompts import QA_PROMPT


def answer_question(question: str):

    prompt = QA_PROMPT.format(
        question=question
    )

    return generate_text(
        prompt
    )