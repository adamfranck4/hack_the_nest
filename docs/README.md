# Documentation

Start with the [project overview, architecture, setup, and validation](../README.md).
This index keeps technical references, submission preparation, and development
records easy to find without mixing their purposes.

## For reviewers

| Document | What it explains |
|---|---|
| [API contract](API_CONTRACT.md) | Endpoints, payloads, game rules, configuration, and deployment |
| [Team decisions](TEAM_DECISIONS.md) | Team roster, selected tracks, accepted scope, and remaining decisions |
| [Submission copy](DEVPOST_DRAFT.md) | Prepared project description and AI-tool disclosure for team review |

The demo video is submitted separately. No recording script or video is stored
as part of this documentation update.

## For contributors

| Document | What it explains |
|---|---|
| [Shared instructions](../AGENTS.md) | Required synchronization, ownership, privacy, and transparency rules |
| [Agent roles](AGENT_ROLES.md) | Shared manager/worker responsibilities |
| [Agent handoffs](AGENT_HANDOFFS.md) | Dated task ownership, changes, validation, and operational history |
| [Demo readiness](DEMO_SCRIPT.md) | Rehearsal checks and fallback behavior |

Claude Code enters through [CLAUDE.md](../CLAUDE.md), with platform metadata in
[`.claude/agents/`](../.claude/agents/). Codex role entries are in
[`.codex/agents/`](../.codex/agents/); runtime registration is unverified.
[GEMINI.md](../GEMINI.md) is guidance for a possible future coding-agent connection,
separate from the app's Gemini API integration.

## Event and research records

- [Hackathon context](HACKATHON_CONTEXT.md): sourced event facts and official
  submission/judging requirements, with verification labels.
- [Track assessment](TRACK_ASSESSMENT.md): dated analysis and recommendations,
  not accepted product decisions or an organizer's scoring rubric.

Keep accepted choices in team decisions, rules in the shared instructions, and
task outcomes in handoffs. Historical entries describe what was known at the
time; their test counts and verification status are not automatically current.
