# Devpost submission copy

Prepared project text for the team's final review; this document does not mean
an entry has been submitted. Submit through the
[official event](https://hack-the-nest.devpost.com/) using the
[verified requirements](../hackathon/HACKATHON_CONTEXT.md#verified-devpost-submission-requirements).

## Project name

Talk It Out

## Tagline

A conversation gym: practice difficult conversations with AI characters and
review feedback on the communication techniques you used.

## Inspiration

Difficult conversations often happen before we have practiced them. Talk It Out
provides a low-stakes place to rehearse an apology, a disagreement, or a clear
request, then review what to try differently.

## What it does

Choose one of six scenarios, speak or type a reply, and see how the AI character
responds. A mood meter tracks the interaction, optional hints suggest replies,
and a scorecard summarizes techniques, examples, and alternatives. The transcript
lets the learner review the exchange before another attempt.

The live scenario definitions are maintained in
[the character catalog](../../backend/app/characters.py). Sessions have bounded
turns and explicit outcomes, including an early-ending report. Voice requests
share an atomic estimated-credit budget; typed input remains available when
voice is paused.

## How it is built

- React browser modules with `htm` templates; no frontend build step.
- Python FastAPI serving both the interface and API from one origin.
- Gemini REST calls for dialogue, mood changes, suggestions, and scorecards.
- ElevenLabs REST calls for transcription and character speech.
- In-memory session state and daily voice-credit reservations.
- Automated API, game-rule, concurrency, and mock/live catalog regression checks.

See the [architecture and code map](../../README.md#architecture-and-code-map) for
source entry points and the [API contract](../API_CONTRACT.md) for interfaces.

## Engineering choices

The original Windows ARM64 environment could not install the provider SDKs, so
both integrations use REST through `httpx`. Browser modules avoided a required
Node build toolchain. A generated demo catalog prevents scenario data from
splitting between mock and live modes. Atomic credit reservations prevent
simultaneous voice requests from overspending the estimated daily budget.

## Validation and limitations

The [handoffs](../coordination/AGENT_HANDOFFS.md) record automated and live checks separately.
Automated tests use fake integrations and do not validate paid services. A real
typed Gemini round and scorecard were verified; the team still needs to confirm
microphone capture/transcription and its recording setup on the actual device.

Sessions and counters reset on restart. Feedback is generated from the transcript,
not vocal tone, and scores are not validated measures of learning. Mock mode is
an explicitly labeled simulator with no real AI or speech calls.

## AI tools and contributions

Claude Code and OpenAI Codex assisted with implementation, documentation, tests,
review, and debugging. Gemini and ElevenLabs are runtime services with the roles
listed above. The team should confirm this account and provide each person's
actual contribution and learning before submission. No private prompts, key
values, credential files, or sensitive logs belong in the entry.

## Team and tracks

All three teammates are first-time hackathon attendees. The
[team record](../coordination/TEAM_DECISIONS.md) contains the roster and confirmed app
selections. Enter the corresponding main-track and applicable award entries in
Devpost. Provider conditions for AI/ML and any additional MLH entry remain
organizer-confirmation items; selection alone does not establish eligibility.

## Possible next steps

Custom scenarios, difficulty options, and practice history are possible future
work, not current features. Product recommendations are kept separately in
[the track assessment](../hackathon/TRACK_ASSESSMENT.md#product-priorities-recommendations-not-an-implementation-request).

## Links

- [Live app](https://talk-it-out-0dzk.onrender.com/)
- [Public repository](https://github.com/adamfranck4/hack_the_nest)

## Submission media

Submit the required video separately through Devpost; enter its checked URL and
other media directly in the submission form. Keep the video and private recording
script out of GitHub. Prepare requested narration privately in chat unless the
user explicitly authorizes publishing it. Use only actual, checked media.
