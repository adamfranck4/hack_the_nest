"""Voice budget (API_CONTRACT v1.2): daily ElevenLabs credit pacing guard."""
from datetime import datetime, timezone

import pytest

from app import budget, config

LIMIT_MSG = "Today's voice limit is reached — type your reply instead."


@pytest.fixture(autouse=True)
def clean_budget(monkeypatch):
    """No env limit by default, ElevenLabs 'configured', budget reset before/after."""
    monkeypatch.delenv("VOICE_DAILY_CREDIT_LIMIT", raising=False)
    monkeypatch.setattr(config, "elevenlabs_configured", lambda: True)
    budget.reset()
    yield
    budget.reset()


def set_limit(monkeypatch, value):
    monkeypatch.setenv("VOICE_DAILY_CREDIT_LIMIT", str(value))


def text_turn(client, sid, text="hello"):
    return client.post(f"/api/sessions/{sid}/turns", data={"text": text})


def audio_turn(client, sid):
    return client.post(f"/api/sessions/{sid}/turns",
                       files={"audio": ("a.webm", b"bytes", "audio/webm")})


# --- unlimited -------------------------------------------------------------
def test_unset_limit_is_unlimited(client, fakes, new_session):
    s = new_session()
    assert s["voice_available"] is True
    assert s["opening"]["audio_b64"]
    h = client.get("/api/health").json()
    assert h["voice_available"] is True
    assert h["voice_credits_left_today"] is None
    fakes.reply = "x" * 5000
    for _ in range(3):
        r = text_turn(client, s["session_id"])
        assert r.status_code == 200
        assert r.json()["reply_audio_b64"]
        assert r.json()["voice_available"] is True
    assert audio_turn(client, s["session_id"]).status_code == 200


@pytest.mark.parametrize("val", ["", "   ", "abc", "1.5", "10k"])
def test_empty_or_bad_limit_means_unlimited(client, monkeypatch, new_session, val):
    set_limit(monkeypatch, val)
    s = new_session()
    assert s["voice_available"] is True
    assert s["opening"]["audio_b64"]
    h = client.get("/api/health")
    assert h.status_code == 200
    assert h.json()["voice_credits_left_today"] is None
    assert h.json()["voice_available"] is True


# --- TTS gating ------------------------------------------------------------
def test_tts_skipped_when_over_limit(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 150)
    fakes.reply = "a" * 60
    s = new_session()
    budget.reset()
    fakes.calls["tts"].clear()
    sid = s["session_id"]

    r = text_turn(client, sid)  # 0 + 60 <= 150 -> spoken
    assert r.json()["reply_audio_b64"]
    assert len(fakes.calls["tts"]) == 1
    r = text_turn(client, sid)  # 60 + 60 <= 150 -> spoken
    assert r.json()["reply_audio_b64"]
    assert budget.credits_left() == 30
    r = text_turn(client, sid)  # 120 + 60 > 150 -> skipped
    assert r.status_code == 200
    assert r.json()["reply_audio_b64"] is None
    assert len(fakes.calls["tts"]) == 2  # fake TTS not called for skipped one
    assert budget.credits_left() == 30  # skipped call costs nothing


def test_exact_limit_boundary_allowed(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 150)
    s = new_session()
    budget.reset()
    fakes.reply = "a" * 150  # used + len == limit is allowed
    r = text_turn(client, s["session_id"])
    assert r.json()["reply_audio_b64"]
    assert budget.credits_left() == 0


def test_failed_tts_does_not_consume_budget(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 150)
    s = new_session()
    budget.reset()
    fakes.reply = "a" * 100
    fakes.tts_error = True
    r = text_turn(client, s["session_id"])
    assert r.status_code == 200 and r.json()["reply_audio_b64"] is None
    assert budget.credits_left() == 150
    fakes.tts_error = False
    r = text_turn(client, s["session_id"])  # still fits since nothing was spent
    assert r.json()["reply_audio_b64"]
    assert budget.credits_left() == 50


def test_session_opening_skipped_when_too_long_for_limit(client, fakes, monkeypatch):
    set_limit(monkeypatch, 1)  # any opening line is longer than 1 char
    r = client.post("/api/sessions", json={"character_id": "toddler"})
    assert r.status_code == 201
    assert r.json()["opening"]["audio_b64"] is None
    assert fakes.calls["tts"] == []
    assert budget.credits_left() == 1


def test_stt_cost_counted_on_success(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 1000)
    s = new_session()
    budget.reset()
    fakes.reply = "a" * 10
    r = audio_turn(client, s["session_id"])
    assert r.status_code == 200
    assert budget.credits_left() == 1000 - 100 - 10


