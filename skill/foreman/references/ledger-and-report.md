# Claim-to-Evidence Ledger and report

Read this before building findings (Stage 5) and the report (Stage 6). The output format is fixed before the investigation starts and does not change with the results.

## 1. Ledger row (one per finding)

Row rules:
- Every invoice gets one row, including Matched ones. If one invoice has several lines with different results, give each line that raises a finding its own row (target "INV-012 line 2").
- Every payment application gets one row for the application as a whole (arithmetic, retention, previously certified). Each line that raises a finding gets its own extra row (target "PA-03 item 3"). The application row is Matched only when its arithmetic is correct and none of its lines raised a finding. Otherwise it takes the most serious **primary** class among its own checks and its line rows (Conflicting, then Missing evidence, then Review, then Insufficient data), and points to those line rows.
- Every non-claim risk from [evidence-rules.md](evidence-rules.md) section 4 gets a row.
- Matched rows are kept, so a reviewer can see what was checked.

| Field | Content |
|---|---|
| ID | F01, F02, … in report order |
| Target | The claim or record, for example "INV-010", "PA-03 item 3", "CO-005", "IMG_5521.jpg" |
| Claim | What is asked: description, quantity, rate, amount, date |
| Scope basis | The contract item it falls under (item, quantity, rate, value), or the exclusion it falls under, or "not a contract item" |
| Change basis | Change order number and revision, amount, signature status for each party with dates |
| Approval evidence | Evidence type, date, who, and the short quote that matters |
| Discussion | Recording or minutes, timestamp, one-sentence quote |
| Reported work | Site report, diary, delivery note or photo, with date |
| Missing evidence | What was looked for and not found |
| Checks and calculation | The ladder steps that raised something, with the arithmetic written out |
| Class | Primary class, plus any "also" class |
| Amount at issue | The amount the finding concerns: the difference, the excess or the full claim, labelled |
| What the records show | Two or three plain sentences, following the wording rules |
| Recommended action | One concrete human verification step |
| Sources | Exact file path of every cited record, with page or timestamp where available |

## 2. Registers

1. **Project Overview.** Project name, confirmed folder, contract number and date, parties, contract sum, contract sum adjusted by signed change orders (additions and omissions listed), number of records found by type, records not used and why, report date, the model mode the user confirmed.
2. **Original Scope Register.** Item, description, quantity, unit, rate, value; exclusions; the payment, retention, change, notice and certification clauses quoted, with path and page.
3. **Change-Order Register.** Number, revision, date issued, description, amount (omissions negative), signature status for each party with dates, evidence type, status (formal approval / not signed / conflicting revisions / written approval only), stated reason, claims that cite it.
4. **Evidence Timeline.** Date, event, evidence type, people, source path. Oldest first, one line per event.
5. **Missing Evidence.** Each item that was referenced or required but not found, where it was expected, which finding it affects.
6. **Coverage and limits.** Files that could not be read, OCR used, transcripts with warnings, photos without metadata, cross-check disagreements, files listed but not used, and what Foreman does not judge.

## 3. Totals

Compute every total from the Ledger, show its formula, and label claims and payment applications separately:
- Total invoiced: the sum of all invoice totals, including invoices with findings. An invoice whose amount could not be read is listed by number beside the total ("plus INV-xxx, amount unreadable") and never estimated.
- Invoices Matched / flagged (any class other than Matched).
- Amount without approval evidence: the full amount of each invoice whose finding carries the required sentence, plus the excess value of each payment-application line that carries it. Non-claim rows (for example an unsigned change order not yet invoiced) are listed but not added.
- For each payment application: claimed due, the amount the findings dispute, and the due amount recalculated without the disputed lines (gross − disputed, less retention, less previously certified).

## 4. Report template

```markdown
# Foreman investigation report — {project name}

Prepared from the accessible records in {confirmed folder} on {date}. This report identifies documentary discrepancies for human review. It is not a legal or financial decision.

## Summary
- Claims checked: {n} invoices, {n} payment applications. Ledger rows: {n} Conflicting, {n} Missing evidence, {n} Review, {n} Insufficient data, {n} Matched (every row counted once by its primary class, including application rows and non-claim rows).
- Total invoiced {amount}; Matched {amount}; flagged {amount}; without approval evidence {amount}.
- Most important actions: {up to three, one line each}.

## Findings that need review
{Ledger rows, ordered Conflicting, Missing evidence, Review, Insufficient data. Each as a short block: ID, target, class, amount at issue, what the records show, evidence chain, sources, recommended action.}

## Matched claims
{Compact table: ID, target, basis, amount, sources.}

## Evidence timeline
{Table: date, event, evidence type, source.}

## Missing evidence
{List.}

## Registers
{Project overview, original scope register, change-order register.}

## Coverage and limits
{List.}

## Next human actions
{Numbered list, most urgent first.}
```

Formatting rules:
- Money with currency symbol, thousands separator and two decimals ($1,800.00). Dates as YYYY-MM-DD in the report, whatever format the source used.
- Every finding block ends with its source paths, one per line.
- Keep each "what the records show" to three sentences or fewer. Detail goes in the evidence chain.
- Do not include agent names, CLI names or internal status values in the report.
