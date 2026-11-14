import sys
from pathlib import Path

BACKEND = str(Path(__file__).resolve().parent.parent)
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

import pytest
from fastapi.testclient import TestClient

FAKE_MP3 = b"fake-mp3"


class Fakes:
    """Controllable stand-ins for the Gemini/ElevenLabs integrations."""

    def __init__(self):
        self.delta = 0
        self.techniques = []
        self.note = "try validating first"
        self.reply = "fake reply"
        self.stt_text = "transcribed words"
        self.calls = {"reply": [], "score": [], "tts": [], "stt": []}
        self.gemini_error = False
        self.score_error = False
        self.tts_error = False
        self.stt_error = False


@pytest.fixture
def fakes(monkeypatch):
    from app.integrations import IntegrationError, elevenlabs, gemini

    f = Fakes()

    def character_reply(character, history, user_text, mood):
        f.calls["reply"].append((character.id, list(history), user_text, mood))
        if f.gemini_error:
            raise IntegrationError("gemini down")
        return {"reply": f.reply, "mood_delta": f.delta,
                "techniques": list(f.techniques), "note": f.note}

    def score_session(character, history, final_mood, outcome):
        f.calls["score"].append((character.id, list(history), final_mood, outcome))
        if f.score_error:
            raise IntegrationError("gemini down")
        return {"score": 77, "summary": "Nice work.",
                "techniques_used": [{"name": "validation", "count": 2}],
                "best_line": {"text": "I hear you", "why": "validates"},
                "worst_line": {"text": "calm down", "why": "dismissive",
                               "better": "That sounds hard"}}

    def text_to_speech(text, voice_id):
        f.calls["tts"].append((text, voice_id))
        if f.tts_error:
            raise IntegrationError("tts down")
        return FAKE_MP3

    def speech_to_text(audio, filename, content_type):
        f.calls["stt"].append((audio, filename, content_type))
        if f.stt_error:
            raise IntegrationError("stt down")
        return f.stt_text

    monkeypatch.setattr(gemini, "character_reply", character_reply)
    monkeypatch.setattr(gemini, "score_session", score_session)
    monkeypatch.setattr(elevenlabs, "text_to_speech", text_to_speech)
    monkeypatch.setattr(elevenlabs, "speech_to_text", speech_to_text)
    return f


@pytest.fixture
def client(fakes):
    from app.main import app
    return TestClient(app)


@pytest.fixture
def new_session(client):
    def make(character_id="toddler"):
        r = client.post("/api/sessions", json={"character_id": character_id})
        assert r.status_code == 201, r.text
        return r.json()
    return make
