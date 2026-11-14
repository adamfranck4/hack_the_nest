"""In-memory daily ElevenLabs credit budget (UTC day). See docs/API_CONTRACT.md."""
import os
import threading
from datetime import date, datetime, timezone

STT_COST = 100

_lock = threading.Lock()
_day: date | None = None
_used = 0


def limit() -> int | None:
    """Daily limit from env; None = unlimited (unset, empty or non-integer)."""
    raw = (os.environ.get("VOICE_DAILY_CREDIT_LIMIT") or "").strip()
    if not raw:
        return None
    try:
        return max(0, int(raw))
    except ValueError:
        return None


def _roll() -> None:
    """Reset the counter on a new UTC day. Caller holds the lock."""
    global _day, _used
    today = datetime.now(timezone.utc).date()
    if _day != today:
        _day, _used = today, 0


def can_spend(n: int) -> bool:
    lim = limit()
    if lim is None:
        return True
    with _lock:
        _roll()
        return _used + n <= lim


def spend(n: int) -> None:
    global _used
    with _lock:
        _roll()
        _used += n


def credits_left() -> int | None:
    lim = limit()
    if lim is None:
        return None
    with _lock:
        _roll()
        return max(0, lim - _used)


def voice_available() -> bool:
    return can_spend(STT_COST)


def reset() -> None:
    global _day, _used
    with _lock:
        _day, _used = None, 0
