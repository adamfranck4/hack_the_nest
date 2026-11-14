import base64

import pytest

PUBLIC = {"id", "name", "emoji", "title", "scenario", "goal", "meter_label", "start_mood"}
IDS = ["toddler", "angry_caller", "upset_friend", "teen", "roommate", "coworker"]


def turn(client, sid, text="hello"):
    return client.post(f"/api/sessions/{sid}/turns", data={"text": text})


# 1. health / characters
def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    b = r.json()
    assert b["status"] == "ok"
    assert isinstance(b["gemini"], bool) and isinstance(b["elevenlabs"], bool)


def test_characters_public_only(client):
    r = client.get("/api/characters")
    assert r.status_code == 200
    chars = r.json()["characters"]
    assert [c["id"] for c in chars] == IDS
    for c in chars:
        assert set(c) == PUBLIC
    assert "persona_prompt" not in r.text and "voice_id" not in r.text


# 2. create session
@pytest.mark.parametrize("cid", IDS)
def test_create_session(client, cid):
    r = client.post("/api/sessions", json={"character_id": cid})
    assert r.status_code == 201
    b = r.json()
    assert b["session_id"]
    assert set(b["character"]) == PUBLIC
    assert b["character"]["id"] == cid
    assert b["mood"] == b["character"]["start_mood"]
    assert b["status"] == "active" and b["turn"] == 0 and b["max_turns"] == 8
    assert b["opening"]["text"]
    assert base64.b64decode(b["opening"]["audio_b64"]) == b"fake-mp3"


def test_create_session_unknown_character(client):
    assert client.post("/api/sessions", json={"character_id": "nope"}).status_code == 404


def test_create_session_tts_failure_still_201(client, fakes):
    fakes.tts_error = True
    r = client.post("/api/sessions", json={"character_id": "toddler"})
    assert r.status_code == 201
    assert r.json()["opening"]["audio_b64"] is None


def test_create_session_missing_body(client):
    assert client.post("/api/sessions", json={}).status_code == 422


# 3. turns
def test_turn_text_shape_and_passthrough(client, fakes, new_session):
    s = new_session()
    fakes.delta = -10
    fakes.techniques = ["validation"]
    fakes.note = "good"
    fakes.reply = "ok mommy"
    r = turn(client, s["session_id"], "I hear you")
    assert r.status_code == 200
    b = r.json()
    assert set(b) >= {"turn", "user_text", "reply_text", "reply_audio_b64", "mood",
                      "mood_delta", "techniques", "note", "status", "max_turns"}
    assert b["turn"] == 1 and b["user_text"] == "I hear you"
    assert b["reply_text"] == "ok mommy"
    assert base64.b64decode(b["reply_audio_b64"]) == b"fake-mp3"
    assert b["mood"] == s["mood"] - 10 and b["mood_delta"] == -10
    assert b["techniques"] == ["validation"] and b["note"] == "good"
    assert b["status"] == "active" and b["max_turns"] == 8


def test_turn_history_passed_to_gemini(client, fakes, new_session):
    s = new_session()
    turn(client, s["session_id"], "first")
    turn(client, s["session_id"], "second")
    _, history, user_text, mood = fakes.calls["reply"][1]
    assert user_text == "second"
    assert [h["role"] for h in history] == ["character", "user", "character"]


def test_mood_clamps_upper(client, fakes, new_session):
    s = new_session()
    fakes.delta = 25
    r = turn(client, s["session_id"]).json()
    assert r["mood"] == min(100, s["mood"] + 25)
    assert 0 <= r["mood"] <= 100


def test_mood_clamps_lower_and_bounds_always(client, fakes, new_session):
    s = new_session()
    fakes.delta = -25
    mood = s["mood"]
    for _ in range(8):
        r = turn(client, s["session_id"])
        if r.status_code == 409:
            break
        b = r.json()
        assert b["mood"] == max(0, min(100, mood - 25))
        mood = b["mood"]
        assert 0 <= mood <= 100


