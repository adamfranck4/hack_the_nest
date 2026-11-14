# Agent handoffs

Shared status for agents across accounts and checkouts. After every user input,
record a concise entry with a distinct session label, branch/base commit, files
owned, new context or an explicit no-decision-change note, outcome, and blockers.
Update the entry as work completes. Keep facts and accepted decisions in their
existing reference documents; never include secrets or whole chat transcripts.
In a shared checkout, the coordinator serializes entries from its workers.

## 2026-11-14 — claude-manager — Talk It Out MVP build

- Branch/base: shared `main` on Adam's machine, base `3ba42ad`.
- Input: Adam chose the "Talk It Out" conversation-practice app and a Python +
  React stack (see [team decisions](TEAM_DECISIONS.md#project-accepted-by-adam-2026-11-14)).
- Owned files: everything listed in [API_CONTRACT.md](API_CONTRACT.md#folder-layout-and-ownership)
  (`backend/`, `frontend/`, `README.md`, `docs/DEMO_SCRIPT.md`, `docs/DEVPOST_DRAFT.md`,
  `.env.example`). Other sessions: please don't edit these during the build;
  propose changes via a handoff entry instead.
- Outcome: MVP built and verified by the coordinator — 32 backend tests pass
  (fakes, no API calls); live run: toddler round won in 3 turns with real
  Gemini + ElevenLabs audio, scorecard 95; bad line on angry caller spiked the
  meter +20; UI checked in browser (picker, meter, typed turn, no console
  errors). Default Gemini model changed to `gemini-flash-lite-latest`
  (`gemini-flash-latest` timed out). Not yet verified: live microphone input,
  phone layout. Docs keep a few `VERIFY after build` markers for items needing a live rehearsal. v1.3 adds teen, roommate and coworker scenarios (6 total).
- Blockers: none. Note: `google-genai`/`elevenlabs` SDKs can't install on this
  machine (no `cryptography` wheel for Python 3.14 ARM64); REST via `httpx` instead.

## 2026-11-14 — codex-context-sync — documentation consolidation

- Branch/base: local `work` to shared `main`, starting at `ea39194`.
- Input: apply the duplication review and require concise, uniform organization
  after future changes. The preceding review was report-only; cleanup is now authorized.
- Owned files: shared instructions, README, team decisions, event-reference
  cross-references, this handoff, and Claude/Codex role instruction files.
- Outcome: shared rules consolidated in AGENTS.md; role duties moved intact to
  AGENT_ROLES.md with thin Claude/Codex entries. Added a mandatory organization
  check, simplified navigation, and clarified secret storage and unverified
  track rationale. Shared facts and team choices remain in their own documents.
- Validation: Markdown links/anchors and whitespace pass; six TOMLs parse;
  platform metadata and worker duties preserved. Markdown/TOML content reduced
  by about 36%. App settings, dependencies, and code unchanged.
- Remaining limitation: Codex role activation is unverified, now noted in README.
  No external blocker identified. Publication must be verified against the GitHub
  commit containing this entry; the entry alone does not establish push success.

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
