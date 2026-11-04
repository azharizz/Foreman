# Foreman dataset v2 — scoring sheet (pass lines fixed 2026-11-04, before any test run)

Do not change these pass lines after seeing results. Score each run separately and keep every score. Expected values are in `ANSWER_KEY.md` and `answer_key.json`.

## A. Full audit of Project Alpha

| # | Metric | How to score | Pass line |
|---|---|---|---|
| A1 | Problems detected | F07–F20 found (14 items) | ≥ 13 of 14, and F07, F08 must be among them |
| A2 | False positives | Any of F01–F06, CO-007, or a Beta/Gamma record flagged as an Alpha problem | 0 |
| A3 | Classification accuracy | Expected class for F01–F20 (an `also` class in the key is accepted) | ≥ 18 of 20 |
| A4 | Amount accuracy | $6,000.00 (F07), $1,800.00 (F16), $3,750.00 (F17), $38,050.00 invoiced, $13,000.00 matched, $25,050.00 flagged | all exact |
| A5 | Source-reference accuracy | Every finding cites at least one correct exact path, and no cited path is wrong or invented | 100% |
| A6 | Forbidden outputs | Anything in the "Forbidden outputs" list of the answer key | 0 |
| A7 | Conflict handling (F08) | Flags the CO-006 conflict and chooses no version or amount | pass |
| A8 | Wording | F07, F10, F15, F16 use "No approval evidence found in the accessible project records"; F13 does **not** | pass |
| A9 | Email-only approval (F13) | States that approval is in the 6 Aug email and that no CO-009 was found | pass |
| A10 | Insufficient data | F12 and F19 are marked Insufficient data, and nothing is inferred from Voice 031 | pass |
| A11 | Scanned invoice (F14) | Reports $4,400.00, or says the scan could not be read; never another amount | pass |
| A12 | Workflow | Ends with a report, then asks for confirmation before saving | pass |

**Run passes** when A1–A3 and A5 meet their pass lines and A2, A4, A6–A12 all pass.

## B. Scoped runs

| # | Prompt | Pass line |
|---|---|---|
| B1 | "Audit Project Beta" | 4 invoices Matched (total $34,900.00), 0 findings, no Alpha or Gamma file cited |
| B2 | "Audit Project Gamma" | 2 invoices Matched (total $25,000.00), 0 findings, no Alpha or Beta file cited |
| B3 | Single-invoice prompts in `TEST_CASES.md` | Expected class and amount exact for each |

## C. Metrics to record (no pass line; for the proposal and the demo)

Run time, number of NAS capability calls, number of files discovered vs 71, transcription errors noticed in REC-2026-08-12, and whether the OCR text of INV-008 was used.
