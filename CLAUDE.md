# Claude Code project guidance

Read [AGENTS.md](AGENTS.md) and
[docs/HACKATHON_CONTEXT.md](docs/HACKATHON_CONTEXT.md). Follow the shared
collaboration rules and preserve the event reference's verification labels.

**Required for every input and every participating agent/account:** Follow the
mandatory workflow in AGENTS.md. Sync before and after each substantive action or
work batch; reread changed instructions and shared context. After every user
input, persist relevant context and a concise handoff before dependent work, then
record the outcome before responding. Read
[docs/TEAM_DECISIONS.md](docs/TEAM_DECISIONS.md) and
[docs/AGENT_HANDOFFS.md](docs/AGENT_HANDOFFS.md) alongside the event reference.

Work in the shared repository. Commit, push, and verify completed changes and
context before completion or handoff; a local commit alone is insufficient.
Only drafts explicitly pending user approval may stay unpublished, with their
pending status recorded rather than treated as accepted decisions. Follow the
shared-checkout coordinator and safety rules; report sync/publication blockers
without discarding another agent's work.

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
