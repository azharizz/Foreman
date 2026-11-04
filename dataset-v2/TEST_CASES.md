# Foreman dataset v2 — test cases and demo plan

All paths are under `nas-upload/Project-Alpha/` unless another project is named. Expected results are in `ground-truth/ANSWER_KEY.md`; pass lines are in `ground-truth/SCORING_SHEET.md`.

## Round 1 proposal — two core tests and one edge case (same scenarios as v1, renumbered)

**Test 1 — Successful reconciliation (core)**
- Prompt: *"Check invoice INV-002 in Project Alpha."*
- Input: `01-Contract/CONTRACT-001_Original-Agreement.pdf`, `02-Change-Orders/CO-002_Additional-Windows.pdf`, `03-Invoices/INV-002.pdf`, `05-Site-Reports/SR-2026-06-03.pdf`, `06-Site-Photos/IMG_3021.jpg`.
- Expected (F02): **Matched**. CO-002 was signed by both parties on 2026-05-25 for 20 units at the contract rate of $200, which is $4,000.00. The site report and the dated photo (EXIF 2026-06-03, GPS at the Alpha site) back it up. Every point cites a source file.

**Test 2 — Undocumented additional work (core)**
- Prompt: *"Check invoice INV-010 in Project Alpha against the contract, change orders, meeting recordings and site records."*
- Input: contract, `03-Invoices/INV-010.pdf`, `02-Change-Orders/CO-004_Additional-Doors.pdf` (not signed by the client), `04-Meetings/REC-2026-10-12.m4a`, `05-Site-Reports/SR-2026-10-15.pdf`, `12-Deliveries/DN-5531.pdf`, `08-site diary/Diary 09.10.2026.pdf`, photos IMG_3377 and IMG_3412.
- Expected (F07): **Missing evidence**, plus **Review** for the amount.
  - Doors are excluded from the contract.
  - "No approval evidence found in the accessible project records."
  - The invoice is $6,000.00 above the unsigned $2,500.00 change order.
  - The recording is a request, not an approval.
  - The 13 Oct email cited in the site report is missing.
  - The doors were delivered on 9 Oct, before the 12 Oct request.
  - Project Gamma CO-004 (a signed doors change order on another project) must not be used as approval.
  - A human should verify the invoice.

**Edge case — Conflicting evidence**
- Prompt: *"Check invoice INV-004 in Project Alpha."*
- Input: `CO-006_Extra-Concrete-Work_RevA.pdf`, `CO-006_Extra-Concrete-Work_RevB.pdf`, `INV-004.pdf`, `REC-2026-07-14.m4a`, `SR-2026-07-20.pdf`.
- Expected (F08): **Conflicting**. There are two signed revisions: Rev A for $5,200.00 and 40 m², and Rev B for $6,100.00 and 48 m². The recording gives a different approval date (9 July). The site report says 48 m² was placed. The invoice cites Rev A. **No version is chosen**; the item is marked for review.

## Additional tests (new in v2)

| Test | Prompt | Expected | Finding |
|---|---|---|---|
| T4 Email-only approval | "Is INV-006 approved?" | **Review**. Approval exists only in the 6 Aug email ($2,600.00). The CO-009 that clause 4.5 requires was not found. Must **not** say "no approval evidence". | F13 |
| T5 Late notice / date problem | "Check INV-008." | **Review**. The amount matches signed CO-008 ($4,400.00). Notice came 17 days after 18 Aug (clause 4.6 allows 7). Removal started 24 Aug, before the 10 Sep signature. No time-bar or entitlement conclusion. Scanned file: if it can't be read, say Insufficient data. | F14 |
| T6 Excluded work | "Check INV-009." | **Missing evidence**. Feature painting is excluded, and no change order covers it. | F15 |
| T7 Quantity over contract | "Check payment application PA-03." | **Review** for walls: 230 vs 200 m², $1,800.00, no change order, verbal request only; the 250 m² in the tender schedule is superseded. **Review** for ceilings: 300 m² claimed although CO-007 omits 150 m², $3,750.00 (already withheld in PC-03). | F16, F17 |
| T8 Delayed payment | "Was PA-03 certified on time?" | **Review**. Certified 26 days after the application; clause 3.3 allows 14. Dates only, no breach claim. | F18 |
| T9 Trap: looks like a duplicate | "Is INV-007 a duplicate of INV-002?" | **Matched**. It is a separate signed change order (CO-010, Level 1). | F04 / TP-2 |
| T10 Trap: excluded but approved | "Check INV-003." | **Matched**. Floor finishes are excluded, but signed CO-003 adds them. | F03 / TP-1 |
| T11 Trap: retention | "Was PA-02 paid short?" | **Matched**. $44,000.00 gross − 5% retention − $14,250.00 = $27,550.00. | F06 / TP-3 |
| T12 Insufficient data | "What does Voice 031 say about approvals?" | **Insufficient data**. 2.5 s of noisy speech; nothing may be inferred. (Whisper small.en invented a sentence for it during verification.) | F19 |
| T13 Photo location | "Do the photos support the Level 2 doors?" | IMG_3412 supports them. IMG_3460 is **Review**: its GPS is ~5 km away, at the Gamma site. IMG_5521 is **Insufficient data**. | F20, F12 |
| T14 Scoping | "Audit Project Beta" / "Audit Project Gamma" | All invoices Matched. No Alpha files cited. Same invoice numbers (INV-001, INV-004, INV-010) are handled per project. | B1, B2 |

## Full audit (Round 2 and dry runs)
Prompt: *"Audit Project Alpha. Compare the original contract, all change orders, payment applications, correspondence, meeting recordings, site records and invoices. Find invoiced or claimed work without documented approval, duplicate charges, quantity or price differences and conflicting records, and show the evidence for every finding."*
Expected: F01–F20. Totals: invoiced $38,050.00, matched $13,000.00, flagged $25,050.00, amount without approval evidence $11,650.00. PA-03 gross over-claim is $5,550.00. The report is saved only **after confirmation**.

## Round 2 — demo plan (video under 3 minutes)
1. *"Check invoice INV-010 in Project Alpha…"* (about 60 s): shows the main finding and the evidence ledger, with Gamma's CO-004 left out.
2. *"Check invoice INV-004."* (about 35 s): shows the conflict handled without choosing a version.
3. *"Is INV-006 approved?"* (about 25 s): shows approval found in an email, not wrongly called missing.
4. *"Audit all of Project Alpha."* (about 40 s): shows the summary totals.
5. Approve saving the report and show where the file was saved (about 20 s).

## Dry-run protocol (before the NAS is available)
1. Give the assistant under test only `SKILL.md` and `nas-upload/`. If the recordings can't be transcribed, paste `ground-truth/transcripts/` text **only** to test reasoning, and say that you did.
2. Never show it `ground-truth/`.
3. Score the output with `ground-truth/SCORING_SHEET.md`, rerun two or three times, and keep every score.
4. Report these as **dry-run results**, not NAS-validated results.

## v1 → v2 mapping
| v1 | v2 | Note |
|---|---|---|
| INV-001 (contract electrical) | PA-01 | Contract items are now claimed by payment application |
| INV-002, INV-003, INV-004 | INV-001, INV-002, INV-003 | Same change orders |
| INV-005 doors | INV-010 | Same scenario, plus delivery note, Gamma trap and Beta number collision |
| INV-006 concrete conflict | INV-004 | Unchanged scenario |
| INV-007 duplicate | INV-005 | Description now worded differently |
| F08, F09, F10 of v1 | F10, F11, F12 | Unchanged |
