# Round 1 submission checklist

Deadline: **Sun 15 Nov 2026, 11:45 pm PT** (= Mon 16 Nov, 14:45 WIB). Target: submit by **14 Nov**.

Live Devpost rules and updates were re-checked on 2026-11-04: no change from the saved copy. **Re-check again on submission day**: https://ugreenhackathon.devpost.com/rules and /updates.

## You must do (cannot be automated)

- [ ] Fill `{TEAM_NAMES}` and `{TEAM_REPRESENTATIVE}` in `PROPOSAL.md` (up to 3 people; the representative receives the finalist email).
- [ ] Read the proposal once in your own words. The FAQ says "be human where it counts". Edit freely, but keep the answers at 500 words or fewer (the builder checks this).
- [ ] Build the final PDF: `python build_pdf.py PROPOSAL.md Foreman_Proposal.pdf`. It refuses to build with unfilled fields, more than 500 words, or more than 1 MB.
- [ ] On Devpost: pick the track **Open Innovation** (the gallery form calls it "Explore Your Imagination"; confirm the label on the form), upload `Foreman_Proposal.pdf` and `foreman.zip`, and fill the form fields.
- [ ] Keep the submitted PDF and ZIP unchanged after the deadline. The rules say Round 1 materials must be retained.

## Already verified (2026-11-04)

| Item | Requirement | Status |
|---|---|---|
| `foreman.zip` | 10 MB or less; contains only `SKILL.md` and `references/*.md`; no scripts or manifests | 14.6 KB; 3 files under `foreman/` |
| Official checker on the ZIP contents | static checks pass | `static-pass`, 0 errors, 0 warnings, 0 info |
| `name` | lowercase, hyphenated, 2–64 characters | `foreman` |
| `description` | 1,024 characters or fewer | 703 |
| Every reference linked from SKILL.md | required | yes |
| No credentials, personal data or third-party material | required | yes (synthetic, fictional) |
| Proposal answers | 500 words or fewer | 489 |
| Proposal PDF | 1 MB or less | about 6 KB |
| Third-party disclosure | required in the proposal | present (outside the word count) |

## Files

| File | Use |
|---|---|
| `PROPOSAL.md` | Proposal source (edit this) |
| `Foreman_Proposal_DRAFT.pdf` | Draft render with the team fields marked [TO FILL] |
| `build_pdf.py` | Builds the final PDF and checks the limits |
| `foreman.zip` | The Skill package to upload (built from `skill/foreman/`) |
| `NAS_DAY_PLAN.md` | Round 2 plan, fallbacks and demo script |

Rebuild the ZIP after any Skill change: `cd skill && zip -X -r ../submission/foreman.zip foreman -x '*.DS_Store'`, then run the checker on it.
