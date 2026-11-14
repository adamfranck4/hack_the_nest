# Shared development guidance

## Scope and reference map

These rules apply to every Codex session/account, Claude Code, and any other
agent working on [the shared repository](https://github.com/adamfranck4/hack_the_nest).
Gemini coding-agent participation is unconfirmed; the app's Gemini API use is a
separate integration. Different sessions may have
separate memory, checkouts, tools, and permissions. Never assume shared chat history.

| Document | Authoritative content |
|---|---|
| [Hackathon context](docs/HACKATHON_CONTEXT.md) | Event facts, deadlines, sources, verification status |
| [Team decisions](docs/TEAM_DECISIONS.md) | Roster, accepted choices, proposals, unresolved decisions |
| [Build contract](docs/API_CONTRACT.md) | App API routes, interfaces, file ownership |
| [Agent handoffs](docs/AGENT_HANDOFFS.md) | Per-input status, ownership, outcomes, blockers |
| [Agent roles](docs/AGENT_ROLES.md) | Manager and worker responsibilities |
| This file | Shared workflow, safety, organization rules |

Read team decisions and current handoffs before work; consult event context when
relevant and role responsibilities when assigned a role. Platform entry files
(`CLAUDE.md`, `GEMINI.md`, `.claude/agents/`, `.codex/agents/`) refer here rather
than restating shared policy.

## Mandatory workflow

A **work batch** is one coherent action such as research, editing, testing,
delegation, or preparing a repository-based answer. Every new input, interruption,
or resumed task starts a new batch. Sync before and after each batch; Git safety
inspection and synchronization commands are prerequisites, not recursive batches.

1. **Sync before acting.** Inspect branch, status, diffs, staged changes, and
   recent commits; `git fetch origin`, safely integrate the intended remote
   branch, and reread changed instructions/context. Shared work targets
   `origin/main`; coordinated feature work targets its upstream and accounts for
   changes on `origin/main`. With a clean checkout and compatible history, use
   `git merge --ff-only origin/main` for shared work. If history diverges or
   another agent has uncommitted work, coordinate non-destructive integration
   before proceeding with affected work.
2. **Update context after every input.** Persist new facts, choices, constraints,
   corrections, and ownership in the document identified above before dependent
   work. Preserve fact/proposal, approval, and verification labels. Record a
   concise handoff even if no decisions changed; update its outcome before
   responding. Never copy entire chats or secrets into context.
3. **Work in this repository.** Use an existing checkout of the shared GitHub
   repository and its agreed branches. Different accounts may use separate
   checkouts of that same repository. Do not keep the only copy of authorized
   work in chat, scratch files, disconnected projects, private forks, or local
   branches. Follow the current task scope; documentation work alone does not
   authorize application features or architecture/dependency changes.
4. **Sync and deliver after acting.** Update the outcome, perform the consistency
   check below and relevant validation, fetch/reconcile concurrent changes, then
   commit only intended changes and push before completion, handoff, or a final
   response. If a concurrent push rejects yours, reconcile and rerun affected
   checks before retrying. Fetch again and verify the remote contains the commit.
   Git creates commits locally first; delivery requires a verified push. Use an
   explicit destination when names differ, e.g. local `work` to shared `main`:
   `git push origin HEAD:refs/heads/main`. Feature-branch delivery is not a merge
   into `main`; report the destination and commit link accurately.
5. **Keep only approval-pending drafts unpublished.** Mark explicit drafts and
   record their pending status without publishing private draft content or
   treating it as accepted. After approval, integrate, commit, push, and verify.
   Do not invent approval gates for already authorized routine work.

If synchronization or publication is blocked, preserve all work, continue safe
independent work, and report the exact blocker and unpublished state. Never claim
unverified completion.

## Collaboration and safety

- Use a distinct, non-sensitive session label, branch/base commit, and file
  ownership in briefs/handoffs; “Codex” or a local branch name alone is ambiguous.
  Share decisions through repository documents and GitHub-visible handoffs.
- Agree on ownership and shared interfaces (routes, methods, payloads, data models,
  variable names) before overlapping work. Coordinate contract changes before
  editing dependent components; avoid files actively owned by another agent.
- Preserve other agents' work, project conventions, behavior, and architecture.
  Do not reset, revert, clean, force-push, or automatically stash another agent's
  work. Prefer focused commits and coordinated separate branches; do not create
  a Git worktree unless explicitly requested. Recheck and stage only owned files.
- In a shared checkout, one coordinator serializes Git and common context updates
  (the manager for its workers). Workers provide deltas to that coordinator, who
  fulfills the workflow for their completed changes. Never switch a shared branch
  while others edit, concurrently edit shared handoff files, or stage unfinished
  work belonging to someone else.
- Run relevant tests for application changes and report actual outcomes, including
  failed or unrun checks. Prioritize a working project before the final submission
  deadline in [the event schedule](docs/HACKATHON_CONTEXT.md#critical-deadlines).
- Never expose or commit keys, tokens, credentials, or other secrets. Use approved
  environment secret storage or ignored local configuration; document names only.
  Never share account credentials between agents.

## Required organization check after changes

Before delivering each batch, review the affected files and their references:

- Keep one authoritative location per fact, decision, rule, or role responsibility;
  link to it instead of copying prose, rosters, deadlines, or prize tables.
- Extend the appropriate existing file before creating a new one. New files need
  a distinct purpose and an index/reference link; avoid duplicate context files.
- Keep platform entries thin: retain required metadata and runtime-specific
  instructions, and point to the shared rules/roles. Keep counterpart entry
  formats uniform without copying platform-specific tools or models across agents.
- Use consistent terminology, headings, links, and concise formatting. Update
  stale references/placeholders; label assumptions and pending approvals. Preserve
  meaningful history and uncertainty instead of silently changing team decisions.
- Check affected links/anchors, role-file syntax, and diffs; remove only redundant
  material within the authorized scope. Record checks, remaining issues, branch,
  commit link, and push status in the handoff/report. Do not claim role activation
  or runtime behavior from file presence alone.

## Required transparency for every agent

- Keep GitHub-visible updates factual and concise: the handoff and commit/PR
  description must explain the request, behavior changed, files/ownership,
  validation commands and actual results, and remaining risks or incomplete work.
  Label docs-only plans, mock demonstrations, tested implementation, and verified
  live behavior separately. Do not present another agent's report as your own test.
- Record operational actions too, even when they do not change source: dependency
  installation, processes started/stopped, environment or access changes, external
  service use, deployment attempts, cancellations, and rollback results. State
  what was done, its outcome, and anything the next agent must clean up or resume.
- Explain what each push contains and any expected automatic deployment. Verify
  the remote commit, then distinguish GitHub delivery from deployment requested,
  building, live-verified, failed, or unverified. Verify live behavior separately;
  do not infer it from a successful push or a passing mock test.
- Protect private information while reporting actions: include variable names
  and configuration status, never key values, tokens, credential files, private
  account details, authenticated URLs, or unredacted logs. Summarize/redact private
  inputs rather than copying them into GitHub. Do not commit ignored local setup.
- Give the user progress updates and a final account of changes, checks, blockers,
  destination branch, and commit link. Shared-checkout workers send these details
  to their coordinator for the combined handoff; avoid duplicating full logs.
