# Demo readiness

Readiness checks and fallback guidance for the live demonstration.
[Submission media](DEVPOST_DRAFT.md#submission-media) has the video-handling instructions.
Submission limits, deadlines, and attendance requirements are maintained in
[the event reference](../hackathon/HACKATHON_CONTEXT.md#verified-devpost-submission-requirements).

## Before a real demonstration

- Start the service using the [local setup](../../README.md#run-locally), or open
  the public app early enough for the free host to wake.
- Check `/api/health` for configured-key presence and voice availability. These
  flags alone do not prove provider authentication or microphone functionality.
- On the actual recording/judging device, test microphone permission, recording,
  transcription, character playback, and scorecard generation.
- Confirm the recorder captures both the presenter and app audio by playing back
  a short test. Keep credentials, private tabs, and notifications out of view.
- Plan sufficient bounded voice quota for a full session. Public pacing limits
  are described in the [API contract](../API_CONTRACT.md#voice-budget-v12).
- Coordinate a pause in `main` pushes during the demonstration: Render can
  redeploy, and in-memory sessions reset when the process restarts.

## Accurate claims

Use the actual response, meter change, and score returned by the app. Model
outputs and response times vary. Do not promise a particular score or a win.
Scoring uses transcribed words, not vocal tone or volume; generated scores are
coaching feedback rather than validated measures of learning.

Mock mode is useful for reviewing the interface, but its responses and scores
are simulated. Label it clearly and use real mode when demonstrating live AI
and speech integration. Automated and live validation evidence belongs in
[the dated handoffs](../coordination/AGENT_HANDOFFS.md); complete the device-specific checks
above before claiming the full microphone path was verified.

## Fallbacks

| Condition | Response |
|---|---|
| Microphone unavailable or room too noisy | Use typed input and identify it as typed mode |
| Voice budget exhausted | Continue with typing; the UI explains voice availability |
| Character playback unavailable | Use the displayed reply text and acknowledge the audio issue |
| AI request fails | Use the retry control; if the service remains unavailable, use a real recorded backup |
| Service restarts | Start a new session; previous in-memory state cannot be recovered |
| Connectivity fails | Use a local copy of the recorded backup; the live app needs internet |

For the separately submitted video, verify duration and access against the
[official requirements](../hackathon/HACKATHON_CONTEXT.md#verified-devpost-submission-requirements).
Do not publish or describe a recording as completed until the team has checked
its exported file and judge-facing link.
