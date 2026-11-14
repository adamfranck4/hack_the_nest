# Talk It Out

A conversation gym. Practice hard conversations by voice with AI characters
before you have them with real people.

Built at Hack The Nest 2026 (Eastern Michigan University, November 14-15, 2026).

**Live demo:** <https://talk-it-out-0dzk.onrender.com> (free hosting: the first visit after
idle can take 30-60 seconds to wake up; voice is limited per day, typing always works).

> Pilots practice in simulators. Why do we practice hard conversations for the
> first time on real people?

## The problem

Most of us never rehearse the conversations that matter: calming a toddler
mid-meltdown, de-escalating an angry customer, apologizing to a hurt friend.
There is no safe place to try, fail, and try again.

## What it does

Pick a character, talk to it, and try to calm it down.

| Character | Situation | Meter |
|---|---|---|
| Milo, a toddler | Refuses to put his shoes on | Meltdown |
| Angry caller | Their order arrived broken for the third time | Anger |
| Upset friend | You forgot their birthday | Hurt |

<!-- VERIFY after build: character names, scenarios and meter labels match backend/app/characters.py -->

## How it works

- You speak into your mic (or type). ElevenLabs transcribes your voice.
- Gemini plays the character and replies in character. ElevenLabs speaks the reply aloud.
- Each turn Gemini moves a live mood meter based on the techniques you used:
  naming feelings, offering choices, a sincere apology, taking ownership, and so on.
- Calm the character to 15 or below to win. At 100 you lose. You get 8 turns.
- A scorecard grades your techniques and shows your best line, your worst line,
  and a better alternative for the worst one.

<!-- VERIFY after build: win/lose thresholds, turn limit and scorecard fields in the running UI -->

## Quick start (Windows)

You need Python 3 and two API keys. No Node.js is required.

1. Get keys (free tiers are enough):
   - Gemini: [aistudio.google.com](https://aistudio.google.com)
   - ElevenLabs: [elevenlabs.io](https://elevenlabs.io)
2. From the repo root, create the virtual environment and install dependencies:

   ```powershell
   python -m venv backend/.venv
   backend/.venv/Scripts/python -m pip install -r backend/requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in the keys:

   ```powershell
   copy .env.example .env
   ```

   | Variable | Required | Purpose |
   |---|---|---|
   | `GEMINI_API_KEY` | yes | Gemini REST API |
   | `ELEVENLABS_API_KEY` | yes | ElevenLabs text-to-speech and speech-to-text |
   | `GEMINI_MODEL` | no | Defaults to `gemini-flash-latest` |

   Never commit `.env`. It is git-ignored.

4. Run the server:

   ```powershell
   backend/.venv/Scripts/python -m uvicorn app.main:app --app-dir backend --reload --port 8000
   ```

5. Open <http://localhost:8000>. Allow microphone access, or use the text box.

`GET /api/health` reports whether each key is configured.

Run the tests:

```powershell
backend/.venv/Scripts/python -m pytest backend/tests
```

<!-- VERIFY after build: every command above runs from a clean checkout; .env.example lists the variables -->

## Tech stack

- Backend: Python, FastAPI, Uvicorn, `httpx`
- AI: Gemini (REST) for character, mood scoring and scorecard
- Voice: ElevenLabs (REST) for text-to-speech and speech-to-text
- Frontend: React 18 loaded from a CDN with `htm` templates, no build step
- State: in-memory sessions (reset on server restart)

We call both APIs directly over REST because the Google and ElevenLabs Python
SDKs would not install on our Python 3.14 ARM64 machine.

## Team

Adam Franck (captain), Gavin Robbins, Nolan Drake. Grand Valley State University.
First hackathon for most of us.

Tracks: AI/ML, Best Beginner, Best use of ElevenLabs. Also eligible for MLH Best
Use of Gemini API. (Third track to be confirmed in the event app.
See [team decisions](docs/TEAM_DECISIONS.md#tracks).)

## What's next

More scenario packs (teen, relative with dementia, de-escalation training),
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
