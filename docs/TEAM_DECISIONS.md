# Team decisions

Team choices and strategy for Hack The Nest 2026. Event facts (rules, deadlines,
prize lists) live in [HACKATHON_CONTEXT.md](HACKATHON_CONTEXT.md); this file
records what *our team* decided and why. Update it when a decision changes.

Last updated: Saturday, November 14, 2026 (Claude Code manager session).

## Team

| Member | School | Role in app | Status |
|---|---|---|---|
| Adam Franck | Grand Valley State University | Captain | Checked in |
| Gavin Robbins | Grand Valley State University | Member | Checked in |
| Nolan Drake | Grand Valley State University | Member | Checked in |

We are a beginner team (first hackathon for most of us).

## Tracks (app allows up to 3)

| # | Track | Status |
|---|---|---|
| 1 | AI/ML | **Selected** in the event app |
| 2 | Best Beginner | **Selected** in the event app |
| 3 | Best use of ElevenLabs | **Recommended**; not yet confirmed as selected in the app |

### Why ElevenLabs for the third track

- Stacks with AI/ML: one project can qualify for both (voice AI is AI).
- Beginner-friendly: one API call adds text-to-speech, speech-to-text or a voice
  agent, leaving time for the core app.
- Demos well: a talking/listening app stands out at judging tables.
- Sponsor tracks usually draw fewer entries than broad tracks.
- Prizes (per HACKATHON_CONTEXT.md, unverified): 1st ElevenLabs Scale plan for
  3 months, 2nd Pro plan for 3 months.

### Alternatives considered

- **Computer Science Department** ($1,000 team scholarship, $250/member):
  highest-value prize, but judged on architecture, algorithms and code quality,
  which favours experienced teams. It is run by EMU's CS department and our team
  is from GVSU; **ask an organizer whether non-EMU students are eligible** before
  choosing it.
- **Best use of Base44**: rejected. Requires building inside Base44's no-code
  builder rather than our own code, and is judged by community vote.

## Implications for the build

- The project must clearly use AI/ML and should integrate the ElevenLabs API
  (voice input and/or output) as a visible part of the demo.
- Keep scope beginner-sized: a working end-to-end demo beats extra features.
- ElevenLabs API key goes in `.env` only (suggested name: `ELEVENLABS_API_KEY`,
  to be added to `.env.example` when the integration is built). Never commit keys.

## Open items

- Project idea: not chosen yet.
- Confirm the third track is actually selected in the app.
- Draft due on Devpost and the event app at **12:00 AM Sunday, Nov 15**; final
  submission due **12:00 PM Sunday** (Eastern).
