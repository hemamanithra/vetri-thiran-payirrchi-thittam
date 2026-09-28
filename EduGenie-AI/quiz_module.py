import json
import re

from ai_client import generate_text
from prompts import QUIZ_PROMPT


# ============================================================
# CLEAN MARKDOWN JSON
# ============================================================

def clean_json_block(text: str):

    text = text.strip()

    # Remove ```json
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove ```
    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


# ============================================================
# VALIDATE QUIZ
# ============================================================

def validate_quiz(data):

    if not isinstance(
        data,
        dict
    ):

        raise ValueError(
            "Quiz response must be a JSON object."
        )


    questions = data.get(
        "questions"
    )


    if not isinstance(
        questions,
        list
    ):

        raise ValueError(
            "Quiz response does not contain questions."
        )


    if len(questions) != 3:

        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )


    for question in questions:

        if not isinstance(
            question,
            dict
        ):

            raise ValueError(
                "Invalid question object."
            )


        options = question.get(
            "options"
        )


        if not isinstance(
            options,
            list
        ):

            raise ValueError(
                "Options must be a list."
            )


        if len(options) != 4:

            raise ValueError(
                "Each question must have exactly 4 options."
            )


        answer = question.get(
            "answer"
        )


        if answer not in options:

            raise ValueError(
                "Answer must match one of the options."
            )


    return data


# ============================================================
# GENERATE QUIZ
# ============================================================

def generate_quiz(text: str):

    prompt = QUIZ_PROMPT.format(
        text=text
    )


    raw_response = generate_text(

        prompt,

        temperature=0.2,

        max_output_tokens=1800
    )


    cleaned_response = clean_json_block(
        raw_response
    )


    # ========================================================
    # FIRST PARSE ATTEMPT
    # ========================================================

    try:

        data = json.loads(
            cleaned_response
        )

        return validate_quiz(
            data
        )

    except (
        json.JSONDecodeError,
        ValueError
    ):

        pass


    # ========================================================
    # REPAIR ATTEMPT
    # ========================================================

    repair_prompt = f"""

Convert the following content into valid JSON.

Return ONLY JSON.

Use exactly this structure:

{{
    "questions": [
        {{
            "question": "string",
            "options": [
                "string",
                "string",
                "string",
                "string"
            ],
            "answer": "string",
            "explanation": "string"
        }}
    ]
}}

Requirements:

- Exactly 3 questions.
- Exactly 4 options per question.
- Every answer must exactly match one option.

Content:

{raw_response}
"""


    repaired_response = generate_text(

        repair_prompt,

        temperature=0.1,

        max_output_tokens=1800
    )


    repaired_response = clean_json_block(
        repaired_response
    )


    try:

        data = json.loads(
            repaired_response
        )

        return validate_quiz(
            data
        )

    except Exception as error:

        raise RuntimeError(
            f"Could not parse quiz response: {error}"
        )