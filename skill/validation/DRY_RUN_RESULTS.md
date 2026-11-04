# Foreman dry-run results (pre-NAS)

These are **dry-run results, not NAS results.** No UGREEN NAS was used.

The Skill was run by AI models acting as the Uliya main agent. The expert results were simulated from the dataset files:
- PDF text from `pdftotext`, and macOS Vision OCR for the image-only scan;
- whisper `small.en` transcripts;
- EXIF read with `piexif`.

Every run received identical inputs. The simulation returns raw document text, not the structured fields a real UGREEN expert would return, so it tests Foreman's reasoning and instructions, not UGREEN extraction.

The optional cross-check was simulated as `failed`, to test failure handling. The models never saw `ground-truth/`. Scores use `dataset-v2/ground-truth/SCORING_SHEET.md` (pass lines fixed before testing).

Models: Claude Haiku 5.5 and Claude Sonnet 5.5, through the Agent tool. These are stand-ins for Uliya's local or cloud model, which is likely weaker than Sonnet.

## Static checks

| Check | Result |
|---|---|
| Official `check-skill.mjs` (kit v0.7.3, run from a byte-identical copy) | `static-pass`, 0 errors, 0 warnings, 0 info (`official-check.json`) |
| Local re-implementation of the checker rules | static-pass |

## Round 1 (Skill as of commit 274a25f)

| Run | Model | Scope | A1 detected | A2 false pos. | A3 classes | A4 amounts | A6 forbidden | Verdict |
|---|---|---|---|---|---|---|---|---|
| r1-haiku-alpha | Haiku | Alpha full audit | 14/14 | 0 | 20/20 | **fail**: invoiced $33,650 (exp. $38,050), flagged $20,650 (exp. $25,050) | 0 | **FAIL (A4)** |
| r1-sonnet-alpha | Sonnet | Alpha full audit | 14/14 | 0 | 20/20 | all exact | 0 | **PASS** (independent scorer: A1–A12 all pass; one weakness: the ceiling over-claim also got the missing-approval sentence, which A8 does not test) |
| r1-haiku-beta | Haiku | Beta (B1) | 4/4 Matched, $34,900.00 | 0 | — | exact | 0 | **PASS** |
| r1-haiku-gamma | Haiku | Gamma (B2) | 2/2 Matched, $25,000.00 | 0 | — | exact | 0 | **PASS** |

Round 1 problems and the fixes applied for round 2:

| Problem seen | Cause in the Skill | Fix |
|---|---|---|
| The scanned INV-008 was dropped from the invoiced total, because OCR read `$4,400.00` and `$4.400.00` | No rule for OCR readings that differ only in separators | evidence-rules step 1: same digits means a formatting artefact, so use the amount. Totals rule: unreadable invoices are listed beside the total, never silently dropped |
| The ceiling over-claim ($3,750) got "No approval evidence found…" (both models) | Step 4 did not separate claiming *omitted* work from claiming *extra* work | Step 4 now words the finding by cause: omitted work is "claims work omitted by CO-xxx", without the missing-approval sentence |
| Walls excess: unclear whether step 3d or step 4 applies | Step 3d said "not a contract item" too loosely | Step 4 is the only step for extra quantity on a contract item |
| The missing 13 Oct email appeared only inside the INV-010 finding | The non-claim row rule was implicit | A referenced missing document always gets its own row |
| Summary counts were unclear (are application rows included?) | Template wording | Counts are "Ledger rows by primary class, every row once" |
| A cross-check was sent for an unreadable scan | Cross-check purpose unclear | A cross-check is only for readable documents |
| Date checks were lost when a claim stopped at step 1 | Ladder silent | Step 6 date checks still run on the cited documents, as a separate row |
| Save instruction: where the report text goes, who sets the date in the file name | Template silent | "Report text:" line; Foreman sets the name; the returned path is reported as returned |
| No evidence type for notices, RFIs, registers, certificates | Table incomplete | Added the "Context record" type |
| Duplicates: does the missing-approval sentence apply? | Silent | A duplicate never carries it |
| Transcripts without speaker labels | Silent | Quote as "a speaker says" |
| CO-005 was dated 23/09 but cited a drawing issued 25/09 (found by Haiku) | **Dataset bug**, not the Skill | Generator fixed (CO-005 now issued 26/09); dataset regenerated and re-verified (0 problems, deterministic) |

