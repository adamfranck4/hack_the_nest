# hack_the_nest

Project for Hack The Nest 2026 at Eastern Michigan University, November 14–15, 2026.

Status: repository scaffold. The project idea and stack are not chosen; there is
no application, dependency manifest, or test suite yet.

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

## Development status

Install/run commands and the project description will be documented when the
application exists. `.env.example` currently declares no variables; when needed,
use approved environment secret storage or ignored `.env` configuration as
specified in [AGENTS.md](AGENTS.md#collaboration-and-safety).

## Agent entry points

Claude Code selects its manager through `.claude/settings.json` and defines
roles in `.claude/agents/`. Codex role files are in `.codex/agents/`; their
registration/activation in the current runtime is unverified. Gemini is a
possible future participant, not a confirmed connection. These files share
responsibilities through the role reference rather than maintaining separate
copies of team policy.
