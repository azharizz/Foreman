# Foreman synthetic test dataset — version 2

A fully **synthetic** construction archive with three projects, for testing the Foreman Skill: Round 1 dry runs and proposal test cases, and Round 2 (the single NAS day and the demo video).

- All parties, people, addresses, GPS coordinates and amounts are fictional or arbitrary.
- Every document carries a "SYNTHETIC TEST DATA" marker, and every photo is labelled "SYNTHETIC ILLUSTRATION - NOT A REAL PHOTO".
- No real documents, third-party datasets, company names or trademarks are used.
- v1 (`../dataset/`) is untouched.

**This dataset is not part of the Skill package.** The Skill ZIP may contain only `SKILL.md` and `references/` files. Never put any of this folder in the ZIP.

## Folder map

| Path | Purpose | Upload to NAS? |
|---|---|---|
| `nas-upload/Project-Alpha/` | Main audited project: 59 files. Contract and a superseded tender schedule, 10 change orders, 10 invoices (one scanned), 3 payment applications and 1 certificate, 5 recordings, 5 weekly reports, 4 daily diaries, 9 photos, 3 email threads, 2 RFIs, a drawing/spec register, 3 delivery notes, 1 irrelevant file | **Yes** |
| `nas-upload/Project-Beta/` | Distractor from a different contractor: invoice numbers INV-001 and INV-010, a signed CO-004, and a client rep named "Maya Lindgren". All of these collide with Alpha. | **Yes** |
| `nas-upload/Project-Gamma/` | Distractor from the same contractor and PM: a second `CONTRACT-001`, a **signed** doors CO-004, INV-004, and `SR-2026-10-15` again | **Yes** |
| `ground-truth/` | `ANSWER_KEY.md`, `answer_key.json`, `SCORING_SHEET.md`, `transcripts/` (audio scripts) | **No**, and never show it to the AI under test |
| `alt-formats/` | `.wav` copies of every recording; `.eml` copies of the email threads | **No** (they would look like duplicates) |
| `real-photo-slot/` | Where real photos can be added later (3 empty slots, also listed in `MANIFEST.csv`) | — |
| `TEST_CASES.md` | Round 1 tests, 11 more tests, demo plan, v1→v2 mapping | — |
| `MANIFEST.csv` | Every file with project, kind, date, role, SHA-256 and size | — |
| `VERIFICATION.md` | What was checked, the results, and known weaknesses | — |
| `tools/` | `generate_dataset.py` (builds everything), `verify_dataset.py` (re-derives findings from the files), `ocr_vision.js`, `requirements.txt` | — |

## What is planted (details and exact paths in the answer key)

| Cause (PRODUCT_FOREMAN §6.4) | Planted item |
|---|---|
| Owner-directed change, signed | CO-001/INV-001, CO-002/INV-002, CO-010/INV-007: Matched |
| Owner-directed deduction (removes work) | CO-007 −$3,750; PA-03 still claims the full ceiling (F17) |
| Unforeseen site condition plus late notice | Asbestos: diary 18 Aug, notice 4 Sep, removal before signature; scanned INV-008 (F14) |
| Design error or omission | RFI-014 → A-102 Rev C → fire-rated upgrade approved **only by email** (F13); RFI-017 → duct clash → CO-005 not signed (F10) |
| Verbal instruction never formalised | Extra walls (noisy recording plus diary, F16); ducts (F10); doors request (F07) |
| Revised change order | CO-006 Rev A/B, both signed, conflicting (F08) |
| Delayed or disputed payment | PC-03 certified 26 days after PA-03; email chase (F18) |
| Quantity or price disagreeing with the contract | PA-03 walls 230 vs 200 m² (F16); INV-010 $8,500 vs $2,500 (F07) |
| Invoice for excluded work | INV-009 feature painting (F15) |
| Duplicate billing | INV-005 repeats INV-001 (F09) |
| Insufficient data | Undated photo IMG_5521 (F12); 2.5 s unclear `Voice 031.m4a` (F19) |
| Photo location conflict | IMG_3460 is in the Alpha folder but has GPS at the Gamma site (F20) |
| False-positive traps | Excluded-but-approved INV-003; look-alike INV-007; retention on PA-02; negative CO-007; superseded tender schedule; Beta/Gamma collisions |

**Realistic mess:**
- Mixed file naming (`CO_008 ACM removal.pdf`, `co-005_hvac_reroute.pdf`, `SiteDiary 24 Aug 26.pdf`).
- Mixed date formats (2026-09-04, 04.09.2026, 18/08/2026 and 24 Aug 2026; all unambiguous).
- Typos ("Additonal", "recieved").
- Folder names with spaces.
- A superseded schedule in `01-Contract/from-tender/`.

File names never contain status words such as SIGNED, DRAFT or DUPLICATE. Status appears only inside the documents and their metadata.

## What it can and cannot test

- **Can test:**
  - The Skill's investigation logic, classification, wording, evidence citation and project scoping, against a known answer.
  - Whether a pipeline reads a scanned PDF, noisy audio, EXIF dates and GPS.
- **Cannot test:**
  - Real-world accuracy.
  - UGREEN's actual OCR, transcription or photo AI. Nothing here has been run on a UGREEN NAS.
  - Real photos (the images are drawings).
  - Real meeting audio (the voices are synthetic, mixed with synthetic noise).
  - Scale beyond about 70 files.

Passing on this dataset is a **dry-run result**, not evidence that UGREEN's tools perform well.

## Using it

- **Round 1:** dry runs with `SKILL.md` and `nas-upload/` only. Score with `ground-truth/SCORING_SHEET.md`.
- **Round 2 (one NAS day):**
  1. Upload the contents of `nas-upload/` on the day. **[Verify]** the upload method in the finalist instructions.
  2. Keep `ground-truth/` and `alt-formats/` off the NAS.
  3. Run the prompts in `TEST_CASES.md` while recording the screen.
  4. Back up results before the data is reset.

## Regenerating (deterministic, seed 20261104)

```
python3 -m venv "$SCRATCH/venv" && "$SCRATCH/venv/bin/pip" install -r tools/requirements.txt
"$SCRATCH/venv/bin/python" tools/generate_dataset.py .
"$SCRATCH/venv/bin/python" tools/verify_dataset.py . "$SCRATCH" [whisper_txt_dir]
```

- Use a scratch folder outside the project for the venv.
- Requires macOS (`say`, `afconvert`, `osascript`), plus `ffmpeg` and poppler.
- Regenerating rewrites `nas-upload/`, `alt-formats/`, `MANIFEST.csv`, `ground-truth/answer_key.json`, `ground-truth/ANSWER_KEY.md` and `ground-truth/transcripts/`. It keeps the hand-written docs and `SCORING_SHEET.md`.
- Back-to-back runs on this machine gave byte-identical files, audio included. Across separate sessions, macOS `say` occasionally produces slightly different audio (seen once: `REC-2026-10-12.m4a` came out 0.01 s shorter, with the same words). All documents, photos, amounts and dates are fully deterministic; audio hashes may differ between runs or Macs.
