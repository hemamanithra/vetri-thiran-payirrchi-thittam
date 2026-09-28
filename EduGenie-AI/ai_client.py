from functools import lru_cache

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE
)


# ============================================================
# CHECK API CONFIGURATION
# ============================================================

def is_gemini_configured():

    return bool(
        GEMINI_API_KEY
    )


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        return None

    from google import genai

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    return client


# ============================================================
# GENERATE TEXT
# ============================================================

def generate_text(
    prompt: str,
    temperature: float = TEMPERATURE,
    max_output_tokens: int = MAX_OUTPUT_TOKENS
):

    client = get_client()

    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    try:

        from google.genai import types

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt,

            config=types.GenerateContentConfig(

                temperature=temperature,

                max_output_tokens=max_output_tokens

            )
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    except Exception as error:

        raise RuntimeError(
            f"Gemini API request failed: {error}"
        ) from error