"""Talk It Out FastAPI app: /api/* routes plus static frontend at /."""
import base64
import logging

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import characters, config, sessions
from app.integrations import IntegrationError, elevenlabs, gemini

log = logging.getLogger("talk_it_out")

app = FastAPI(title="Talk It Out")
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)


def character_public(c) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "emoji": c.emoji,
        "title": c.title,
        "scenario": c.scenario,
        "goal": c.goal,
        "meter_label": c.meter_label,
        "start_mood": c.start_mood,
    }


def tts_b64(text: str, voice_id: str):
    """TTS never fails a request: return None on any error."""
    try:
        return base64.b64encode(elevenlabs.text_to_speech(text, voice_id)).decode("ascii")
    except Exception as exc:  # noqa: BLE001 - audio is optional
        log.warning("TTS failed: %s", type(exc).__name__)
        return None


class SessionCreate(BaseModel):
    character_id: str


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "gemini": config.gemini_configured(),
        "elevenlabs": config.elevenlabs_configured(),
    }


@app.get("/api/characters")
def list_characters():
    return {"characters": [character_public(c) for c in characters.list_characters()]}


@app.post("/api/sessions", status_code=201)
def create_session(body: SessionCreate):
    character = characters.get_character(body.character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Unknown character")
    session = sessions.create_session(character)
    return {
        "session_id": session.id,
        "character": character_public(character),
        "mood": session.mood,
        "status": session.status,
        "turn": session.turn,
        "max_turns": sessions.MAX_TURNS,
        "opening": {
            "text": character.opening_line,
            "audio_b64": tts_b64(character.opening_line, character.voice_id),
        },
    }


def _require_session(session_id: str) -> sessions.Session:
    session = sessions.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown session")
    return session


@app.post("/api/sessions/{session_id}/turns")
def take_turn(
    session_id: str,
    audio: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
):
    session = _require_session(session_id)
    if session.status != "active":
        raise HTTPException(status_code=409, detail=f"Session is over ({session.status})")

    user_text = (text or "").strip()
    if not user_text:
        if audio is None or not audio.filename:
            raise HTTPException(status_code=422, detail="Provide 'text' or an 'audio' file")
        data = audio.file.read()
        if not data:
            raise HTTPException(status_code=422, detail="Audio file is empty")
        try:
            user_text = (
                elevenlabs.speech_to_text(
                    data, audio.filename or "audio.webm", audio.content_type or "audio/webm"
                )
                or ""
            ).strip()
        except IntegrationError as exc:
            raise HTTPException(status_code=502, detail=str(exc))
        if not user_text:
            raise HTTPException(status_code=422, detail="Could not hear anything; try again")

    character = session.character
    try:
        result = gemini.character_reply(
            character, list(session.history), user_text, session.mood
        )
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    reply_text = result["reply"]
    delta = int(result.get("mood_delta", 0))
    new_turn = session.turn + 1
    new_mood, status = sessions.apply_turn(session.mood, delta, new_turn)

    session.history.append({"role": "user", "text": user_text})
    session.history.append({"role": "character", "text": reply_text})
    session.mood, session.turn, session.status = new_mood, new_turn, status

    return {
        "turn": new_turn,
        "user_text": user_text,
        "reply_text": reply_text,
        "reply_audio_b64": tts_b64(reply_text, character.voice_id),
        "mood": new_mood,
        "mood_delta": delta,
        "techniques": list(result.get("techniques") or []),
        "note": result.get("note", ""),
        "status": status,
        "max_turns": sessions.MAX_TURNS,
    }


@app.get("/api/sessions/{session_id}/scorecard")
def scorecard(session_id: str):
    session = _require_session(session_id)
    if session.turn == 0:
        raise HTTPException(status_code=409, detail="No turns played yet")
    try:
        result = gemini.score_session(
            session.character, list(session.history), session.mood, session.status
        )
    except IntegrationError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {
        "outcome": session.status,
        "final_mood": session.mood,
        "score": result["score"],
        "summary": result["summary"],
        "techniques_used": result.get("techniques_used", []),
        "best_line": result.get("best_line"),
        "worst_line": result.get("worst_line"),
        "transcript": list(session.history),
    }


# Static frontend last so /api routes win.
if config.FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=config.FRONTEND_DIR, html=True), name="frontend")
