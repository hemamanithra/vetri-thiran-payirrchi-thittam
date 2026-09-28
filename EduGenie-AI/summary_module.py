from ai_client import generate_text
from prompts import SUMMARY_PROMPT


def summarize_text(text: str):

    prompt = SUMMARY_PROMPT.format(
        text=text
    )

    return generate_text(
        prompt,
        max_output_tokens=1200
    )