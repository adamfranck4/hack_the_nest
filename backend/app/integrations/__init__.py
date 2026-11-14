"""External service clients (Gemini, ElevenLabs)."""
import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[3]


class IntegrationError(Exception):
    """Raised for any failure talking to an external service."""


def get_env(name: str, default: str | None = None, required: bool = False) -> str | None:
    """Read an env var, loading the repo-root .env if it is not already set."""
    value = os.environ.get(name)
    if not value:
        load_dotenv(REPO_ROOT / ".env", override=False)
        value = os.environ.get(name)
    if not value:
        if required:
            raise IntegrationError(f"{name} is not configured")
        return default
    return value
