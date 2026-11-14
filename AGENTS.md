# Shared development guidance

## Shared context

Codex and Claude Code may work simultaneously on this repository. When event
context is relevant, read [docs/HACKATHON_CONTEXT.md](docs/HACKATHON_CONTEXT.md).
It is the shared event reference; preserve its source and verification labels.
Keep event research there rather than duplicating it in agent instructions.

## Collaboration rules

1. Codex and Claude Code share this repository. Establish the files each agent
   owns for the current task before overlapping work.
2. Inspect the current Git branch, status, diffs, staged changes, and recent
   commits before changes. Recheck before staging or committing.
3. Do not discard or overwrite another agent's work or uncommitted changes. Do
   not reset, revert, clean, or force-push to resolve overlapping work.
4. Prefer separate branches and focused commits. In a shared checkout, branch
   switches affect both agents: coordinate first. Use existing isolated checkouts
   where available; do not create a Git worktree unless explicitly requested.
   Stage only files intentionally changed for your task; do not use blanket
   staging that can capture another agent's changes.
5. Coordinate shared API contracts and interfaces before implementation: routes,
   methods, payloads, data models, and environment-variable names. Communicate
   necessary contract changes before editing dependent components.
6. Avoid editing files actively owned by another agent. If ownership overlaps or
   unexpected edits appear, coordinate and reconcile rather than replacing them.
7. Preserve existing project conventions, application behavior, and architecture.
   Preserve existing documentation and Claude-specific instructions under
   `.claude/`; these shared rules complement their role and ownership guidance.
8. Run relevant tests when changing application code. Report commands and actual
   outcomes, including failed or unrun checks; do not claim unexecuted validation.
9. Do not expose or commit API keys, tokens, credentials, or other secrets. Keep
   values in approved local/environment secret storage; document names only.
10. Prioritize maintaining a working project before **Sunday, November 15, 2026,
    noon Eastern (`America/Detroit`)**, the final submission deadline. The draft
    is due at the start of that Sunday, **12:00 AM**, on Devpost and the event app.

## Scope and handoff

Follow the user's current task scope. Context/documentation work alone does not
authorize choosing a project, developing application features, or changing
dependencies, configuration, or architecture. Report files changed, validation,
unresolved coordination issues, branch/commit status, and whether work was pushed.