def test_text_wins_over_audio(client, fakes, new_session):
    s = new_session()
    r = client.post(f"/api/sessions/{s['session_id']}/turns",
                    data={"text": "typed"},
                    files={"audio": ("a.webm", b"audio", "audio/webm")})
    assert r.status_code == 200
    assert r.json()["user_text"] == "typed"
    assert fakes.calls["stt"] == []


def test_audio_only_uses_stt(client, fakes, new_session):
    s = new_session()
    r = client.post(f"/api/sessions/{s['session_id']}/turns",
                    files={"audio": ("a.webm", b"audio", "audio/webm")})
    assert r.status_code == 200
    assert r.json()["user_text"] == "transcribed words"
    assert fakes.calls["stt"][0][0] == b"audio"
    assert fakes.calls["reply"][0][2] == "transcribed words"


def test_empty_transcript_422(client, fakes, new_session):
    s = new_session()
    fakes.stt_text = "   "
    r = client.post(f"/api/sessions/{s['session_id']}/turns",
                    files={"audio": ("a.webm", b"audio", "audio/webm")})
    assert r.status_code == 422


# 4. game rules
def test_win(client, fakes, new_session):
    s = new_session()
    fakes.delta = -25
    b = {}
    for _ in range(8):
        b = turn(client, s["session_id"]).json()
        if b["status"] != "active":
            break
    assert b["status"] == "won" and b["mood"] <= 15
    assert turn(client, s["session_id"]).status_code == 409


def test_lose(client, fakes, new_session):
    s = new_session()
    fakes.delta = 25
    b = {}
    for _ in range(8):
        b = turn(client, s["session_id"]).json()
        if b["status"] != "active":
            break
    assert b["status"] == "lost" and b["mood"] >= 100
    assert turn(client, s["session_id"]).status_code == 409


def test_timeout_after_8_turns(client, fakes, new_session):
    s = new_session()
    fakes.delta = 0
    for i in range(1, 9):
        b = turn(client, s["session_id"]).json()
        assert b["turn"] == i
        assert b["status"] == ("active" if i < 8 else "timeout")
    assert turn(client, s["session_id"]).status_code == 409


def _land_on(client, fakes, s, target):
    mood, b = s["mood"], None
    while mood != target:
        fakes.delta = max(-25, min(25, target - mood))
        b = turn(client, s["session_id"]).json()
        mood = b["mood"]
        if mood != target:
            assert b["status"] == "active"
    return b


def test_mood_15_is_won(client, fakes, new_session):
    s = new_session()
    assert _land_on(client, fakes, s, 15)["status"] == "won"


def test_mood_16_is_not_won(client, fakes, new_session):
    s = new_session()
    assert _land_on(client, fakes, s, 16)["status"] == "active"


def test_mood_99_not_lost_and_100_lost(client, fakes, new_session):
    s = new_session()
    assert _land_on(client, fakes, s, 99)["status"] == "active"
    fakes.delta = 1
    assert turn(client, s["session_id"]).json()["status"] == "lost"


# 5. errors
def test_unknown_session_404(client):
    assert turn(client, "deadbeef").status_code == 404
    assert client.get("/api/sessions/deadbeef/scorecard").status_code == 404


def test_neither_text_nor_audio_422(client, new_session):
    s = new_session()
    assert client.post(f"/api/sessions/{s['session_id']}/turns").status_code == 422
    assert client.post(f"/api/sessions/{s['session_id']}/turns",
                       data={"text": ""}).status_code == 422


def test_gemini_failure_502_and_state_unchanged(client, fakes, new_session):
    s = new_session()
    fakes.gemini_error = True
    assert turn(client, s["session_id"]).status_code == 502
    fakes.gemini_error = False
    assert turn(client, s["session_id"]).json()["turn"] == 1


