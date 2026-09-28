from ai_client import generate_text

from config import (
    ENABLE_LOCAL_EXPLANATION,
    LOCAL_EXPLANATION_MODEL
)

from prompts import EXPLAIN_PROMPT


# ============================================================
# LOCAL MODEL
# ============================================================

_local_pipeline = None


def local_explanation(topic: str):

    global _local_pipeline

    if _local_pipeline is None:

        from transformers import pipeline

        _local_pipeline = pipeline(
            "text2text-generation",
            model=LOCAL_EXPLANATION_MODEL
        )

    prompt = f"""
Explain this educational topic simply.

Topic:
{topic}

Include:

1. Definition
2. Explanation
3. Example
4. Key points
"""

    result = _local_pipeline(
        prompt,
        max_new_tokens=300,
        do_sample=False
    )

    return result[0][
        "generated_text"
    ].strip()


# ============================================================
# MAIN EXPLANATION FUNCTION
# ============================================================

def explain_topic(topic: str):

    # Try local model if enabled
    if ENABLE_LOCAL_EXPLANATION:

        try:

            return local_explanation(
                topic
            )

        except Exception:

            # If local model fails,
            # automatically use Gemini.
            pass


    # Gemini fallback/default
    prompt = EXPLAIN_PROMPT.format(
        topic=topic
    )

    return generate_text(
        prompt,
        max_output_tokens=1400
    )