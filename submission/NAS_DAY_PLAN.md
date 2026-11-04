# Foreman — NAS day plan (Round 2, one assigned 24-hour day between Nov 22 and Nov 28)

The NAS is available only from 12:00 a.m. to 11:59 p.m. **Pacific Time** on the assigned day: 15:00 WIB that day to 14:59 WIB the next day. Credentials work only on that day, and everything is reset afterwards. Everything below is prepared beforehand so the day is spent testing, not setting up.

## Before the day (Nov 21, after the finalist email)

1. **Read the finalist email.** Note the assigned date, the activation and expiry times, the connection method and the upload method. **[Verify]**: web file manager, SMB or other.
2. **Prepare the upload set.** Put the contents of `dataset-v2/nas-upload/` (71 files, about 3 MB) in a separate folder, plus a copy with spaces removed from all file names, in case the NAS tools reject them.
3. **Prepare fallback media.**
   - `dataset-v2/alt-formats/*.wav`, in case `.m4a` transcription fails.
   - `alt-formats/*.eml`, in case printed-email PDFs are not read.
   - Upload these only if needed: they duplicate records and would add noise to the audit.
4. **Prepare the Skill.** Make `foreman.zip` from `skill/foreman/` at the Round 1 version plus any fixes. Keep the Round 1 ZIP unchanged; the rules require Round 1 materials to be kept.
5. **Gather the materials to have open on the day.** Print or have open `dataset-v2/ground-truth/SCORING_SHEET.md`, the prompts below, and an empty results sheet.
6. **Plan the recording.** Screen recorder ready, 1080p, microphone checked. Narration is in English (or full English subtitles).

## On the day — run order (times in hours after access opens)

| Time | Step | Done when |
|---|---|---|
| 0:00–0:30 | Log in, check the NAS and Uliya, set Uliya to the **local model**, note the model name and version | Screenshot of the settings |
| 0:30–1:00 | Upload `nas-upload/` into one folder (for example `Foreman-Test`), keeping the subfolders | File count is 71 |
| 1:00–1:30 | Install the Skill ZIP through the official route; confirm Uliya lists Foreman | Screenshot |
| 1:30–2:30 | **Smoke test:** "Check invoice INV-002 in Project Alpha. The project folder is Foreman-Test/Project-Alpha." | Report shows INV-002 Matched |
| 2:30–5:00 | **Capability probes.** One short prompt per expert, to see real behaviour: file listing, document typing, the scanned INV-008, one `.m4a` transcription, photo metadata for IMG_3460 and IMG_5521, and a save to a test folder | Each probe's output saved |
| 5:00–9:00 | **Full audit, local model, run 1.** Score it with the scoring sheet and save the full output | Score recorded |
| 9:00–12:00 | Fix `SKILL.md` wording if a probe or the audit shows a problem; reinstall; **full audit, run 2** | Score recorded |
| 12:00–14:00 | Scoped runs: "Audit Project Beta", "Audit Project Gamma"; single-claim runs for INV-010 and INV-004 | Scores recorded |
| 14:00–17:00 | **Demo recording** (script below), several takes | At least one good take |
| 17:00–20:00 | Optional: one full audit with a cloud model (only if allowed; disclose it) for comparison | Score recorded |
| 20:00–23:00 | **Back up everything:** reports, run logs, screenshots, the final Skill, scores. Download saved reports from the NAS | Files on your laptop |
| 23:00 | Stop. Data is reset at the end of the day | — |

If a capability probe fails:

| Problem | Fallback |
|---|---|
| Scanned PDF unreadable | Expected; the Skill reports Insufficient data. Note it as a limitation |
| `.m4a` not transcribed | Upload the `.wav` copies and rerun Stage 4 only |
| Photo metadata not read by path | The Skill already falls back to a folder search; if both fail, record it as a limitation |
| File names with spaces rejected | Use the renamed copy |
| Save fails | The report stays in chat; copy it out manually and record the failure |

## Results sheet (fill in on the day)

Run · model · prompt · start/end time · classes per finding F01–F20 · totals · forbidden-language hits · false positives · notes.

## Demo video script (under 3 minutes, English)

| Time | Show | Say |
|---|---|---|
| 0:00–0:15 | The project folder on the NAS: contract, change orders, invoices, recordings, photos | "A construction company keeps every project record on its UGREEN NAS. Foreman checks whether what is being billed was ever approved." |
| 0:15–0:30 | Typing "Audit Project Alpha…"; Foreman's confirmation question about the folder and the local model | "It asks before reading anything, and it runs on the local model, so the contracts and prices stay on the NAS." |
| 0:30–1:15 | The INV-010 finding: $8,500 billed, unsigned CO-004 for $2,500, the meeting where the client only asked for a quote, the missing 13 Oct email, and the delivery note dated before the request | "Every finding links back to the exact files. Foreman never says 'fraud'. It says 'No approval evidence found in the accessible project records', and tells you what to check." |
| 1:15–1:45 | The INV-004 conflict: two signed revisions with different amounts | "When records disagree, it does not pick a winner. A person decides." |
| 1:45–2:05 | INV-006: approval found only in an email | "It also knows the difference between no approval and approval that only exists in an email." |
| 2:05–2:30 | The summary totals and the Matched claims (the traps) | "It also shows what checks out, so reviewers can trust what it flags." |
| 2:30–2:50 | The save confirmation, then the saved report path in the project folder | "Nothing is written without your approval. The report is saved back to the project archive." |
| 2:50–3:00 | Closing | "Foreman: know what changed, what was approved, and what you are paying for." |

Show only real output from the NAS run. If a step did not work on the NAS, leave it out of the video rather than staging it.
