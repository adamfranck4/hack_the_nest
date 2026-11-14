# Agent handoffs

Shared status for agents across accounts and checkouts. After every user input,
record a concise entry with a distinct session label, branch/base commit, files
owned, new context or an explicit no-decision-change note, outcome, and blockers.
Update the entry as work completes. Keep facts and accepted decisions in their
existing reference documents; never include secrets or whole chat transcripts.
In a shared checkout, the coordinator serializes entries from its workers.

## 2026-11-14 — codex-context-sync

- Branch: local `work`, publishing to shared `main`; base: `ca2dda3`.
- Input: require every agent/account to sync before and after work, update shared
  context after every input, and commit/push work to the shared GitHub repository.
  Only drafts explicitly pending user approval may remain unpublished drafts.
- Owned files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, this handoff,
  and shared-workflow instructions in `.claude/agents/` and `.codex/agents/`.
- Outcome: workflow recorded in the shared instructions and every role entry
  point; includes context routing, draft handling, and serialized worker updates.
  Documentation links and role-file syntax checked before commit/push.
- Team/project decisions: unchanged. No application development performed.
- Blockers: none identified. Verify publication using the GitHub commit containing
  this entry; a local copy of the entry alone is not evidence of a push.
