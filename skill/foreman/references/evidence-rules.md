# Evidence rules

Read this before reconciling claims (Stage 5). It defines how each record is weighed, how each claim line is classified, and what may and may not be said. The project's own contract is always the rulebook: use only clauses returned by the contract extraction, never a generic standard form.

## 1. Evidence types

Give every statement about a change exactly one type. The type decides what the statement can prove.

| Type | What counts | Can prove approval? |
|---|---|---|
| Formal approval | A change order or other instrument the contract names, signed by every party the contract requires, with dates | Yes |
| Written approval | A letter or email from the person the contract authorises (usually the client's representative) that explicitly approves defined work at a stated price | Yes, but check what the contract says must follow it |
| Discussion | A recording or minutes where a change is requested, priced, estimated or discussed | No |
| Reported instruction | A site report or diary that says someone instructed the work, usually verbally | No |
| Reported work | A site report, diary, delivery note or photo showing work done or materials delivered | No; it shows what happened, not who approved it |
| Claim | An invoice line or payment application line | No; it is what is being checked |
| Superseded or draft | A document that says it is a draft, for discussion only, replaced or superseded | No; it is context only, never the contract basis |

A change order missing any required signature is **not** formal approval, however complete it looks. An estimate or "I will review it" is not approval. "Go ahead, we will sort out the paperwork later" is a reported or recorded instruction, not approval, unless the contract says verbal instructions are binding.

## 2. The five classes

| Class | Use when |
|---|---|
| **Matched** | The claim agrees with the contract item or a formal or written approval in description, quantity, rate and amount, and no check below raised a finding |
| **Review** | A discrepancy needs human verification: amount or quantity difference, possible duplicate, dates outside the contract's own rules, approval found but its required follow-up not found, or two extraction results that disagree |
| **Missing evidence** | Required supporting evidence was not found: no approval for changed or excluded work, a referenced document that is not in the folder, a change order lacking a required signature |
| **Conflicting** | Two or more records disagree on the same fact (two signed revisions, different approval dates or amounts) and no record says which one governs |
| **Insufficient data** | The record cannot be read or is too thin to compare: unreadable scan, failed or empty transcript, photo without a date, no executed contract |

Each finding has one **primary class** and, where a second check also raised something, an **also** class (for example "Missing evidence, also Review for the amount").

## 3. Reconciliation ladder for each claim line

Run every step for every claim line. The **first** step that raises a finding sets the primary class; later steps that raise something become "also" classes and are described in the same finding.

1. **Readable?** If the claim document could not be read, or its amount is uncertain after OCR, the line is Insufficient data. Report the file and stop this line. Never estimate an amount.
2. **Reference exists?** Find what the line cites: a contract item, a change order (and revision), a written approval or a quote. If **none** of the cited documents is among the discovered files, the line is Missing evidence; when the missing document was the approval basis, add the required sentence. If some cited documents exist and others do not (for example an approval email exists but its attached quote does not), continue the ladder and list the missing ones under Missing evidence without changing the class.
3. **Approval basis.**
   - a. The cited change order has two or more signed revisions with different scope or amount, and no later record states which one governs → **Conflicting**. Show every revision, the claim's choice and the other records. Never pick one.
   - b. The cited change order lacks a required signature → **Missing evidence**, with the required sentence. Its amount is not an approved ceiling: compare the claim with it in step 4, labelled "unsigned change order amount".
   - c. There is no change order, but a written approval matches the work and price → approval evidence **exists**. If the contract requires a formal instrument to follow and none was found → **Review**. If the contract does not allow approval by letter or email at all, the result is still **Review** ("written approval found; the contract requires a signed change order, which was not found"). Never use the "no approval evidence" sentence here.
   - d. The work is changed or extra (not a contract item) and the only support is discussion, reported instruction, reported work or nothing → **Missing evidence**, with the required sentence.
   - e. The work falls under a contract **exclusion** and no formal or written approval covers it → **Missing evidence**, with the required sentence. If a signed change order covers it, the exclusion is not a finding.
4. **Amount and quantity.**
   - Claim amount differs from the approved amount, or from the contract quantity × rate → **Review**. Show the calculation.
   - For contract items, compare the claimed quantity with the contract quantity **adjusted by every signed change order, including omissions (deductions)**. If the claim exceeds it → **Review**. Value the excess at the contract rate, and add the required sentence for the excess when no approval covers it.
   - Payment applications: line value = claimed quantity × contract rate (or percentage complete × item value); gross = Σ line values; retention = the contract's percentage of gross; amount due = gross − retention − previously certified. "Previously certified" must equal the certified amounts of earlier applications found in the folder; where no certificate exists for an earlier application, compare with that application's amount due and say so. If any figure differs → **Review**. A due amount lower than gross because of retention is expected and is **not** a finding.
5. **Duplicates.** If the total billed against one change order or contract item exceeds its approved amount or quantity, or two claims cite the same reference with the same quantity and amount, the later claim is **Review** (possible duplicate). Two claims with the same amount but different signed change orders are not duplicates.
6. **Dates against the contract's own rules.** Use only time rules quoted from the contract.
   - Work recorded as started before the approval date, when the contract requires approval before work starts → **Review**.
   - Written notice of a site condition given later than the contract's notice period after the condition was first recorded → **Review**.
   - A written approval whose required follow-up instrument was not found is already raised in step 3c; add its dates and day count there instead of raising it twice.
   State the dates, the day count and the clause. Never state a legal consequence.
7. **Corroboration.** Site reports, diaries, delivery notes and photos support the timeline. They never turn a missing approval into Matched. Note relevant tensions in the finding, for example materials delivered before the recorded request.
8. **Matched** only when steps 1–6 raised nothing.

## 4. Records that are not claims

| Situation | Class |
|---|---|
| Change order not signed by every required party, work reported done or instructed, not yet claimed | Missing evidence, with the required sentence (risk of future billing without approval) |
| A record refers to another document (for example "client email of 13 October approving the work") that is not in the folder | Missing evidence. Never claim the document exists or say what it contains |
| Payment certificate or payment issued later than the period the contract sets | Review. State the dates, the day count and the clause; draw no conclusion about breach |
| Signed omission (deduction) change order | Not a finding. Record it in the Scope Register and apply it in step 4 |
| Photo with no EXIF capture date and no date in its file name | Insufficient data. Not used as corroboration. The file modified time is not a capture date |
| Photo whose GPS is more than 1 km (Foreman default) from the site reference point in the contract | Review: "Location metadata does not match the project site." Not used as corroboration |
| Photo with GPS but no site reference point in the contract | Usable for timing only; note "location not checked: no site reference in the contract" |
| Photo with a date but no GPS | Usable for timing only; note "location not recorded" |
| Recording that is empty, very short, low quality, or names no project item, quantity, amount or date | Insufficient data. Nothing is inferred from it, even if a transcript was produced |
| Document that says it is superseded or a draft | Not a finding by itself; flag it only if a claim relies on it |

## 5. Wording

Required sentences:
- Missing approval: **"No approval evidence found in the accessible project records."**
- Conflict: "These records disagree. Foreman has not chosen between them; a person needs to confirm which applies."
- Unreadable: "This file could not be read reliably, so it was not used."

Write findings as observations: "INV-010 bills $8,500.00. CO-004, the change order it cites, is $2,500.00 and has no client signature." Then why it matters, then the human action.

Never use: fraud, fraudulent, dishonest, illegal, guilty, theft, breach, "entitled", "not entitled", "time-barred", "invalid claim", "not payable", "approval does not exist", "the contractor lied". Never guess intent. Never recommend withholding or releasing payment; recommend verification steps instead, for example "Ask the contract administrator to locate the signed change order before the invoice is accepted."
