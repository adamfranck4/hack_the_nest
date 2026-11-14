# Agent handoffs

Shared status for agents across accounts and checkouts. After every user input,
record a concise entry with a distinct session label, branch/base commit, files
owned, new context or an explicit no-decision-change note, outcome, and blockers.
Update the entry as work completes. Keep facts and accepted decisions in their
existing reference documents; never include secrets or whole chat transcripts.
In a shared checkout, the coordinator serializes entries from its workers.
Apply the [shared transparency requirements](../AGENTS.md#required-transparency-for-every-agent)
to operational actions and push/deployment status as well as code changes.

## 2026-11-14 — codex-track-assessment — judging review

- Branch/base: local `work` to shared `main`, base `70dcb25`.
- Input: assess Talk It Out for AI/ML, Best Beginner, and intended ElevenLabs
  selection using prior context, current code, and new official-source research.
- Ownership: assessment/provenance documentation and this handoff only. No app,
  track selections, environment settings, or deployment settings are being changed.
- Outcome: [TRACK_ASSESSMENT.md](TRACK_ASSESSMENT.md) separates verified descriptions,
  judge-style assessment, and prioritized recommendations. Verified website text
  adds beginner learning emphasis and flags unresolved OpenAI/Exa provider fit.
  Entrant tracks redirected to login; current account selection cannot be verified.
- Operations: read official event/source assets, MLH judging guidance, ElevenLabs
  TTS documentation, and existing coaching-product pages; used a read-only research
  browser. No paid AI requests, app edits, service restarts, or settings changes.
  Historical sponsor winner claims remain unverified and were not used as criteria.
- Validation: report citations checked against successfully retrieved sources;
  local references/anchors and diff checks passed. App tests were not run for this docs-only
  batch. A `main` docs push may trigger Render auto-deploy; it is not an app release.

## 2026-11-14 — codex-review-fixes — consistency and transparency

- Branch/base: local `work` targeting shared `main`, base `d423481`.
- Input: fix concurrent voice overspending, early-end outcomes, and stale mock
  scenarios; review consistency and require transparent, privacy-safe agent updates.
  Test all changes before finalization and verify the public deployment separately
  from the repository's configured Render auto-deploy behavior.
- Ownership: voice-budget and scorecard paths, shared character/demo data,
  associated tests, affected documentation, and shared agent instructions.
- Changes: atomic voice-credit reservations/refunds (including midnight rollover),
  explicit `ended` scorecard outcome in real/mock modes, and a generated static
  demo catalog sourced from live character definitions with parity checks.
  Aligned setup/status/interface docs and centralized transparency requirements.
- Validation before push: 89 backend tests and 4 Node frontend tests passed;
  Markdown links/anchors, generated JSON, TOML syntax, and diff checks passed.
  Tests use fakes and do not call paid AI services. A pre-existing Starlette
  TestClient deprecation warning remains; it does not affect these results.
- Operations: installed pinned test dependencies in a temporary `/tmp` virtual
  environment; no source dependency declarations, keys, or environment settings
  changed. No persistent app server was started for these checks.
- Delivery: pushing this batch to `main` is expected to trigger Render auto-deploy.
  Deployment/site checks will follow the push; they are not established by local
  tests or by this handoff. GitHub commit link and observed deployment outcome
  are reported separately to the user, without including private credentials.
- Verified delivery: [33b4428](https://github.com/adamfranck4/hack_the_nest/commit/33b442832d61bc856f0161a4bcf01eb93e2ebff0)
  reached GitHub `main`. The public Render site then served byte-identical copies
  of the pushed API module, generated catalog, and scorecard component.
- Post-push browser checks: desktop/mobile homepage; all six mock openings/hints;
  hint toggle; typed mock round and Ended early scorecard; exhausted-voice typed
  fallback. No horizontal overflow in checked mobile screens, page errors, or
  failed requests. Browser requests used a TLS-verifying HTTP client to bridge
  this environment's Chromium trust-store mismatch; verification was not disabled.
- Live service check: one short real typed Gemini round and an early scorecard
  succeeded (85/100). Session creation/reply may use ElevenLabs TTS credits;
  no concurrent paid budget stress test or microphone/STT call was performed.
- Remaining limits: budget and sessions remain process-local and reset on
  restart; service-key usage limits remain the hard cap. Live microphone input
  is untested. No environment/deployment settings or secret values were changed.
- This follow-up records test evidence and the optional Node 22+ test prerequisite
  only; it does not alter app code. A further `main` push may auto-deploy again.

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
