# Team decisions

Team choices and strategy for Hack The Nest 2026. Event facts (rules, deadlines,
prize lists) live in [HACKATHON_CONTEXT.md](HACKATHON_CONTEXT.md); this file
records what *our team* decided and why. Update it when a decision changes.

Last updated: Saturday, November 14, 2026 (codex-review-fixes; aligned status with
the accepted project and six implemented scenarios; roster/track choices unchanged).

## Team

| Member | School | Role in app | Status |
|---|---|---|---|
| Adam Franck | Grand Valley State University | Captain | Checked in |
| Gavin Robbins | Grand Valley State University | Member | Checked in |
| Nolan Drake | Grand Valley State University | Member | Checked in |

We are a beginner team (first hackathon for most of us).

## Tracks

Selection rules and prizes are recorded in
[the event reference](HACKATHON_CONTEXT.md#selectable-tracks-in-the-official-app).

| # | Track | Status |
|---|---|---|
| 1 | AI/ML | **Selected** in the event app |
| 2 | Best Beginner | **Selected** in the event app |
| 3 | Best use of ElevenLabs | **Recommended**; not yet confirmed as selected in the app |

### Why ElevenLabs for the third track

Team rationale, not verified judging guidance: voice AI appears compatible with
the AI/ML focus and could support a manageable, visible demo. Ease of integration
depends on the project. The earlier suggestion that sponsor tracks draw
fewer entries is unverified; it is not an established event fact.

### Alternatives considered

- **Computer Science Department**: considered for its scholarship. The team
  perceived the engineering emphasis as potentially harder for beginners; no
  comparative difficulty or highest-value ranking is confirmed. Eligibility for
  non-EMU students remains unconfirmed; ask an organizer before choosing it.
- **Best use of Base44**: rejected based on the team's preference for writing its
  own code. The earlier claim that entry exclusively requires a no-code workflow
  has not been verified. Event-listed details remain in the reference document.

## Implications for the build

- The accepted project uses Gemini for character/scoring and ElevenLabs for
  speech. The ElevenLabs integration is implemented; third-track selection in
  the event app remains a separate, unconfirmed decision.
- Keep scope beginner-sized: a working end-to-end demo beats extra features.
- The ElevenLabs integration uses `ELEVENLABS_API_KEY`. Store the value using the
  [shared secret-handling rules](../AGENTS.md#collaboration-and-safety).

## Project (accepted by Adam, 2026-11-14)

**Talk It Out**: a "conversation gym" app where you practice hard conversations
by voice with AI characters and a live mood meter shows whether you are calming them down.
A scorecard grades the communication techniques used. Gemini plays the
characters and scores; ElevenLabs provides voices and speech-to-text.

Ideas considered and dropped: interview coach (too bland), single-character
toddler simulator (folded in as one character), financial-literacy game.

**Stack (accepted):** Python (FastAPI) backend + React frontend with no build
step. This originally accommodated a build machine without Node; Node is optional
for frontend regression checks, not required to run the app. Full contract and
ownership: [API_CONTRACT.md](API_CONTRACT.md).

API keys: Gemini (AI Studio, free tier) and ElevenLabs (restricted key, 8,000-credit
usage cap, no expiry) are stored in Adam's git-ignored `.env`; teammates need their own copy
shared privately.

## Open items

- Implemented scope: six scenarios; the catalog lives in
  `backend/app/characters.py`. Custom characters and difficulty levels remain stretch goals.
- Confirm the third track is actually selected in the app.
- Submission deadlines: see [the event schedule](HACKATHON_CONTEXT.md#critical-deadlines).
