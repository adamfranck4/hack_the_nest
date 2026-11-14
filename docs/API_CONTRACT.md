# Talk It Out — build contract

Authoritative contract for the app build: folder layout, file ownership, API
routes and payloads, Python module interfaces, and env var names. Change it only
through the coordinator (claude-manager session); workers report needed changes
instead of editing around it. Project rationale lives in
[TEAM_DECISIONS.md](TEAM_DECISIONS.md).

## What the app does

A "conversation gym": pick an AI character (toddler, angry caller, upset friend),
talk to it by voice, and try to calm it down. Gemini plays the character and
moves a **mood meter**; ElevenLabs gives it a voice and transcribes you. At the
end a scorecard grades the communication techniques you used.

## Stack and run

- Backend: Python 3.14 (Windows ARM64), FastAPI + Uvicorn, `httpx` for all
  external calls. **Do not add `google-genai` or the `elevenlabs` SDK**: their
  dependency `cryptography` has no wheel for this machine. Call both REST APIs
  directly with `httpx`.
- Frontend: React 18.3.1 with **no build step** (Node is not installed). Native
  ES modules loaded from `https://esm.sh/react@18.3.1`,
  `https://esm.sh/react-dom@18.3.1/client` and `https://esm.sh/htm@3.1.1`;
  components written with `htm` tagged templates instead of JSX.
- One origin: FastAPI serves `/api/*` and serves `frontend/` as static files at
  `/`. Open <http://localhost:8000>.
- Venv: `backend/.venv` (git-ignored). From the repo root:

```bash
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
backend/.venv/Scripts/python -m uvicorn app.main:app --app-dir backend --reload --port 8000
backend/.venv/Scripts/python -m pytest backend/tests
```

## Env vars (repo-root `.env`, git-ignored; names only here)

| Name | Required | Use |
|---|---|---|
| `GEMINI_API_KEY` | yes | Gemini REST, header `x-goog-api-key` |
| `ELEVENLABS_API_KEY` | yes | ElevenLabs REST, header `xi-api-key` |
| `GEMINI_MODEL` | no | default `gemini-flash-lite-latest` (falls back to `gemini-3.5-flash`) |

Never put key values in URLs, logs, code, tests or docs.

## Folder layout and ownership

| Path | Owner |
|---|---|
| `backend/requirements.txt`, `backend/app/__init__.py`, `backend/app/main.py`, `backend/app/config.py`, `backend/app/sessions.py` | backend |
| `backend/app/characters.py`, `backend/app/integrations/` (`__init__.py`, `gemini.py`, `elevenlabs.py`), `backend/scripts/` | data-integrations |
| `frontend/` | frontend |
| `backend/tests/` | qa-tester |
| `README.md`, `docs/DEMO_SCRIPT.md`, `docs/DEVPOST_DRAFT.md` | docs-demo |
| `.env.example`, this file, `docs/TEAM_DECISIONS.md`, `docs/AGENT_HANDOFFS.md`, all Git operations | coordinator (claude-manager) |

Workers do not run `git add/commit/push/checkout`; the coordinator does.

## Python interfaces (data-integrations → backend)

`backend/app/characters.py`

```python
@dataclass(frozen=True)
class Character:
    id: str            # "toddler" | "angry_caller" | "upset_friend"
    name: str          # e.g. "Milo"
    emoji: str
    title: str         # e.g. "Toddler"
    scenario: str      # 1-2 sentences shown to the player
    goal: str          # what the player must achieve
    meter_label: str   # e.g. "Meltdown meter"
    start_mood: int    # 0-100, higher = more upset
    voice_id: str      # ElevenLabs voice id
    opening_line: str  # first line the character says
    persona_prompt: str
    techniques: tuple[str, ...]  # good techniques that calm this character
    bad_moves: tuple[str, ...]   # things that make it worse

def list_characters() -> list[Character]: ...
def get_character(character_id: str) -> Character | None: ...
```

`backend/app/integrations/__init__.py` defines `class IntegrationError(Exception)`.
All integration functions raise `IntegrationError` (never return error dicts) on
missing keys, HTTP errors, timeouts or unparseable model output.

`backend/app/integrations/gemini.py`

```python
History = list[dict]  # [{"role": "user" | "character", "text": str}, ...] oldest first

def character_reply(character: Character, history: History, user_text: str, mood: int) -> dict:
    """Returns {"reply": str, "mood_delta": int (clamped -25..25),
    "techniques": list[str] (subset of character.techniques used in user_text),
    "note": str (one short coaching hint for the player)}"""

def score_session(character: Character, history: History, final_mood: int, outcome: str) -> dict:
    """Returns {"score": int 0-100, "summary": str,
    "techniques_used": [{"name": str, "count": int}],
    "best_line": {"text": str, "why": str} | None,
    "worst_line": {"text": str, "why": str, "better": str} | None}"""
```

`backend/app/integrations/elevenlabs.py`

```python
def text_to_speech(text: str, voice_id: str) -> bytes: ...  # mp3 bytes
def speech_to_text(audio: bytes, filename: str, content_type: str) -> str: ...
```

The backend calls these **through the module** (`from app.integrations import
gemini, elevenlabs` then `gemini.character_reply(...)`) so tests can monkeypatch
`app.integrations.gemini.character_reply` etc.

## Game rules (backend)

- New session starts at `character.start_mood`; `max_turns = 8`.
- Each turn: `mood = clamp(mood + mood_delta, 0, 100)`.
- `mood <= 15` → `"won"`; `mood >= 100` → `"lost"`; turn 8 reached otherwise →
  `"timeout"`. Else `"active"`.
- Sessions live in memory (dict keyed by uuid4 hex). Lost on restart; that's fine.

## HTTP API

Errors use FastAPI's default body `{"detail": "<message>"}`.

`CharacterPublic` = `{id, name, emoji, title, scenario, goal, meter_label, start_mood}`

| Method & path | Request | Success | Errors |
|---|---|---|---|
| `GET /api/health` | — | `200 {"status": "ok", "gemini": bool, "elevenlabs": bool}` (bools = key configured) | — |
| `GET /api/characters` | — | `200 {"characters": [CharacterPublic]}` | — |
| `POST /api/sessions` | JSON `{"character_id": str}` | `201 {"session_id", "character": CharacterPublic, "mood", "status": "active", "turn": 0, "max_turns": 8, "opening": {"text", "audio_b64": str \| null}}` | 404 unknown character |
| `POST /api/sessions/{id}/turns` | `multipart/form-data`: `audio` file (optional, browser webm/ogg) and/or `text` field (optional); at least one | `200 {"turn", "user_text", "reply_text", "reply_audio_b64": str \| null, "mood", "mood_delta", "techniques": [str], "note", "status", "max_turns"}` | 404 session, 409 not active, 422 neither field / empty transcript, 502 Gemini or STT failure |
| `GET /api/sessions/{id}/scorecard` | — | `200 {"outcome": status, "final_mood", "score", "summary", "techniques_used", "best_line", "worst_line", "transcript": [{"role", "text"}]}` | 404 session, 409 zero turns, 502 Gemini failure |

- If `text` is given it wins over `audio` (typed fallback for noisy rooms).
- TTS failure never fails a request: return `audio_b64: null` and the text.
- Audio is mp3, base64; the frontend plays `data:audio/mpeg;base64,<b64>`.
