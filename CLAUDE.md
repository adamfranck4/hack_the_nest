# Claude Code project guidance

Read [AGENTS.md](AGENTS.md) and
[docs/HACKATHON_CONTEXT.md](docs/HACKATHON_CONTEXT.md). Follow the shared
collaboration rules and preserve the event reference's verification labels.

Codex may be editing this repository simultaneously. Inspect Git state before
changes, agree on file ownership and shared interfaces, and avoid overwriting
files being edited by Codex. Coordinate branch switches in a shared checkout;
prefer separate branches and focused commits when practical. Preserve existing
application behavior, architecture, conventions, and other agents' changes.
Run relevant tests for application changes and never expose or commit secrets.
Maintain a working project ahead of the Sunday noon Eastern deadline.

Preserve and follow the existing Claude-specific team and role instructions in
`.claude/agents/` and the existing `.claude/settings.json`. This file adds shared
context and coordination guidance without replacing those instructions. Keep
event details in the shared context document rather than duplicating them here.
