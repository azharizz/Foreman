# Foreman — AI Construction Scope & Change-Order Investigator

Track: Open Innovation

## 1. What does the Skill do?

Foreman investigates a construction project folder on UGREEN AI NAS. It links every invoice and payment claim to the contract, change orders, correspondence, recordings and site photos, and flags unapproved, duplicated, mismatched or conflicting charges with exact source files.

## 2. Who is the target user and problem?

Contractors' project managers, contract administrators and quantity surveyors. Extra work is often instructed verbally and invoiced weeks later, while the evidence sits scattered across contracts, emails, recordings and photos. Disputes are costly: Arcadis's 2026 report (United States, 2025 data) gives an average claimed dispute of US$56.0M lasting 12.2 months.

## 3. What is your proposed solution?

A Claim-to-Evidence Ledger. For every claim, Foreman connects five records:
- what was agreed (the contract);
- what was formally changed (change orders and written approvals);
- what was discussed (recordings);
- what was reported (diaries, delivery notes, photos);
- what is billed.

Each finding gets one of five classes (Matched, Review, Missing evidence, Conflicting, Insufficient data), an amount and source paths.

## 4. What is the Core User Flow?

The user says "Audit Project Alpha" and confirms the folder and model mode. Foreman then:
1. Lists the files and identifies each document by its content.
2. Builds the scope and change-order registers.
3. Transcribes the recordings and reads photo dates and GPS.
4. Reconciles every claim with a fixed eight-step ladder.
5. Shows the report; saves it only after confirmation.

## 5. What substantive difference does your idea offer?

It is not document Q&A. It reasons across record types and over time, and keeps formal approval separate from discussion. It never chooses between conflicting versions. It writes "No approval evidence found in the accessible project records" instead of guessing. It never alleges fraud or decides entitlement.

## 6. Which UGREEN AI NAS capabilities will be used, and at which step?

- **Files** (`ug-filesystem`, file-agent): discovery.
- **Documents** (`ug-document`, document-agent): typing documents and reading the contract, change orders, correspondence and claims.
- **Knowledge** (`ug-knowledge`, knowledge-agent): transcribing recordings, and saving the report after confirmation.
- **Albums** (`ug-photo` meta, photo-agent): photo dates and locations.

## 7. What was your technical approach?

`SKILL.md` is an orchestration-only Skill. It sends ten self-contained delegations to four registered experts, and each stage uses only real upstream results.
- **Inputs:** the project folder and the request type.
- **Permissions:** read-only, plus one save that needs approval.
- **Model and data:** local model recommended; cloud data flow disclosed; no external services.
- **Errors:** all five delegation states are handled. Unreadable scans or recordings become Insufficient data.

## 8. What is the current development status?

Built:
- `SKILL.md` and two reference files, passing the official checker (static-pass, no warnings).
- A synthetic archive: three projects, 71 files, 20 planted findings.
- Dry runs on simulated expert results (Claude Haiku and Sonnet standing in for Uliya's model): after two fix rounds, all audits passed with exact amounts and no false positives.

Pending: execution on the NAS.

## 9. What is your final validation plan?

- **Core 1:** INV-002 matches signed CO-002.
- **Core 2:** INV-010 bills $6,000 above an unsigned change order that only a meeting supports. Missing approval evidence must be reported.
- **Edge:** INV-004 cites one of two signed, conflicting revisions. It must be marked Conflicting without choosing.

Pass lines are fixed before testing.

## 10. Are there any known limitations?

OCR, transcription and local-model reasoning on the iDX6011 Pro are unverified. Photos are used for metadata only. The test data is synthetic. Foreman gives no legal judgement.

---

**Team:** {TEAM_NAMES} (team representative: {TEAM_REPRESENTATIVE})

**Third-party components and data flows** (outside the word limit): the Skill includes no third-party code, models, APIs or datasets. Processing uses only Uliya's registered experts and the model the user selects in Uliya; in cloud mode, content may be sent to that provider. The test data is entirely synthetic and created by the team. The Skill was built with the official UGOS Skill Creation Tool v0.7.3. An AI coding assistant was used for drafting, and dry runs used Claude models as stand-ins for the Uliya model.
