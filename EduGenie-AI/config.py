import os

from dotenv import load_dotenv


# Load .env
load_dotenv()


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "EduGenie"


# ============================================================
# GEMINI SETTINGS
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()


# ============================================================
# OPTIONAL LOCAL MODEL
# ============================================================

ENABLE_LOCAL_EXPLANATION = (
    os.getenv(
        "ENABLE_LOCAL_EXPLANATION",
        "false"
    ).lower()
    == "true"
)


LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
).strip()


# ============================================================
# GENERATION SETTINGS
# ============================================================

MAX_OUTPUT_TOKENS = int(
    os.getenv(
        "MAX_OUTPUT_TOKENS",
        "2048"
    )
)


TEMPERATURE = float(
    os.getenv(
        "TEMPERATURE",
        "0.4"
    )
)