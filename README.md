# hack_the_nest

Project for Hack The Nest 2026 at Eastern Michigan University, November 14–15, 2026.

> Status: repo scaffold only. The idea, stack and setup steps get filled in once the build starts.

## Shared context and collaboration

- [Hackathon context](docs/HACKATHON_CONTEXT.md): event rules, deadlines, tracks,
  prizes, logistics, and verification status. All event times are Eastern
  (`America/Detroit`).
- [Team decisions](docs/TEAM_DECISIONS.md): our team, chosen tracks and why.
- [Shared agent instructions](AGENTS.md): file ownership, Git safety, and required
  GitHub synchronization for all agents, including Codex sessions from different accounts.
- [Claude Code instructions](CLAUDE.md): entry point for Claude-specific guidance.
- [Gemini instructions](GEMINI.md): entry point if Gemini joins; no connection is
  currently confirmed.

All agents must sync with GitHub before work and push completed changes before
handoff, following AGENTS.md. The draft submission is due Sunday, November 15,
at 12:00 AM; final submission is due that Sunday at 12:00 PM (noon), Eastern.

## What it does

_To be written: the problem and the one-sentence pitch._

## Getting started

_To be written: install and run commands._

There is no application, dependency manifest, or test suite yet. `.env.example`
currently declares no variables. Once required variables are documented, copy it
to `.env` and fill in the values. Never commit `.env`.

## Tech stack

_To be decided._

## Working with the agent team

Multiple Codex agents from different accounts and Claude Code may collaborate on
this repo, with a possible future Gemini connection. Each session must identify
itself and coordinate ownership using AGENTS.md. Claude Code is configured to use
the `manager` agent in [.claude/agents](.claude/agents), which splits a goal into
tasks and hands them to five workers. The manager includes the shared instructions
in worker briefs and coordinates Git operations for workers sharing its checkout:

| Agent | Owns |
|---|---|
| `manager` | Planning, delegation, checking results |
| `frontend` | UI, pages, components, styling |
| `backend` | Server, API routes, business logic, auth |
| `data-integrations` | Database schema, seed data, third-party APIs |
| `qa-tester` | Tests, running the app, bug reports |
| `docs-demo` | README, demo script, pitch material |

Give the manager a goal, for example: "build the MVP for <idea> with login and a dashboard".

## Team

_Add names here._
