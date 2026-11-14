# Documentation

Start with the [project overview, architecture, setup, and validation](../README.md).
Use the [API contract](API_CONTRACT.md) for endpoints, game rules, configuration,
and deployment details. Supporting documents are grouped by purpose below.

## Submission

| Document | What it explains |
|---|---|
| [Submission copy](submission/DEVPOST_DRAFT.md) | Prepared project description and AI-tool disclosure for team review |
| [Demo readiness](submission/DEMO_READINESS.md) | Rehearsal checks and fallback behavior |

## Coordination

| Document | What it explains |
|---|---|
| [Shared instructions](../AGENTS.md) | Required synchronization, ownership, privacy, and transparency rules |
| [Team decisions](coordination/TEAM_DECISIONS.md) | Roster, selected tracks, accepted scope, and remaining decisions |
| [Agent roles](coordination/AGENT_ROLES.md) | Shared manager/worker responsibilities |
| [Agent handoffs](coordination/AGENT_HANDOFFS.md) | Dated task ownership, changes, validation, and operational history |

Claude Code enters through [CLAUDE.md](../CLAUDE.md), with platform metadata in
[`.claude/agents/`](../.claude/agents/). Codex role entries are in
[`.codex/agents/`](../.codex/agents/); runtime registration is unverified.
[GEMINI.md](../GEMINI.md) is guidance for a possible future coding-agent connection,
separate from the app's Gemini API integration.

## Hackathon

- [Hackathon context](hackathon/HACKATHON_CONTEXT.md): sourced event facts and official
  submission/judging requirements, with verification labels.
- [Track assessment](hackathon/TRACK_ASSESSMENT.md): dated analysis and recommendations,
  not accepted product decisions or an organizer's scoring rubric.

Keep accepted choices in team decisions, rules in the shared instructions, and
task outcomes in handoffs. Historical entries describe what was known at the
time; their test counts and verification status are not automatically current.
