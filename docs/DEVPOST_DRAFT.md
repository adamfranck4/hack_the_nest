# Devpost draft: Talk It Out

**DRAFT. Fill in and verify after the build.**

Deadlines (Eastern, see [event schedule](HACKATHON_CONTEXT.md#critical-deadlines)):
draft due **12:00 AM Sunday, Nov 15** on Devpost AND the event app; final
submission **12:00 PM Sunday, Nov 15**. The event-specific Devpost URL has not
been supplied yet.

Everything marked `VERIFY` must be checked against the running app before pasting.

## Project name

Talk It Out

## Tagline (under 200 characters)

A conversation gym: practice hard conversations by voice with AI characters, calm them down, and get a scorecard on the techniques you used.

## Inspiration

Pilots practice in simulators. Why do we practice hard conversations for the
first time on real people? Calming a toddler, de-escalating an angry customer, or
apologizing to a hurt friend, or setting a limit with a teenager are skills, but there is nowhere safe to rehearse
them. We wanted a place to fail privately and try again.

## What it does

You pick a character and talk to it by mic (or typing). Gemini plays the
character in real time. ElevenLabs gives it a voice and transcribes you. A live
mood meter moves based on the communication techniques you use, such as naming
feelings, offering choices, sincere apology, and taking ownership.

- Six characters, each with its own meter: Milo the toddler refusing his shoes
  (Meltdown meter), Dana the angry customer whose order arrived broken for the
  third time (Anger meter), Jordan the friend whose birthday you forgot (Hurt
  meter), Riley the teenager caught on their phone at 1 AM (Eye-roll meter), Sam
  the roommate fed up with your dirty dishes (Tension meter), and Casey the
  coworker who presented your idea as theirs in a meeting (Defensiveness meter).
- Live "Try saying" suggestion chips help when you are stuck; a Hints toggle
  turns them off.
- A daily voice budget protects the public demo: when it runs out, characters
  go text-only and typed input remains available.
- Win by getting the meter to 15 or below. Lose at 100. You have 8 turns.
- A scorecard shows a score, which techniques you used, your best line, your
  worst line, and a better alternative for the worst one.

## How we built it

- Python FastAPI backend serving both the API and the frontend from one origin.
- Gemini REST API plays the character and returns the reply, a mood change, the
  techniques detected, and a coaching note each turn. A second call writes the
  scorecard.
- ElevenLabs REST API for text-to-speech (character voice) and speech-to-text
  (your microphone).
- React 18 loaded from a CDN with `htm` templates, so there is no build step.
- Sessions held in memory. Typed input is a fallback for noisy rooms.
- Tests with pytest.

<!-- VERIFY after build: pytest suite exists and passes; typed fallback works -->

## Challenges we ran into

- The Google and ElevenLabs Python SDKs would not install on Python 3.14 on
  Windows ARM64 (a dependency had no wheel), so we call both REST APIs directly
  with `httpx`.
- Node was not installed, so we built the React frontend with no build step,
  using ES modules from a CDN and `htm` instead of JSX.
- Designing believable mood scoring. The model had to reward real techniques,
  punish threats and dismissiveness, and not swing wildly from turn to turn.
- Getting browser microphone audio, transcription and playback to work together
  in a smooth turn-by-turn loop.

<!-- VERIFY after build: add any real challenges that came up during the build (latency, audio format, prompt tuning) and remove any that did not -->

## Accomplishments that we're proud of

- A working end-to-end voice loop: you speak, the character answers aloud, and
  the meter moves.
- Most of us had never done a hackathon before.
- The scorecard turns a fun game into feedback you can actually learn from.

<!-- VERIFY after build: confirm the voice loop works end to end; add real numbers (rounds played, latency) if we have them -->

## What we learned

- How to call REST APIs directly when SDKs are not an option.
- How to prompt an LLM to act as a character and also produce structured scoring.
- Keeping scope small and getting one flow working beats building many features.
- Working as a team of three with shared documents and clear file ownership.

## What's next for Talk It Out

- More scenario packs: a relative with dementia, de-escalation training.
- Custom characters you design yourself.
- Difficulty levels.
- Progress history so you can see yourself improve.
- Who it is for: new parents, babysitters, customer-service training, and
  education and nursing students.

## Built with

python, fastapi, uvicorn, httpx, gemini-api, google-gemini, elevenlabs, react, htm, javascript, html5, css3, pytest, web-audio

<!-- VERIFY after build: trim this list to what the final code actually uses -->

## Tracks

AI/ML, Best Beginner, Best use of ElevenLabs (confirm all three are selected in
the event app). Also eligible for MLH Best Use of Gemini API.

## Team

Adam Franck (captain), Gavin Robbins, Nolan Drake. Grand Valley State University.

## Links to add

- Live demo (Try it out): <https://talk-it-out-0dzk.onrender.com>
- Code: <https://github.com/adamfranck4/hack_the_nest>
- Demo video: TODO after recording (shot list in [DEMO_SCRIPT.md](DEMO_SCRIPT.md))
- Screenshots: TODO (character select, meter mid-round, scorecard)
