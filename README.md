# Talk It Out

A conversation gym. Practice hard conversations by voice with AI characters
before you have them with real people.

Built at Hack The Nest 2026 (Eastern Michigan University, November 14-15, 2026).

**Live demo:** <https://talk-it-out-0dzk.onrender.com> (free hosting: the first visit after
idle can take 30-60 seconds to wake up; voice is limited per day, typed input remains available).

> Pilots practice in simulators. Why do we practice hard conversations for the
> first time on real people?

## The problem

Most of us never rehearse the conversations that matter: calming a toddler
mid-meltdown, de-escalating an angry customer, apologizing to a hurt friend,
setting a limit with a teenager, or asking a coworker for credit.
There is no safe place to try, fail, and try again.

## What it does

Pick a character, talk to it, and try to calm it down.

| Character | Situation | Meter |
|---|---|---|
| Milo, a toddler | Refuses to put his shoes on | Meltdown meter |
| Dana, an angry caller | Her order arrived broken for the third time | Anger meter |
| Jordan, an upset friend | You forgot their birthday | Hurt meter |
| Riley, a teenager | You caught them on their phone at 1 AM on a school night | Eye-roll meter |
| Sam, an annoyed roommate | You keep leaving dirty dishes in the sink | Tension meter |
| Casey, a credit-taking coworker | They presented your idea as their own in a meeting | Defensiveness meter |

While you play, live "Try saying" suggestion chips offer ideas for your next line.
A Hints toggle turns them off if you want a harder round.

## How it works

- You speak into your mic (or type). ElevenLabs transcribes your voice.
- Gemini plays the character and replies in character. ElevenLabs speaks the reply aloud.
- Each turn Gemini moves a live mood meter based on the techniques you used:
  naming feelings, offering choices, a sincere apology, taking ownership, and so on.
- Calm the character to 15 or below to win. At 100 you lose. You get 8 turns.
- A scorecard grades your techniques and shows your best line, your worst line,
  and a better alternative for the worst one.


## Quick start

Use the repository root. Python is required; Node.js is not required to run the
app. Preserve an existing `.env`; otherwise copy `.env.example` using the commands
below. For real conversations, enter `GEMINI_API_KEY` and `ELEVENLABS_API_KEY`
privately. Optional settings and defaults are in
[the build contract](docs/API_CONTRACT.md#env-vars-repo-root-env-git-ignored-names-only-here).
Get keys from [Google AI Studio](https://aistudio.google.com) and
[ElevenLabs](https://elevenlabs.io); never commit their values.

### Windows (PowerShell)

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
backend/.venv/Scripts/python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

### macOS / Linux

```bash
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
test -f .env || cp .env.example .env
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Open <http://localhost:8000>. Allow microphone access or type your reply. Keep the
terminal running; Ctrl+C stops the server. Health/key-presence and voice-budget
status are available at `/api/health` (key presence does not verify API access).
If the voice budget runs out, typed input remains available.

### Simulated demo (no keys)

Use `?mock=1` on the local or live URL. It simulates replies and scorecards without
calling Gemini or ElevenLabs; it does not provide real speech transcription or
spoken replies. Add `&novoice=1` to exercise the exhausted-voice UI. The demo uses
the same scenario catalog, opening lines, hints, and early-ending labels as the
real app. Ending a round early displays **Ended early**, not Out of turns.

## Validation and demo data

Run the backend suite with your virtual environment's interpreter:

```bash
backend/.venv/bin/python -m pytest backend/tests
```

On Windows, use `backend/.venv/Scripts/python` instead. Frontend API regression
checks use Node 22+ and its built-in runner (Node is optional for app use):

```bash
node --test frontend/tests/api.test.mjs
```

Character definitions are authoritative in `backend/app/characters.py`. After
changing them, regenerate the committed static demo catalog:

```bash
python3 backend/scripts/export_demo_characters.py
```

On Windows, use `python` instead. Do not edit `frontend/characters.json` manually.
The backend suite checks catalog parity; no build step or API keys are needed
for export or the mocked tests. Live API and microphone checks must be reported
separately from these automated checks.

## Tech stack

- Backend: Python, FastAPI, Uvicorn, `httpx`
- AI: Gemini (REST) for character, mood scoring and scorecard
- Voice: ElevenLabs (REST) for text-to-speech and speech-to-text
- Frontend: React 18 loaded from a CDN with `htm` templates, no build step
- State: in-memory sessions (reset on server restart)

We call both APIs directly over REST because the Google and ElevenLabs Python
SDKs would not install on our Python 3.14 ARM64 machine.

## Team and tracks

Roster and confirmed/pending track choices are maintained in
[team decisions](docs/TEAM_DECISIONS.md). Event category and eligibility details
remain in [the event reference](docs/HACKATHON_CONTEXT.md).

## What's next

More scenario packs (relative with dementia, de-escalation training),
custom characters, difficulty levels, and progress history. Use cases: new
parents, babysitters, customer-service training, education and nursing students.

## Demo and submission

- [Demo script](docs/DEMO_SCRIPT.md): 3-minute table demo and 2-minute video shot list
- [Devpost draft](docs/DEVPOST_DRAFT.md): submission text

## Shared references

| Document | Contents |
|---|---|
| [Hackathon context](docs/HACKATHON_CONTEXT.md) | Rules, deadlines, tracks, prizes, logistics, verification status |
| [Team decisions](docs/TEAM_DECISIONS.md) | Team roster, selected tracks, rationale, open decisions |
| [Build contract](docs/API_CONTRACT.md) | App API, module interfaces, folder ownership, run commands |
| [Agent handoffs](docs/AGENT_HANDOFFS.md) | Current ownership, input/status history, blockers |
| [Shared agent instructions](AGENTS.md) | Mandatory workflow and organization rules for all agents/accounts |
| [Agent roles](docs/AGENT_ROLES.md) | Manager and worker responsibilities |
| [Claude guidance](CLAUDE.md) / [Gemini guidance](GEMINI.md) | Platform entry points |

## Agent entry points

Claude Code selects its manager through `.claude/settings.json` and defines
roles in `.claude/agents/`. Codex role files are in `.codex/agents/`; their
registration/activation in the current runtime is unverified. Gemini is a
possible future participant, not a confirmed connection. These files share
responsibilities through the role reference rather than maintaining separate
copies of team policy.
