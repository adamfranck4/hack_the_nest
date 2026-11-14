"""Gemini REST client (character replies + session scoring) via httpx."""
import json

import httpx

from . import IntegrationError, get_env

BASE = "https://generativelanguage.googleapis.com/v1beta/models"
History = list[dict]
# gemini-flash-latest hung (>60s) during testing, so the default is the lite alias.
DEFAULT_MODEL = "gemini-flash-lite-latest"
FALLBACK_MODELS = ("gemini-3.5-flash", "gemini-flash-lite-latest")


def _call(system: str, prompt: str, schema: dict) -> dict:
    key = get_env("GEMINI_API_KEY", required=True)
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": schema,
            "temperature": 0.8,
        },
    }
    models = [get_env("GEMINI_MODEL", DEFAULT_MODEL)]
    for fb in FALLBACK_MODELS:
        if fb not in models:
            models.append(fb)
    last = "no attempt"
    r = None
    for model in models:
        try:
            r = httpx.post(
                f"{BASE}/{model}:generateContent",
                headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                json=body,
                timeout=15,
            )
        except httpx.HTTPError as e:
            last = f"request failed: {type(e).__name__}"
            r = None
            continue
        if r.status_code == 200:
            break
        last = f"error {r.status_code}: {r.text[:300]}"
        if r.status_code not in (404, 429, 500, 503, 504):
            break
        r = None
    if r is None or r.status_code != 200:
        raise IntegrationError(f"Gemini {last}")
    try:
        data = r.json()
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        out = json.loads(text)
    except (ValueError, KeyError, IndexError, TypeError) as e:
        raise IntegrationError("Gemini returned unparseable output") from e
    if not isinstance(out, dict):
        raise IntegrationError("Gemini returned unexpected JSON shape")
    return out


def _fmt_history(history: History, character) -> str:
    lines = []
    for h in history:
        who = "PLAYER" if h.get("role") == "user" else character.name.upper()
        lines.append(f"{who}: {h.get('text', '')}")
    return "\n".join(lines) or "(conversation just started)"


def _int(value, lo: int, hi: int, default: int = 0) -> int:
    try:
        return max(lo, min(hi, int(round(float(value)))))
    except (TypeError, ValueError):
        return default


def character_reply(character, history: History, user_text: str, mood: int) -> dict:
    system = (
        character.persona_prompt
        + "\n\nYou are also the hidden judge of a communication-skills game. The PLAYER is trying to"
        f" calm you down. Your current {character.meter_label} is {mood}/100 (higher = more upset)."
        f"\nGood techniques: {', '.join(character.techniques)}."
        f"\nBad moves: {', '.join(character.bad_moves)}."
        "\nFor the player's latest line output JSON with:"
        "\n- reply: your in-character spoken reply (1-3 short sentences), consistent with your new mood."
        "\n- mood_delta: integer from -25 to 25 (negative = calmer). A line that clearly uses one or"
        " more good techniques: -10 to -25 (skilled, specific, sincere = bigger drop). A mediocre or"
        " neutral line: -4 to +4. A line that uses bad moves: +8 to +25. Empty or irrelevant filler"
        " lines: 0 to +5."
        "\n- techniques: list of good technique names (exact strings from the list above) the"
        " player's latest line actually used; empty if none."
        "\n- note: one short coaching hint for the player (under 20 words), not spoken in character."
    )
    prompt = (
        f"Conversation so far:\n{_fmt_history(history, character)}\n\n"
        f"PLAYER'S LATEST LINE: {user_text}\n\nRespond with the JSON."
    )
    schema = {
        "type": "object",
        "properties": {
            "reply": {"type": "string"},
            "mood_delta": {"type": "integer"},
            "techniques": {"type": "array", "items": {"type": "string"}},
            "note": {"type": "string"},
        },
        "required": ["reply", "mood_delta", "techniques", "note"],
    }
    out = _call(system, prompt, schema)
    reply = str(out.get("reply") or "").strip()
    if not reply:
        raise IntegrationError("Gemini returned an empty reply")
    allowed = {t.lower(): t for t in character.techniques}
    techs = []
    for t in out.get("techniques") or []:
        canon = allowed.get(str(t).strip().lower())
        if canon and canon not in techs:
            techs.append(canon)
    return {
        "reply": reply,
        "mood_delta": _int(out.get("mood_delta"), -25, 25),
        "techniques": techs,
        "note": str(out.get("note") or "").strip(),
    }


def _line_obj(v, with_better: bool):
    if not isinstance(v, dict) or not str(v.get("text") or "").strip():
        return None
    res = {"text": str(v["text"]).strip(), "why": str(v.get("why") or "").strip()}
    if with_better:
        res["better"] = str(v.get("better") or "").strip()
    return res


def score_session(character, history: History, final_mood: int, outcome: str) -> dict:
    system = (
        "You are a warm, concise communication coach grading a practice conversation. The PLAYER"
        f" tried to calm {character.name} ({character.title}). Goal: {character.goal}"
        f"\nGood techniques: {', '.join(character.techniques)}."
        f"\nBad moves: {', '.join(character.bad_moves)}."
        "\nOutput JSON with: score (0-100 integer; weigh the final mood, technique use and avoiding"
        " bad moves; a 'won' outcome should usually be 70+, 'lost' under 45), summary (2-3"
        " encouraging sentences, second person), techniques_used (list of {name, count}, names"
        " exactly from the good-techniques list, count = number of player lines using it),"
        " best_line ({text: the player's exact line, why}) or null if there is no player line,"
        " worst_line ({text: the player's exact line, why, better: a rewritten version}) or null if"
        " no line was a real misstep."
    )
    prompt = (
        f"Outcome: {outcome}. Final {character.meter_label}: {final_mood}/100 (lower is better)."
        f"\n\nTranscript:\n{_fmt_history(history, character)}\n\nRespond with the JSON."
    )
    line = {"type": "object", "properties": {"text": {"type": "string"}, "why": {"type": "string"}},
            "required": ["text", "why"]}
    worst = {"type": "object", "properties": {"text": {"type": "string"}, "why": {"type": "string"},
             "better": {"type": "string"}}, "required": ["text", "why", "better"]}
    schema = {
        "type": "object",
        "properties": {
            "score": {"type": "integer"},
            "summary": {"type": "string"},
            "techniques_used": {"type": "array", "items": {"type": "object", "properties": {
                "name": {"type": "string"}, "count": {"type": "integer"}}, "required": ["name", "count"]}},
            "best_line": {**line, "nullable": True},
            "worst_line": {**worst, "nullable": True},
        },
        "required": ["score", "summary", "techniques_used"],
    }
    out = _call(system, prompt, schema)
    allowed = {t.lower(): t for t in character.techniques}
    counts: dict[str, int] = {}
    for item in out.get("techniques_used") or []:
        if not isinstance(item, dict):
            continue
        canon = allowed.get(str(item.get("name", "")).strip().lower())
        if canon:
            counts[canon] = counts.get(canon, 0) + max(1, _int(item.get("count"), 0, 99, 1))
    return {
        "score": _int(out.get("score"), 0, 100, 50),
        "summary": str(out.get("summary") or "").strip(),
        "techniques_used": [{"name": n, "count": c} for n, c in counts.items()],
        "best_line": _line_obj(out.get("best_line"), False),
        "worst_line": _line_obj(out.get("worst_line"), True),
    }
