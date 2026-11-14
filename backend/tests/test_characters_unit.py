import json
from pathlib import Path

import pytest

from app.characters import get_character, list_characters


IDS = ["toddler", "angry_caller", "upset_friend", "teen", "roommate", "coworker"]


def test_six_characters():
    chars = list_characters()
    assert [c.id for c in chars] == IDS


def test_ids_unique_and_voice_ids_nonempty():
    chars = list_characters()
    ids = [c.id for c in chars]
    assert len(ids) == len(set(ids))
    for c in chars:
        assert isinstance(c.voice_id, str) and c.voice_id.strip()


@pytest.mark.parametrize("cid", IDS)
def test_each_character_valid(cid):
    c = get_character(cid)
    assert c is not None and c.id == cid
    assert 16 <= c.start_mood <= 99
    assert len(c.techniques) > 0 and all(t for t in c.techniques)
    assert len(c.bad_moves) > 0 and all(b for b in c.bad_moves)
    assert len(c.starter_suggestions) == 2
    assert all(s.strip() and len(s.split()) <= 20 for s in c.starter_suggestions)
    assert isinstance(c.voice_id, str) and c.voice_id.strip()
    assert c.meter_label and c.meter_label.strip()


def test_character_fields_valid():
    for c in list_characters():
        assert 0 <= c.start_mood <= 100
        assert 15 < c.start_mood < 100, "must not start already won/lost"
        assert len(c.techniques) > 0 and all(t for t in c.techniques)
        assert c.voice_id and c.opening_line and c.persona_prompt and c.name
        assert len(c.bad_moves) > 0


def test_get_character():
    assert get_character("nope") is None
    assert get_character("toddler").id == "toddler"


def test_static_demo_catalog_matches_live_characters(client):
    from app.characters import demo_catalog

    path = Path(__file__).resolve().parents[2] / "frontend" / "characters.json"
    demo = json.loads(path.read_text(encoding="utf-8"))
    assert demo == demo_catalog(), "Run python backend/scripts/export_demo_characters.py"
    assert [entry["character"] for entry in demo["characters"]] == client.get(
        "/api/characters"
    ).json()["characters"]
    assert all(entry["opening"]["text"] for entry in demo["characters"])
    assert "voice_id" not in path.read_text(encoding="utf-8")
    assert "persona_prompt" not in path.read_text(encoding="utf-8")
