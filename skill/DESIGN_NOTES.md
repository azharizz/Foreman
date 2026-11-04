# Foreman Skill — design notes (steps 1–3, 2026-11-04)

The Skill package is `foreman/` (only `SKILL.md` and `references/`; the folder name must equal the Skill name). This file sits outside the package on purpose: the checker rejects any other root file, including the README.md that the Starter Kit recommends.

## 1. Capability verification (step 1)

Source of truth: `requirements/uliya_skill_kit/extracted/uliya-skill-kit/data/capability-catalog.json` (v2.0.0, 2026-09-01). The parent Skill may only `delegate --target <agent> --instruction '<task>'`; each expert picks its own actions.

| Stage | Expert (target) | CLI → actions it can use | Effect / approval | Status |
|---|---|---|---|---|
| 1 Discovery | `file-agent` | `ug-filesystem` ls, find, stat | read / none | Supported |
| 1 Document typing (by content, not file name) | `document-agent` | `ug-document` metadata, qa (preview) | read / none | Supported |
| 2 Contract | `document-agent` | `ug-document` extract (`schema=contract`), qa | read / none | Supported |
| 3 Change orders, correspondence, RFIs, registers, diaries, delivery notes | `document-agent` | `ug-document` extract (`schema=auto/mixed`), qa | read / none | Supported |
| 4 Recordings | `knowledge-agent` | `ug-knowledge` audio-transcription (returns transcript, segments, quality, warnings, failures; `speak-count` option) | read / none | Supported; the catalog example uses `.m4a` |
| 4 Photos | `photo-agent` | `ug-photo` meta (EXIF by path); fallback search-picture by `dir` | read / none | Supported; whether `meta` works on files outside the photo library is unverified |
| 5 Claims | `document-agent` | `ug-document` extract (`schema=invoice` / `mixed_reconciliation`), reconcile | read / none | Supported |
| 5 Cross-check | `document-agent` | `ug-document` reconcile | read / none | Supported; output semantics not documented, so used only as a second opinion |
| 6 Save report | `knowledge-agent` | `ug-knowledge` save-text (returns `verified`, `outputFile`) | **state-change / workflow approval** | Supported; asked only after user confirmation |

Six proposed roles (PRODUCT_FOREMAN §11) mapped to real experts:

| Proposed role | Real expert |
|---|---|
| Project Finder | `file-agent` |
| Contract Analyst, Change Analyst, Invoice Analyst | `document-agent` |
| Meeting Analyst | `knowledge-agent` |
| Visual evidence (new) | `photo-agent` |
| Evidence Investigator | the Foreman Skill itself (main agent reasoning over returned results) |

**Not used on purpose:** `ug-filemgr` tagging, `file-workflow` moves, `ug-filesystem` write actions. Foreman is read-only apart from one confirmed save. This removes every destructive path.

## 2. Gaps and how the Skill handles them

| Gap (unverified until the NAS day) | Handling in the Skill |
|---|---|
| OCR of an image-only PDF via `ug-document` is not stated in the catalog (`ug-photo` vision-ocr exists, but for images) | Stage 5 asks for OCR plus coverage; if the document can't be read → Insufficient data, never a guessed amount |
| Page references: `extract` returns coverage but page numbers aren't promised | Ledger says "page where available" |
| `.eml` support unknown | Dataset ships printed PDFs; `.eml` only in `alt-formats/` |
| `max-files` defaults to 60 | Delegations go in batches of 50 or fewer |
| Permissions, prerequisites and error codes are `unknown` for every action in the catalog | All five delegation states are handled; failures stop only the dependent stages |
| save-text output format and path rules unknown | User chooses the folder; new file only; verified path reported |
| UGREEN documents that chat uploads and knowledge-base content go to the cloud model in cloud mode; whether expert processing of NAS files does the same is not documented | The notice before Stage 1 says content "may be sent"; local model recommended |
| Long report text inside one save instruction; `save-text` also accepts `content-ref` | Unverified size limit; test on the NAS day |
| No scheduled or background capability | None promised (no monitoring, no indexing) |

## 3. Decisions taken (step 2, resolves PRODUCT_FOREMAN §28.3)

1. **Canonical outputs** (§13.1):
   - Project Overview
   - Original Scope Register
   - Change-Order Register
   - Evidence Timeline
   - Claim-to-Evidence Ledger (it doubles as the Invoice Exception Register)
   - Missing Evidence
   - Coverage and limits

   All of these sit inside one Investigation Report. Defined in `foreman/references/ledger-and-report.md`.
2. **Ledger schema:** 15 fields per row (same file, section 1). Matched rows are kept so that false positives can be measured.
3. **Evidence types:** formal approval, written approval, discussion, reported instruction, reported work, claim, and superseded/draft (`references/evidence-rules.md` §1).
4. **Classification:** a fixed 8-step ladder for each claim line. The first step that raises a finding sets the primary class; later steps add "also" classes.
5. **Handover reports:** future work. **Historical reconstruction:** kept only as the "what happened with X" timeline request.
6. **Read-only:** no file tagging, moving or renaming in v1.
7. **Language:** English in Round 1. Replies follow the user's language; machine identifiers stay unchanged.

