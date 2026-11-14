"""ElevenLabs REST client (text-to-speech and speech-to-text) via httpx."""
import httpx

from . import IntegrationError, get_env

BASE = "https://api.elevenlabs.io/v1"
TTS_MODEL = "eleven_flash_v2_5"
STT_MODEL = "scribe_v1"


def _headers() -> dict:
    return {"xi-api-key": get_env("ELEVENLABS_API_KEY", required=True)}


def text_to_speech(text: str, voice_id: str) -> bytes:
    """Return mp3 bytes for `text` spoken in `voice_id`."""
    if not text or not text.strip():
        raise IntegrationError("text_to_speech: empty text")
    try:
        r = httpx.post(
            f"{BASE}/text-to-speech/{voice_id}",
            params={"output_format": "mp3_44100_128"},
            headers=_headers(),
            json={"text": text, "model_id": TTS_MODEL},
            timeout=30,
        )
    except httpx.HTTPError as e:
        raise IntegrationError(f"ElevenLabs TTS request failed: {type(e).__name__}") from e
    if r.status_code != 200 or not r.content:
        raise IntegrationError(f"ElevenLabs TTS error {r.status_code}: {r.text[:200]}")
    return r.content


def speech_to_text(audio: bytes, filename: str, content_type: str) -> str:
    """Transcribe audio bytes; returns the transcript (may be empty string)."""
    if not audio:
        raise IntegrationError("speech_to_text: empty audio")
    try:
        r = httpx.post(
            f"{BASE}/speech-to-text",
            headers=_headers(),
            data={"model_id": STT_MODEL},
            files={"file": (filename or "audio.webm", audio, content_type or "application/octet-stream")},
            timeout=45,
        )
    except httpx.HTTPError as e:
        raise IntegrationError(f"ElevenLabs STT request failed: {type(e).__name__}") from e
    if r.status_code != 200:
        raise IntegrationError(f"ElevenLabs STT error {r.status_code}: {r.text[:200]}")
    try:
        return (r.json().get("text") or "").strip()
    except ValueError as e:
        raise IntegrationError("ElevenLabs STT returned invalid JSON") from e
