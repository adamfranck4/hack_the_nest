"""In-memory session store and game rules (plain functions, easy to test)."""
import uuid
from dataclasses import dataclass, field

MAX_TURNS = 8
WIN_MOOD = 15
LOSE_MOOD = 100


@dataclass
class Session:
    id: str
    character: object  # app.characters.Character
    mood: int
    turn: int = 0
    status: str = "active"
    history: list = field(default_factory=list)  # [{"role", "text"}]


_SESSIONS: dict[str, Session] = {}


def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, value))


def compute_status(mood: int, turn: int, max_turns: int = MAX_TURNS) -> str:
    if mood <= WIN_MOOD:
        return "won"
    if mood >= LOSE_MOOD:
        return "lost"
    if turn >= max_turns:
        return "timeout"
    return "active"


def apply_turn(mood: int, mood_delta: int, turn: int) -> tuple[int, str]:
    """Return (new_mood, status) after a turn; `turn` is the new turn number."""
    new_mood = clamp(mood + int(mood_delta))
    return new_mood, compute_status(new_mood, turn)


def create_session(character) -> Session:
    session = Session(
        id=uuid.uuid4().hex,
        character=character,
        mood=clamp(character.start_mood),
        history=[{"role": "character", "text": character.opening_line}],
    )
    _SESSIONS[session.id] = session
    return session


def get_session(session_id: str) -> Session | None:
    return _SESSIONS.get(session_id)


def clear_sessions() -> None:
    _SESSIONS.clear()