## Round 2 (Skill after the round-1 fixes)

| Run | Model | Scope | A1 detected | A2 false pos. | A3 classes | A4 amounts | A6 forbidden | A8 wording | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| r2-haiku-alpha-a | Haiku | Alpha full audit | 14/14 | 0 | 20/20 | all exact: $38,050 / $13,000 / $25,050 / $11,650; $6,000, $1,800, $3,750; PA-03 recalculated $28,072.50 | 0 | pass; ceiling worded "work omitted by CO-007" | **PASS** |
| r2-haiku-alpha-b | Haiku | Alpha full audit | 14/14 | 0 | 20/20 | all exact (same figures) | 0 | pass; states that the missing-approval sentence "does not apply" to the ceiling | **PASS** |
| r2-sonnet-alpha | Sonnet | Alpha full audit | 14/14 | 0 | 20/20 | all exact (same figures) | 0 | pass; ceiling worded "claims work omitted by CO-007" | **PASS** (scored from its reconciliation log; the report text was not fully transmitted) |

Both Haiku runs gave the same classes and amounts for every finding (consistency check).

Round 2 observations and the fixes applied afterwards:

| Observation | Fix |
|---|---|
| The new "referenced document gets its own row" rule also created rows for a quote, an annex and a clearance certificate. Not wrong, but noisy | Own rows only for missing **approval** documents (approval emails or letters, change orders); other missing attachments go only in the Missing Evidence list |
| Primary class unclear when an excess also needs the missing-approval sentence | Primary stays Review, "also Missing evidence" |
| Application-row class: do "also" classes count? | Primary classes only |
| "Approval date" undefined when two signatures carry different dates | The last required signature |
| Cross-check trigger "inconsistent" undefined | Line amount ≠ quantity × rate, or lines do not add up to the stated total |
| Report date, and a returned file name that differs | The report date is the day Foreman produces the report; tell the user when the returned name differs |
| Document title conflicts with other text | The title wins |
| Test-input bug: the simulated typing step labelled PC-03 a payment application (fixture rule order) | Fixture builder fixed (the model had already corrected it from the title) |

## Round 3 (final Skill: round-2 fixes applied)

| Run | Model | Scope | A1 detected | A2 false pos. | A3 classes | A4 amounts | A6 forbidden | A8 wording | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| r3-haiku-alpha | Haiku | Alpha full audit | 14/14 | 0 | 20/20 | all exact: $38,050 / $13,000 / $25,050 / $11,650; PA-03 recalculated $28,072.50 | 0 | pass | **PASS**. Missing-evidence rows fell from 7–8 to 5: own rows only for CO-009 and the 13 Oct email; quote, annex and certificate listed only |
| r3-haiku-inv010 | Haiku | Single claim "Check invoice INV-010" (B3) | INV-010 found | 0 | Missing evidence + Review | $8,500 / $6,000 exact | 0 | pass | **PASS**. Reviewed only INV-010 and checked that no other claim duplicates it |
| r3-sonnet-alpha | Sonnet | Alpha full audit | 14/14 | 0 | 20/20 | all exact (same figures) | 0 | pass | **PASS** (scored from its reconciliation log; own rows only for the missing approval documents) |

Late observation from r2-sonnet: to keep the save instruction single-quoted, it avoided apostrophes by paraphrasing contract quotes. Fix: escape apostrophes and never reword a quotation (`SKILL.md` Workflow). Second dataset bug found by r2-sonnet: CO-006 Rev B was issued 2026-07-13 although the 14 July meeting announces the revision. The generator now issues it on 2026-07-14 (signature date unchanged; answer key unaffected; dataset re-verified, 0 problems).

## Summary

| Round | Full audits passed | Scoped / single-claim passed |
|---|---|---|
| 1 | 1 of 2 (Haiku failed on totals) | 2 of 2 (Beta, Gamma) |
| 2 | 3 of 3 | — |
| 3 (final) | 2 of 2 | 1 of 1 (INV-010) |

**What this does not show:**
- UGREEN's real extraction, OCR, transcription or photo tools. They were simulated from the dataset files.
- Behaviour of Uliya's local model, which may be weaker than Haiku.
- Performance on real or larger archives.

These remain "pending NAS validation".
