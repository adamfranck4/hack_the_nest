from app.characters import get_character, list_characters


def test_three_characters():
    chars = list_characters()
    assert {c.id for c in chars} == {"toddler", "angry_caller", "upset_friend"}


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
