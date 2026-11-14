# Talk It Out — track assessment

Assessment date: November 14, 2026. Code baseline: `70dcb25`. These are Codex's
recommendations, not organizer scoring weights or accepted team decisions.
Current selections/status remain in [TEAM_DECISIONS.md](../coordination/TEAM_DECISIONS.md#tracks).
Subsequent same-day updates confirm all three tracks selected and identify the
official Devpost event/rules. The verified five judging criteria and submission
requirements are recorded in [event context](HACKATHON_CONTEXT.md#verified-judging-requirements).

## Overall assessment

Best Beginner is the strongest present fit. Best Use of ElevenLabs is a credible
target if judges experience the real voice loop. AI/ML needs provider-eligibility
clarification and a more convincing account of scoring quality and originality.
There is no basis to assign win probabilities without the competing projects
and judges' comparisons.

| Track | Published basis | Current judging assessment |
|---|---|---|
| Best Beginner | Official site says most members must be first-timers and judging emphasizes growth/learning, not polish | Strong fit if the supplied beginner status is confirmed and the humans can explain their learning and decisions |
| Best Use of ElevenLabs | Official site highlights ideas that talk/listen, conversational agents, TTS and STT; game characters are an explicit example | Meaningful integration: character speech plus user transcription. Main uncertainty is the unverified live microphone loop and whether voice delivery makes the practice convincing |
| AI/ML | Website's differently named Future of Intelligence promotes OpenAI models and Exa search, useful agents/apps/tools and product polish | Gemini roleplay, structured feedback and stateful gameplay are implemented, but provider eligibility is unresolved and the general coaching concept is established elsewhere |

Published descriptions are in the [event context](HACKATHON_CONTEXT.md#independently-checked-track-descriptions).
Numerical judging weights remain unpublished in the reviewed material. The
entrant app's AI/ML wording must not be assumed identical to the website challenge.

## What I would ask as a judge

1. Who is the intended learner, and which difficult conversation can they rehearse?
2. What can this do beyond a generic roleplay prompt in a chatbot?
3. How does a score correspond to a communication skill or scenario outcome?
4. Can feedback point to exact player statements rather than plausible invented quotes?
5. Does speaking/listening materially change the experience, and can I try it now?
6. What did each participant learn, decide, and contribute, including use of AI agents?

These are an assessment framework, not additional eligibility rules. General
[MLH judging guidance](https://guide.mlh.com/general-information/judging-and-submissions/judging-plan)
also favors demonstrations and learning, but event-specific instructions take precedence.

## Best Beginner

The implemented app gives the team substantial learning material: a public
deployment, Python/React integration, structured model responses, audio handling,
mock/live parity, concurrent budgeting, and meaningful regression checks.
Prior validation includes 89 backend tests, four frontend checks, mobile/browser
flows and a real typed Gemini round; see [the handoff](../coordination/AGENT_HANDOFFS.md).

Those achievements help only if the participants understand and explain them.
All AI use was permitted in the supplied rules, so disclose Claude/Codex use
without presenting agent-written work as unaided human implementation. Each
member should be able to explain one technical problem, their contribution to
resolving it, and one thing they understand now that they did not before.

Confirm which members are first-timers; for a three-person team, a majority means
at least two. Do not describe the whole team as first-time hackers unless true.
Present the architecture and one bug/fix plainly rather than emphasizing code
volume or treating a test count as a prize criterion. Further cosmetic work has
less direct support from this track's published wording than the learning story.

## Best Use of ElevenLabs

ElevenLabs performs two substantive jobs: generating character speech and
transcribing the learner. Six voice identities and typed fallback are useful,
but a sponsor judge must hear a believable exchange, not just see API names.
The current integration is record/send/reply, not continuous streaming dialogue.

The deployment blueprint sets 300 estimated voice credits/day. The app reserves
100 per transcription; eight microphone turns need at least 800 before TTS.
Openings alone range from 34 to 88 estimated credits across the six characters.
Consequently the configured public pacing guard is not enough for a full voiced
eight-turn round. The counter is an estimate, not an ElevenLabs billing quote.

Before judging:

- Rehearse microphone recording, transcription and reply playback end to end on
  the actual laptop/browser. That microphone/STT path remains unverified by Codex.
- Plan enough demo/rehearsal quota within the service key's real limit. Prefer a
  controlled local/demo configuration rather than removing protection from the
  public site. Change settings explicitly and record them in the handoff.
- Audition voices for character fit and emotional delivery; show an angry and a
  calmer reply with appropriate speech. Measure end-to-end response time.
- Use headphones or a speaker arrangement tested in the room, and have a short
  real recorded backup. Label mock mode and recordings honestly.
- Warm the public site before judges arrive and coordinate a brief pause in
  pushes during the actual demo. Render auto-deploys can restart the process;
  sessions are in memory and are lost on restart.

[ElevenLabs TTS documentation](https://elevenlabs.io/docs/overview/capabilities/text-to-speech)
describes emotional cues, voice choices, and low-latency Flash v2.5. Its component
latency claims do not measure this app's upload, transcription, Gemini, and TTS
pipeline. Do not rush a model/SDK/streaming rewrite without a working rehearsal.
Custom voices and voice agents are listed capabilities, not verified mandatory
requirements for this prize.

## AI/ML

The useful AI work is a stateful practice loop: role-specific prompts, bounded
mood changes, validated technique names, generated hints, and a final debrief.
No reviewed criterion requires training a model from scratch. However, AI roleplay
and conversation coaching already exist: [VirtualSpeech](https://virtualspeech.com/)
and [Yoodli](https://yoodli.ai/) publicly describe roleplays and skill feedback.
Their existence is verified; their marketing effectiveness claims are not used as
evidence here. Do not pitch Talk It Out as the first AI conversation coach.

The biggest weakness is evidence behind the scoring. The same model roleplays
and evaluates, and its generated number is not an independent measurement of
learning. A successful 85/100 test demonstrated an operational integration, not
that a participant became better at real conversations.

Recommended improvement: a small, explicit rubric grounded in the transcript.
For each named skill, show an exact player turn/quote and a short explanation.
Verify quotes against stored history. Check a small set of expected good/bad
response pairs and report observed directional consistency without claiming a
clinical or educational validation study. Test whether irrelevant or score-changing
instructions can manipulate feedback; susceptibility is a test question, not a
confirmed exploit in this assessment.

Also distinguish de-escalation from task success. The present win condition uses
mood alone. Casey might sound calm without agreeing to correct the stolen credit.
A more meaningful debrief would separately assess communication technique,
scenario goal, and respect for boundaries. Do not imply that success means making
another person comply, or that the app clinically assesses users.

The model currently scores words from a transcript; it does not analyze vocal
tone, pitch, or volume. Do not claim that shouting versus speaking softly with
identical transcribed words is what changes the meter.

## Prioritized next steps

| Priority | Action | Why / completion evidence |
|---|---|---|
| First | Ask organizers whether the app's AI/ML award requires OpenAI and/or Exa | All three app selections are now confirmed; resolve provider eligibility before a port. Do not add decorative APIs or logos. |
| First | Rehearse a complete real voice round with an adequate, explicitly bounded demo budget | Essential evidence for the ElevenLabs story; microphone-to-audio recording works on the judging device |
| Next | Add a transcript-grounded skill rubric and explain task success separately from mood | Makes the AI feedback defensible; demonstrate exact evidence and several scoring sanity checks |
| Next | Lead the demo with one relatable adult scenario, then optionally show the toddler | Roommate/coworker practice gives a student audience a concrete use case without expanding the feature set |
| Next | Run a few short volunteer trials and ask what feedback they could use in a real conversation | Qualitative learning evidence; report the small sample honestly and obtain permission before publishing quotes |
| Before submission | Prepare a roughly 90–120 second live sequence plus a concise team-learning account and real backup video | Useful even if actual event slot length differs; follow the organizer's confirmed format |

Recommended demo sequence: problem and learner; scenario; contrasting unhelpful
and helpful wording; mood/feedback; evidence-grounded scorecard; each person's
learning/contribution. Keep model/provider roles explicit. Do not present mock
output as a live sponsor integration.

Defer more characters, accounts, databases, custom avatars, and a wholesale agent
framework migration. They do not address the largest current judging questions.
If provider changes are required, use them for real roleplay/coaching work and
rerun affected tests rather than adding a token integration.

## Product priorities (recommendations, not an implementation request)

1. **Evidence-backed coaching:** improve the scorecard's named skill assessments,
   exact player quotes, explanations, and one actionable next step. Existing
   technique tags and overall score are the starting point, not validation.
2. **A useful scenario outcome:** assess the practical goal separately from mood,
   such as correcting Casey's credit or agreeing a concrete dish plan with Sam.
3. **A repeat-practice loop:** let the learner retry a response in the same
   context, or restart with a specific skill goal and hints off. Make improvement
   visible without requiring accounts or a database.
4. **A dependable voice experience:** test a complete real microphone round,
   choose appropriate voices, reduce waiting, and plan enough bounded quota for
   a full session. Consider reviewing/editing transcription before grading so
   speech-recognition errors are not scored as communication errors.

These recommendations directly support working functionality, meaningful AI/
partner use, a clear user/problem, and quick usability in the now-published rubric.
The voice path currently sends recorded turns rather than streaming; the scoring
uses words, not vocal tone. Do not promise either capability without implementing it.

## Research limits and sources

- [Official EMU event](https://hackthenest.tech/#tracks): event identity and public
  descriptions for the three relevant tracks, checked November 14, 2026.
- [Official Devpost rules](https://hack-the-nest.devpost.com/rules): subsequently
  verified submission requirements, five criteria, and in-person judging schedule.
- [Entrant tracks](https://app.hackthenest.tech/tracks): team selections come from
  supplied shared context. This research session was redirected to login, so
  current signed-in provider conditions/selection state need confirmation.
- [MLH judging plan](https://guide.mlh.com/general-information/judging-and-submissions/judging-plan):
  general demonstration/learning guidance, not a replacement event rubric.
- [ElevenLabs TTS](https://elevenlabs.io/docs/overview/capabilities/text-to-speech):
  capabilities and model-level considerations, not event scoring weights.
- [VirtualSpeech](https://virtualspeech.com/) and [Yoodli](https://yoodli.ai/):
  evidence that the broad category exists, not hackathon competitors or judging criteria.

Prior sponsor-winner research remains unverified and was not used to infer what
this event's judges will reward. No app code, track selections, or runtime
settings were changed for this assessment, and no new paid AI calls were made.
Public track wording was read from the official site's shipped track data;
interactive track-card opening was not reliable in the research browser.
