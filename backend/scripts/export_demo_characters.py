"""Refresh the committed, API-key-free demo catalog from app character definitions."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.characters import demo_catalog


if __name__ == "__main__":
    target = REPO_ROOT / "frontend" / "characters.json"
    target.write_text(json.dumps(demo_catalog(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {target.relative_to(REPO_ROOT)}")
