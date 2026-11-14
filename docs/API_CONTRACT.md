# Talk It Out — build contract

Authoritative contract for the app build: folder layout, file ownership, API
routes and payloads, Python module interfaces, and env var names. The current
task coordinator records interface changes here; delegated workers report needed
changes instead of editing around it. Initial build ownership below is historical
guidance; current assignments are recorded in agent handoffs. Project rationale lives in
[TEAM_DECISIONS.md](TEAM_DECISIONS.md).

## What the app does

A "conversation gym": pick one of the characters defined in `backend/app/characters.py`,
talk to it by voice, and try to calm it down. Gemini plays the character and
moves a **mood meter**; ElevenLabs gives it a voice and transcribes you. At the
end a scorecard grades the communication techniques you used.

## Stack and run

- Backend: Python, FastAPI + Uvicorn, `httpx` for all external calls. The original
  Windows ARM64/Python 3.14 machine could not install the provider SDKs; REST
  clients remain the supported implementation. Render uses the Python version
  pinned in `render.yaml`.
- Frontend: React 18.3.1 with **no build step**. Native
  ES modules loaded from `https://esm.sh/react@18.3.1`,
  `https://esm.sh/react-dom@18.3.1/client` and `https://esm.sh/htm@3.1.1`;
  components written with `htm` tagged templates instead of JSX.
- One origin: FastAPI serves `/api/*` and serves `frontend/` as static files at
  `/`. Open <http://localhost:8000>.