## 4. Checker compliance (learned from `check-lib.mjs`, reviewed, not run)

The checker is stricter than the kit's prose:
- **Headings:** must be exactly `# Goal`, `# Required input`, `# Workflow` (or `# Orchestration`) and `# Completion and failure`.
- **Capability evidence:** needs a `# Generation-time capability evidence` heading, with lines in the form ``- `cli` → `agent` `` using the `→` character. The template's `->` fails.
- **Frontmatter:** only `name` and `description`. The description must contain "when" or "use when", and be 1,024 characters or fewer.
- **Delegate commands:** one per line; single-quoted instruction; no ` --flag`, `|`, `<`, `>`, `&&` or `<placeholder>` inside the instruction.
- **Required text:** all five status words must appear, along with "real result" or "upstream" wording, and "empty result" or "no results" wording.
- **Forbidden on any line:** "skip/bypass/ignore/disable … approval/permission/audit" (even negated); `/nas/…`, `/volume…` or `/share…` paths; `cat`, `cp`, `mv` or `rm` followed by a space; `cli.invoke` unless negated; "request id" / "expert id".

My own re-implementation of these rules (scratchpad `lint_skill.py`) reports **static-pass: 0 errors, 0 warnings**. It caught every planted violation in a negative test. The official checker (`check-skill.mjs`) only reads files and hashes them (no network, no child processes, no writes). It has **not** been run, as agreed; running it is step 4.

## 5. Assumptions I chose (confirm or change)

These are design choices, not facts from the kit or the research:

| Assumption | Where | Why |
|---|---|---|
| A photo more than 1 km from the contract site reference does not corroborate | evidence-rules §4 | Simple, explainable threshold. A large site might need more; change the number if so |
| Batches of up to 50 files per delegation | SKILL Workflow | Stays below the catalog `max-files` default of 60 |
| The first ladder step that raises a finding sets the primary class | evidence-rules §3 | Deterministic and scoreable; matches the answer-key classes |
| A quantity above the contract is Review (with the missing-approval sentence for the excess), not Missing evidence | evidence-rules §3 step 4 | The base quantity is approved; only the excess lacks approval |
| Every request runs all stages over the whole folder | SKILL Goal | Duplicates and approvals can sit anywhere; costs time on large folders |
| The report is offered for saving in the project folder by default | SKILL Stage 6 | The Evidence Vault idea (PRODUCT_FOREMAN §9); Foreman does not create folders |
| Apostrophes inside instructions are escaped as `'"'"'` | SKILL Workflow | The checker requires single-quoted instructions; runtime parsing is unverified |

## 6. How the rules cover dataset-v2 (team-only; never put this in the package)

| Finding | Rule that produces it |
|---|---|
| F01, F02, F05 Matched | Ladder step 8 |
| F03 excluded-but-approved | Step 3e: a signed CO covers the exclusion |
| F04 look-alike | Step 5: a different signed CO is not a duplicate |
| F06 retention | Step 4: retention is not a finding |
| F07 doors | Step 3b (unsigned) + step 4 (amount); delivery before request is noted from the timeline; Gamma excluded by scope |
| F08 concrete | Step 3a (two signed revisions) |
| F09 duplicate | Step 5 (same CO, quantity and amount) |
| F10 ducts | Section 4 (unsigned CO, work done, not claimed) |
| F11 13 Oct email | Section 4 (referenced document missing) |
| F12, F20 photos | Section 4 (no date / GPS more than 1 km from the contract site reference) |
| F13 email approval | Step 3c (approval exists, CO-009 missing); step 2 keeps the missing Q-0806 attachment as a note only |
| F14 asbestos | Step 6 (notice period, work before signature); step 1 if OCR fails |
| F15 painting | Step 3e (exclusion, no approval) |
| F16, F17 PA-03 | Step 4 (quantity above contract adjusted by signed COs, including the deduction) |
| F18 PC-03 | Section 4 (certificate later than contract period) |
| F19 voice memo | Stage 4 rule + section 4 (thin recording → Insufficient data) |
| Superseded schedule, Beta, Gamma | Stage 2 (superseded never used) and Required input (scope = confirmed folder) |

## 7. Status after steps 4–7 (2026-11-04)

- **Step 4, validation:**
  - The official checker passes (`validation/official-check.json`).
  - Three dry-run rounds on Haiku and Sonnet: round 1 had one failure (Haiku, totals); rounds 2 and 3 passed. Details and every fix are in `validation/DRY_RUN_RESULTS.md`.
  - The dry runs also found two dataset bugs (CO-005 and CO-006 Rev B issue dates). Both are fixed in the generator.
- **Step 5, proposal:** `submission/PROPOSAL.md`, 489 words. The team names are still to be filled in.
- **Step 6, package:** `submission/foreman.zip` (checked) and `submission/CHECKLIST.md`.
- **Step 7, NAS day:** `submission/NAS_DAY_PLAN.md`.