def test_failed_stt_does_not_consume_budget(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 1000)
    s = new_session()
    budget.reset()
    fakes.stt_error = True
    assert audio_turn(client, s["session_id"]).status_code == 502
    assert budget.credits_left() == 1000


# --- audio turn 429 --------------------------------------------------------
def test_audio_turn_429_when_cannot_cover_stt(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 150)
    s = new_session()
    budget.reset()
    budget.spend(51)  # 51 + 100 > 150
    r = audio_turn(client, s["session_id"])
    assert r.status_code == 429
    assert r.json() == {"detail": LIMIT_MSG}
    assert fakes.calls["stt"] == []
    assert fakes.calls["reply"] == []
    # typed turns still work
    r = text_turn(client, s["session_id"])
    assert r.status_code == 200
    assert r.json()["voice_available"] is False


def test_audio_turn_ok_at_exact_boundary(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 150)
    s = new_session()
    budget.reset()
    budget.spend(50)  # 50 + 100 == 150
    assert audio_turn(client, s["session_id"]).status_code == 200
    assert len(fakes.calls["stt"]) == 1


def test_text_wins_over_audio_no_stt_call(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 150)
    s = new_session()
    budget.reset()
    budget.spend(100)
    r = client.post(f"/api/sessions/{s['session_id']}/turns", data={"text": "hi"},
                    files={"audio": ("a.webm", b"bytes", "audio/webm")})
    assert r.status_code == 200
    assert fakes.calls["stt"] == []


# --- voice_available flag / health ----------------------------------------
def test_voice_available_flags_and_health(client, fakes, monkeypatch, new_session):
    set_limit(monkeypatch, 500)
    s = new_session()
    assert isinstance(s["voice_available"], bool)
    budget.reset()
    h = client.get("/api/health").json()
    assert h["voice_available"] is True
    assert h["voice_credits_left_today"] == 500
    fakes.reply = "a" * 100
    r = text_turn(client, s["session_id"]).json()
    assert r["voice_available"] is True  # 100 used, 400 left
    assert client.get("/api/health").json()["voice_credits_left_today"] == 400
    budget.spend(350)  # 50 left < 100
    r = text_turn(client, s["session_id"]).json()
    assert r["voice_available"] is False
    h = client.get("/api/health").json()
    assert h["voice_available"] is False
    assert h["voice_credits_left_today"] < 100


def test_credits_left_never_negative(client, monkeypatch):
    set_limit(monkeypatch, 10)
    budget.spend(500)
    assert client.get("/api/health").json()["voice_credits_left_today"] == 0


def test_voice_unavailable_without_elevenlabs_key(client, monkeypatch, new_session):
    monkeypatch.setattr(config, "elevenlabs_configured", lambda: False)
    assert new_session()["voice_available"] is False
    assert client.get("/api/health").json()["voice_available"] is False


# --- limit 0 ---------------------------------------------------------------
def test_zero_limit_voice_off(client, fakes, monkeypatch):
    set_limit(monkeypatch, 0)
    h = client.get("/api/health").json()
    assert h["voice_available"] is False
    assert h["voice_credits_left_today"] == 0
    r = client.post("/api/sessions", json={"character_id": "toddler"})
    assert r.status_code == 201
    b = r.json()
    assert b["voice_available"] is False
    assert b["opening"]["audio_b64"] is None
    sid = b["session_id"]
    t = text_turn(client, sid)
    assert t.status_code == 200
    assert t.json()["reply_audio_b64"] is None
    assert t.json()["voice_available"] is False
    a = audio_turn(client, sid)
    assert a.status_code == 429 and a.json()["detail"] == LIMIT_MSG
    assert fakes.calls["tts"] == [] and fakes.calls["stt"] == []


# --- day rollover ----------------------------------------------------------
def test_day_rollover_resets_counter(monkeypatch):
    set_limit(monkeypatch, 200)

    class FakeDT:
        now_value = datetime(2026, 1, 1, 23, 59, tzinfo=timezone.utc)

        @classmethod
        def now(cls, tz=None):
            return cls.now_value

    monkeypatch.setattr(budget, "datetime", FakeDT)
    budget.spend(150)
    assert budget.credits_left() == 50
    assert budget.voice_available() is False
    FakeDT.now_value = datetime(2026, 1, 2, 0, 1, tzinfo=timezone.utc)
    assert budget.credits_left() == 200
    assert budget.voice_available() is True


def test_budget_state_does_not_leak_between_tests(monkeypatch):
    set_limit(monkeypatch, 100)
    assert budget.credits_left() == 100