def test_stt_failure_502(client, fakes, new_session):
    s = new_session()
    fakes.stt_error = True
    r = client.post(f"/api/sessions/{s['session_id']}/turns",
                    files={"audio": ("a.webm", b"audio", "audio/webm")})
    assert r.status_code == 502
    assert "detail" in r.json()


def test_tts_failure_null_audio(client, fakes, new_session):
    s = new_session()
    fakes.tts_error = True
    r = turn(client, s["session_id"])
    assert r.status_code == 200
    assert r.json()["reply_audio_b64"] is None
    assert r.json()["reply_text"]


# 6. scorecard
def test_scorecard_zero_turns_409(client, new_session):
    s = new_session()
    assert client.get(f"/api/sessions/{s['session_id']}/scorecard").status_code == 409


def test_scorecard_shape(client, fakes, new_session):
    s = new_session()
    fakes.reply = "char reply"
    turn(client, s["session_id"], "my line")
    r = client.get(f"/api/sessions/{s['session_id']}/scorecard")
    assert r.status_code == 200
    b = r.json()
    assert set(b) >= {"outcome", "final_mood", "score", "summary", "techniques_used",
                      "best_line", "worst_line", "transcript"}
    assert b["outcome"] in {"active", "won", "lost", "timeout"}
    assert b["score"] == 77 and b["techniques_used"][0]["name"] == "validation"
    t = b["transcript"]
    assert t[0] == {"role": "character", "text": s["opening"]["text"]}
    assert t[1] == {"role": "user", "text": "my line"}
    assert t[2] == {"role": "character", "text": "char reply"}
    _, _, final_mood, outcome = fakes.calls["score"][0]
    assert final_mood == b["final_mood"] and outcome == b["outcome"]


def test_scorecard_gemini_failure_502(client, fakes, new_session):
    s = new_session()
    turn(client, s["session_id"])
    fakes.score_error = True
    assert client.get(f"/api/sessions/{s['session_id']}/scorecard").status_code == 502


# 6. reply suggestions
@pytest.mark.parametrize("cid", IDS)
def test_starter_suggestions_on_character(cid):
    from app import characters
    c = characters.get_character(cid)
    ss = c.starter_suggestions
    assert len(ss) == 2
    assert all(isinstance(s, str) and s.strip() and len(s.split()) <= 20 for s in ss)


@pytest.mark.parametrize("cid", IDS)
def test_opening_suggestions_match_character(client, new_session, cid):
    from app import characters
    s = new_session(cid)
    assert s["opening"]["suggestions"] == list(characters.get_character(cid).starter_suggestions)
    assert len(s["opening"]["suggestions"]) == 2


def test_turn_suggestions_passthrough(client, fakes, new_session):
    s = new_session()
    fakes.suggestions = ["A one", "B two"]
    assert turn(client, s["session_id"]).json()["suggestions"] == ["A one", "B two"]


def test_turn_suggestions_max_two(client, fakes, new_session):
    s = new_session()
    fakes.suggestions = ["a", "b", "c"]
    assert len(turn(client, s["session_id"]).json()["suggestions"]) <= 2


def test_turn_suggestions_missing_key_is_empty(client, fakes, new_session):
    s = new_session()
    fakes.suggestions = None
    r = turn(client, s["session_id"])
    assert r.status_code == 200
    assert r.json()["suggestions"] == []


@pytest.mark.parametrize("delta,final", [(-25, "won"), (25, "lost"), (0, "timeout")])
def test_turn_suggestions_empty_when_game_over(client, fakes, new_session, delta, final):
    s = new_session()
    fakes.delta = delta
    fakes.suggestions = ["x", "y"]
    b = {}
    for _ in range(8):
        b = turn(client, s["session_id"]).json()
        if b["status"] != "active":
            break
        assert b["suggestions"] == ["x", "y"]
    assert b["status"] == final
    assert b["suggestions"] == []