- Setup, run, and validation commands: [README](../README.md#quick-start).

## Env vars (repo-root `.env`, git-ignored; names only here)

| Name | Required | Use |
|---|---|---|
| `GEMINI_API_KEY` | yes | Gemini REST, header `x-goog-api-key` |
| `ELEVENLABS_API_KEY` | yes | ElevenLabs REST, header `xi-api-key` |
| `GEMINI_MODEL` | no | default `gemini-flash-lite-latest` (falls back to `gemini-3.5-flash`) |
| `VOICE_DAILY_CREDIT_LIMIT` | no | daily ElevenLabs budget in estimated credits; unset/empty = unlimited (local dev); `0` = voice off. Render sets it. |

Never put key values in URLs, logs, code, tests or docs.

## Folder layout and ownership

| Path | Owner |
|---|---|
| `backend/requirements.txt`, `backend/app/__init__.py`, `backend/app/main.py`, `backend/app/config.py`, `backend/app/sessions.py` | backend |
| `backend/app/characters.py`, `backend/app/integrations/` (`__init__.py`, `gemini.py`, `elevenlabs.py`), `backend/scripts/` | data-integrations |
| `frontend/` | frontend |
| `backend/tests/` | qa-tester |
| `README.md`, `docs/DEMO_SCRIPT.md`, `docs/DEVPOST_DRAFT.md` | docs-demo |
| `.env.example`, this file, `docs/TEAM_DECISIONS.md`, `docs/AGENT_HANDOFFS.md`, shared-checkout Git operations | current task coordinator |

Delegated workers do not run `git add/commit/push/checkout` in a shared checkout;
their coordinator does. Independent sessions/checkouts still follow AGENTS.md.

## Python interfaces (data-integrations → backend)

`backend/app/characters.py`

```python
@dataclass(frozen=True)
class Character:
    id: str            # "toddler" | "angry_caller" | "upset_friend" | "teen" | "roommate" | "coworker"
    name: str          # e.g. "Milo"
    emoji: str
    title: str         # e.g. "Toddler"
    scenario: str      # 1-2 sentences shown to the player
    goal: str          # what the player must achieve
    meter_label: str   # e.g. "Meltdown meter"
    start_mood: int    # 0-100, higher = more upset
    voice_id: str      # ElevenLabs voice id
    opening_line: str  # first line the character says
    starter_suggestions: tuple[str, ...]  # exactly 2 example first replies for the player
    persona_prompt: str
    techniques: tuple[str, ...]  # good techniques that calm this character
    bad_moves: tuple[str, ...]   # things that make it worse

def list_characters() -> list[Character]: ...
def get_character(character_id: str) -> Character | None: ...
def public_character(character: Character) -> dict: ...  # CharacterPublic below
def demo_catalog() -> dict: ...  # safe, generated static demo data
```

`frontend/characters.json` is generated from these definitions, not edited by
hand. The export command and parity checks are documented in
[README](../README.md#validation-and-demo-data). It includes public character
fields and opening lines/hints; voice IDs and persona prompts are excluded.

`backend/app/integrations/__init__.py` defines `class IntegrationError(Exception)`.
All integration functions raise `IntegrationError` (never return error dicts) on
missing keys, HTTP errors, timeouts or unparseable model output.

`backend/app/integrations/gemini.py`

```python
History = list[dict]  # [{"role": "user" | "character", "text": str}, ...] oldest first

def character_reply(character: Character, history: History, user_text: str, mood: int) -> dict:
    """Returns {"reply": str, "mood_delta": int (clamped -25..25),
    "techniques": list[str] (subset of character.techniques used in user_text),
    "note": str (one short coaching hint for the player),
    "suggestions": list[str] (exactly 2 things the player could say NEXT, each <= 20 words,
    each using a different technique from character.techniques; [] if the model omits them)}"""

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

## Voice budget (v1.2)

Protects the ElevenLabs free monthly quota on the public deploy. Owned by backend
(`backend/app/budget.py`).

- In-memory counter of estimated credits used per **UTC day**; resets at UTC
  midnight and on server restart (Render free restarts after idle). It is a pacing
  guard, not a hard guarantee — the hard cap is the ElevenLabs key's own usage
  limit set in the ElevenLabs dashboard.
- Cost estimate: TTS = `len(text)` credits; STT = 100 credits per call.
- Reserve estimated credits atomically before each external call, including
  simultaneous TTS/STT requests. In-flight calls count against available credits.
  Successful calls keep their charge; failures refund it. A failed call from a
  previous day must not refund credits from the new day.
- If TTS cannot reserve `len(text)`, skip it (`audio_b64: null`).
- Audio turn (no `text`) unable to reserve 100 credits → **429** `{"detail": "Today's
  voice limit is reached — type your reply instead."}`; STT is not called.
- `voice_available` = limit unset, or `used + 100 <= limit` (and key configured).
- `POST /api/sessions` (201) and `POST .../turns` (200) responses gain
  `"voice_available": bool` (evaluated after the call). The UI hides the mic and
  shows a small "Voice paused for today — typing still works" notice when false.

## HTTP API

Errors use FastAPI's default body `{"detail": "<message>"}`.

`CharacterPublic` = `{id, name, emoji, title, scenario, goal, meter_label, start_mood}`

| Method & path | Request | Success | Errors |
|---|---|---|---|
| `GET /api/health` | — | `200 {"status": "ok", "gemini": bool, "elevenlabs": bool, "voice_available": bool, "voice_credits_left_today": int \| null}` (null = unlimited) | — |
| `GET /api/characters` | — | `200 {"characters": [CharacterPublic]}` | — |
| `POST /api/sessions` | JSON `{"character_id": str}` | `201 {"session_id", "character": CharacterPublic, "mood", "status": "active", "turn": 0, "max_turns": 8, "opening": {"text", "audio_b64": str \| null, "suggestions": [str]}}` (suggestions = `character.starter_suggestions`) | 404 unknown character |
| `POST /api/sessions/{id}/turns` | `multipart/form-data`: `audio` file (optional, browser webm/ogg) and/or `text` field (optional); at least one | `200 {"turn", "user_text", "reply_text", "reply_audio_b64": str \| null, "mood", "mood_delta", "techniques": [str], "note", "suggestions": [str], "status", "max_turns"}` (suggestions pass through from Gemini; `[]` when status is not `active`) | 404 session, 409 not active, 422 neither field / empty transcript, 502 Gemini or STT failure |
| `GET /api/sessions/{id}/scorecard` | — | `200 {"outcome": "ended" \| "won" \| "lost" \| "timeout", "final_mood", "score", "summary", "techniques_used", "best_line", "worst_line", "transcript": [{"role", "text"}]}` | 404 session, 409 zero turns, 502 Gemini failure |

- If `text` is given it wins over `audio` (typed fallback for noisy rooms).
- TTS failure never fails a request: return `audio_b64: null` and the text.
- Early scorecards report `ended` ("Ended early") in real and mock modes; the
  read-only GET does not mutate game status. Natural game outcomes stay unchanged.
- Session creation and turn responses also contain `voice_available: bool` as
  described in the budget section; that field is the UI's microphone availability.
- **Suggestions (v1.1):** the UI shows the current 2 suggestions as "Try saying" chips under the
  latest character line; clicking one fills the text box (does not auto-send). A "Hints" toggle
  (default on) hides them.
- Audio is mp3, base64; the frontend plays `data:audio/mpeg;base64,<b64>`.

## Deploy (Render free tier)

`render.yaml` at the repo root is a Render Blueprint: one long-running Python web
service (not serverless — sessions live in memory, so the app must be a single
process). Render runs `pip install -r backend/requirements.txt` and
`uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`, health check
`/api/health`, auto-deploys on every push to `main`. `GEMINI_API_KEY` and
`ELEVENLABS_API_KEY` are entered in the Render dashboard (`sync: false`), never
committed. Free instances sleep after ~15 min idle; first request takes ~30-60 s.
