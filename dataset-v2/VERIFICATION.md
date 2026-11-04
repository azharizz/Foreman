# Verification — dataset v2 (2026-11-04)

Run with `tools/verify_dataset.py`, which reads only the files in `nas-upload/` (pdftotext, OCR, EXIF, ffprobe) and re-derives the findings with its own rules. It then diffs them against `ground-truth/answer_key.json`. Result: **0 problems**.

## What was checked

| Check | Method | Result |
|---|---|---|
| Text and numbers in every PDF | `pdftotext -layout` on all 56 PDFs. The scanned `INV-008.pdf` has no text layer, so it was OCR'd with macOS Vision (`tools/ocr_vision.js`) | Contract items, change-order amounts, signatures, invoices, PA arithmetic and PC-03 all parsed and match the key |
| Findings re-derived from files | Independent rules: invoice → its change order (signed? revisions? duplicate? work started before signature?), email approval search, contract exclusions, PA quantities vs contract less signed omissions, date gaps vs the contract's own day limits, unsigned uninvoiced CO, referenced-but-missing email | **20 of 20** findings match the key (class and amount) |
| Totals | From the parsed files | Invoiced $38,050.00, matched $13,000.00, flagged $25,050.00, PA-03 due $33,345.00, PC-03 $29,782.50, contract $77,300.00: all equal to the key |
| Totals in code | `generate_dataset.py` asserts every total, the PA arithmetic and the date gaps (17 and 26 days) | Pass |
| Evidence paths | All 75 paths cited in the key exist | Pass |
| Distractors | Beta 4/4 and Gamma 2/2 invoices match their own contract or signed CO | Pass |
| EXIF | piexif on all 10 JPGs | Dates as in the key. Alpha photos are within 0.06 km of the Alpha GPS point; IMG_3460 is 5.01 km away (0.05 km from Gamma's point); IMG_5521 has no EXIF |
| Audio durations | ffprobe | 45.8 s, 23.5 s (noisy), 27.2 s, 23.4 s, 2.55 s (`Voice 031`) |
| Transcription | whisper `small.en` on all 5 recordings, compared with `ground-truth/transcripts/` (approximate word error rate; inflated by number formatting such as "14th" vs "fourteenth") | See below |
| Markers | "SYNTHETIC TEST DATA" in every PDF (including the OCR'd scan), in photo pixels and EXIF, in audio metadata, and in an `.eml` header | Pass |
| Hint words in paths | Regex for signed, draft, duplicate, approved, final, superseded, missing, copy, etc. over all `nas-upload/` paths | None found |
| Answer-key leak | Regex for answer key, expected class, false positive, F01…, TP-…, forbidden, ground truth over all PDF text | None found |
| Determinism | Generated twice and compared SHA-256 of every file | Identical, audio included |

**Whisper small.en results**

| Recording | Error ≈ | What was lost |
|---|---|---|
| REC-2026-07-14 | 7% | "Maya, Priya" heard as "my kriya"; facts intact |
| REC-2026-08-12 site walk (noise + overlap) | 16% | "August" heard as "order", so the date survives only in the file name. The overlapped "Thirty square meters" and "Right" were dropped. Key facts (30 m², $1,800, "just do it… paperwork later") were kept. base.en gave the same result |
| REC-2026-09-22 | 11% | Facts intact |
| REC-2026-10-12 | 3% | Facts intact |
| Voice 031 | 82% | Whisper **invented** "That's one of the problems." This supports the Insufficient data expectation (F19), and the risk of a confident wrong transcript is real |

## Known weaknesses

- **The verifier is not a second reviewer.** It reads only the files, but the same person wrote both it and the generator, so shared blind spots are possible. No independent person has tried to break this dataset yet. That is still the biggest gap.
- **OCR gets one number wrong.** Vision read the scan's total as `$4.400.00`; the verifier tolerates this. A weaker OCR engine may fail outright, and the key allows "Insufficient data (unreadable)" for that case. The scan is only moderately degraded (1.6° rotation, noise, blur).
- **Audio is synthetic speech with synthetic noise.** Whisper copes well even at high noise, so real site recordings will likely be harder. Overlap is simulated by mixing two TTS voices.
- **Photos are drawings.** They test EXIF and GPS handling, not image understanding. The `real-photo-slot/` is still empty.
- **GPS coordinates are arbitrary land coordinates**, not linked to the fictional addresses. A photo app may show a real place name for them.
- **Some classes are judgement calls.** F13 (email approval without the follow-up CO) and F14 (amount matches but dates breach the procedure) are set to Review. F16 also accepts Missing evidence. Reasonable reviewers could disagree, so keep these fixed before testing and don't move them after.
- **Not run on a UGREEN NAS.** Format support (`.m4a`, image-only PDF, file names with spaces) and the real capability outputs are unverified.
- **Small scale.** 71 archive files in three projects. It shows the investigation, not performance at archive scale.
