import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(BASE_DIR / ".env")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'fitbuddy.db'}",
)


GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    "",
).strip()


GEMINI_WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.8-flash",
).strip()


GEMINI_TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-3.8-flash",
).strip()


ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "admin123",
).strip()


MAX_FEEDBACK_LENGTH = int(
    os.getenv(
        "MAX_FEEDBACK_LENGTH",
        "1500",
    )
)