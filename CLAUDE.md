# Claude Code project guidance

Read [AGENTS.md](AGENTS.md) and
[docs/HACKATHON_CONTEXT.md](docs/HACKATHON_CONTEXT.md). Follow the shared
collaboration rules and preserve the event reference's verification labels.

**Required for every participating agent and account:** Before starting any task or
resuming edits, inspect Git state, fetch from GitHub, and synchronize with the
intended remote branch as described in AGENTS.md. Commit and push completed work
before every completion report or handoff, and verify the remote contains it.
Fetch again before pushing; safely reconcile concurrent changes without
overwriting work or force-pushing. Report any synchronization blocker explicitly.

Multiple Codex agents from different accounts may be editing this repository
simultaneously; Gemini may join later but is not confirmed connected. Use distinct
session labels and coordinate ownership with each agent, as described in AGENTS.md.
Do not assume shared chat history, checkouts, or credentials. Inspect Git state before
changes, agree on file ownership and shared interfaces, and avoid overwriting
files being edited by any other agent. Coordinate branch switches in a shared checkout;
prefer separate branches and focused commits when practical. Preserve existing
application behavior, architecture, conventions, and other agents' changes.
Run relevant tests for application changes and never expose or commit secrets.
Maintain a working project ahead of the Sunday noon Eastern deadline.

Preserve and follow the existing Claude-specific team and role instructions in
`.claude/agents/` and the existing `.claude/settings.json`. This file adds shared
context and coordination guidance without replacing those instructions. Keep
event details in the shared context document rather than duplicating them here.
