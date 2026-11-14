"""Environment configuration. Loads the repo-root .env; never exposes key values."""
import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = REPO_ROOT / "frontend"

load_dotenv(REPO_ROOT / ".env")


def gemini_configured() -> bool:
    return bool(os.getenv("GEMINI_API_KEY", "").strip())


def elevenlabs_configured() -> bool:
    return bool(os.getenv("ELEVENLABS_API_KEY", "").strip())
