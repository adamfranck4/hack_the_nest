# Shared development guidance

## Shared context

Multiple Codex agents, including agents from different accounts, and Claude Code
may work simultaneously on this repository. Gemini may also join in the future;
its connection is not yet confirmed. These shared instructions apply to every
participating agent, account, and session. When event context is relevant, read
[docs/HACKATHON_CONTEXT.md](docs/HACKATHON_CONTEXT.md).
It is the shared event reference; preserve its source and verification labels.
Keep event research there rather than duplicating it in agent instructions.
Also read [docs/TEAM_DECISIONS.md](docs/TEAM_DECISIONS.md) for current team
choices and [docs/AGENT_HANDOFFS.md](docs/AGENT_HANDOFFS.md) for cross-session
status. The mandatory workflow below applies after every new user input.

## Mandatory workflow for every input and action

1. **Sync before acting.** On every user input, before substantive research,
   documentation, coding, delegation, or a repository-based answer, inspect Git
   state, fetch, safely integrate the intended remote branch, and reread changed
   instructions and shared context. Repeat before resuming work after an
   interruption and before each new substantive action or work batch. Git safety
   inspection and synchronization commands are the prerequisites to this rule.
2. **Update shared context after every input.** Persist new facts, decisions,
   constraints, corrections, ownership, and blockers before dependent work.
   Event facts go in `docs/HACKATHON_CONTEXT.md`; team/project decisions go in
   `docs/TEAM_DECISIONS.md`; collaboration rules go in these instructions.
   Preserve facts versus proposals, approval status, and verification labels.
   Record a concise input/status handoff in `docs/AGENT_HANDOFFS.md`, even when
   the input adds no new decision. Do not copy whole chats or secrets into docs.
3. **Work in the shared repository.** Keep authorized work, documentation,
   context, and handoffs in the existing checkout of
   `github.com/adamfranck4/hack_the_nest`. Separate accounts may use their own
   checkouts of this same repository; publish to its agreed branches, not an
   unrelated repository, private fork, or disconnected project copy. Do not keep
   the only copy of completed work in chat, scratch files, or a local branch.
4. **Sync and publish after acting.** After each completed substantive action or
   work batch, and before any completion report, handoff, or final response,
   update context with the outcome, fetch and reconcile concurrent changes,
   validate affected work, commit only your intended changes, and push to the
   agreed GitHub branch. Fetch again and verify that the remote branch contains
   your commit. A Git commit is initially local by design; it counts as shared
   delivery only after a verified push. No local-only completion claims.
5. **Draft exception.** Only material explicitly pending user approval may
   remain a draft outside published repository work. Mark it as a draft and do
   not treat it as an accepted decision or implementation. Record its existence
   and pending status in the shared handoff without publishing the draft itself
   if it is meant to stay private. Once approved, integrate it into the shared
   repository, commit, push, and verify. Do not invent approval gates for routine
   work already authorized by the user.

If sync, context updates, or publication are blocked, preserve all work, finish
unaffected work where safe, and report the exact blocker and unpublished state.
Never overwrite another agent's changes, force-push, expose secrets, or claim a
successful sync to satisfy this workflow. Shared-checkout workers send context
and completion deltas to their coordinator, who serializes updates and pushes;
they must not concurrently edit common handoff files or switch the shared branch.

## Collaboration rules

1. All participating agents share this repository. Establish the files each agent
   owns for the current task before overlapping work.
2. Inspect the current Git branch, status, diffs, staged changes, and recent
   commits before changes. Recheck before staging or committing.
3. Do not discard or overwrite another agent's work or uncommitted changes. Do
   not reset, revert, clean, or force-push to resolve overlapping work.
4. Prefer separate branches and focused commits. In a shared checkout, branch
   switches affect everyone using it: coordinate first. Use existing isolated checkouts
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

## Agent identity and coordination across accounts

- Do not assume “Codex” identifies a single agent. Use a distinct, non-sensitive
  session label in task briefs and handoffs, together with the working branch,
  base commit, and files owned. Distinguish separate Codex sessions even when
  they use the same model or local branch name.
- Separate accounts or sessions may have different checkouts, memory, tools,
  and GitHub permissions. Do not assume another agent has read this chat or
  received an instruction until it is available in the shared repository.
- Coordinate through shared repository instructions and GitHub-visible handoffs
  (such as commit or PR descriptions). Report the branch, commit link, changes,
  and outstanding ownership or interface issues so other sessions can resume.
  Never share account credentials to enable collaboration.

## Required GitHub synchronization — all agents

- Before every input-driven action or resumed work batch, inspect Git status, branch, staged
  changes, and recent history, then `git fetch origin`. Synchronize with the
  intended remote branch before doing substantive work. For shared work that
  branch is `origin/main`; for a coordinated feature branch, synchronize with its
  upstream and account for new changes on `origin/main`. Repeat synchronization
  after work as required by the mandatory workflow above.
- With a clean checkout and compatible history, use a fast-forward-only merge
  (for example, `git merge --ff-only origin/main` for shared work). If history
  diverges or another agent has uncommitted changes, inspect and coordinate a
  non-destructive integration before proceeding with affected work. Do not
  automatically stash another agent's work, reset, clean, or force-push.
- Commit completed, relevant changes in focused commits and **push them to
  GitHub before reporting completion or handing off**. Do not leave completed
  work only in the cloud checkout. Fetch again before pushing and incorporate
  remote changes safely; if a concurrent push rejects yours, fetch, reconcile,
  rerun affected checks, and retry without force.
- Use an explicit destination when the local and remote branch names differ
  (for example, local `work` targeting shared `main`:
  `git push origin HEAD:refs/heads/main`). For feature work, push the agreed feature branch and
  identify it in the handoff; do not imply it is already merged into `main`.
- Verify the intended remote branch contains the pushed commit and report the
  branch and commit link. If authentication, conflicts, or branch protection
  block synchronization, report the exact blocker and preserve all work; do not
  claim that GitHub is synchronized. These rules apply equally to every Codex
  session/account, Claude Code, and any Gemini or other agent that joins.
- When delegated workers share a checkout, serialize Git synchronization,
  staging, commits, and pushes through one coordinator (the Claude manager for
  its workers). Workers read these instructions and coordinate synchronization
  before work; the coordinator fulfills the push and verification requirements
  for their completed changes before handoff. Do not switch the shared branch
  while workers are editing or include another worker's unfinished changes.

## Scope and handoff

Follow the user's current task scope. Context/documentation work alone does not
authorize choosing a project, developing application features, or changing
dependencies, configuration, or architecture. Report files changed, validation,
unresolved coordination issues, branch/commit status, and whether work was pushed.
