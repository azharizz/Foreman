# Foreman — Product Document

**Tagline:** Know what changed. Know what was approved. Know what you're paying for.
**Full name:** Foreman — AI Construction Scope & Change-Order Investigator
**Name history:** Called "ScopeProof" in the research chat; renamed Foreman. The name isn't tied to paper — the product works across documents, recordings and photos. **[Verify]** Foreman is a very common word (including an existing open-source tool of the same name); check UGREEN Skills Hub and trademark conflicts.
**Category:** AI Construction Project Investigation (an evidence-intelligence Skill for UGREEN AI NAS)
**Hackathon:** UGREEN Hackathon 2026 on AI NAS (Devpost)
**Primary track:** Open Innovation
**Source:** Distilled from `product_research.md` (a chat with an AI agent). Nothing here is invented beyond that chat, except where a section is explicitly marked **[Decision needed]** or **[Verify]**. The problem background (§6.4) and references (§30.1) were later supplemented with independent research from primary reports, journal papers and government sources (2026-11-04).

> **How to read this document.** Statements are tagged by confidence:
> - **[Confirmed]** — the chat attributes it to an official source (Devpost rules, UGREEN Starter Kit, UGREEN docs).
> - **[Proposed]** — our own design for Foreman. Not an existing UGREEN feature.
> - **[Interpretation]** — the chat's own strategic reasoning or hypothesis, not a fact.
> - **[Verify]** — must be checked against the real UGREEN creation-tool archive / Developer Package before we rely on it.
> - **[Illustrative]** — invented demo numbers, not real project findings.

---

## Table of contents

1. [One-paragraph summary](#1-one-paragraph-summary)
2. [The hackathon: what we are actually building for](#2-the-hackathon-what-we-are-actually-building-for)
3. [The platform: UGREEN AI NAS, UGOS, Uliya, Skills](#3-the-platform-ugreen-ai-nas-ugos-uliya-skills)
4. [Why UGREEN runs this hackathon (strategic context)](#4-why-ugreen-runs-this-hackathon-strategic-context)
5. [Product definition](#5-product-definition)
6. [The problem and its evidence](#6-the-problem-and-its-evidence)
7. [Target users and positioning](#7-target-users-and-positioning)
8. [The core product idea: Claim-to-Evidence Ledger](#8-the-core-product-idea-claim-to-evidence-ledger)
9. [NAS-native design: Project Evidence Vault](#9-nas-native-design-project-evidence-vault)
10. [Investigation workflow (6 stages)](#10-investigation-workflow-6-stages)
11. [Agent architecture](#11-agent-architecture)
12. [UGREEN capability mapping](#12-ugreen-capability-mapping)
13. [Outputs and deliverables](#13-outputs-and-deliverables)
14. [Finding classifications and trust rules](#14-finding-classifications-and-trust-rules)
15. [Worked example: Project Alpha](#15-worked-example-project-alpha)
16. [Scope: what is in and out of version 1](#16-scope-what-is-in-and-out-of-version-1)
17. [Technical constraints and design rules](#17-technical-constraints-and-design-rules)
18. [Privacy and model strategy](#18-privacy-and-model-strategy)
19. [SKILL.md specification](#19-skillmd-specification)
20. [Test plan and metrics](#20-test-plan-and-metrics)
21. [Synthetic test dataset](#21-synthetic-test-dataset)
22. [Judging criteria fit](#22-judging-criteria-fit)
23. [Risks and mitigations](#23-risks-and-mitigations)
24. [Round 1 submission plan](#24-round-1-submission-plan)
25. [Timeline and deadlines](#25-timeline-and-deadlines)
26. [Round 2 / finalist plan](#26-round-2--finalist-plan)
27. [Why Foreman: selection checks](#27-why-foreman-selection-checks)
28. [Open questions, discrepancies and things to verify](#28-open-questions-discrepancies-and-things-to-verify)
29. [Next steps](#29-next-steps)
30. [References](#30-references)

---

## 1. One-paragraph summary

Foreman is an AI **investigator** Skill for UGREEN AI NAS (running through Uliya). It connects a construction project's **original contract, change orders, meeting recordings, site photographs, and invoices** — all already stored on the user's NAS — to uncover **undocumented scope changes, missing approvals, and payment discrepancies**. It answers one expensive question: *"Are we paying for work that was never properly approved, and can we prove what actually happened during this project?"* Its signature feature is the **Claim-to-Evidence Ledger**: every finding links an invoice line to its original scope, the relevant change order, supporting meeting record, and any missing evidence, with exact source file paths. It never declares fraud or legal entitlement; it flags discrepancies for human review. It is **not** a document summarizer, a project-management tool, or a PDF auditor.

---

## 2. The hackathon: what we are actually building for

### 2.1 What this hackathon is (and is not)

**[Confirmed / chat conclusion]** This is **not** a general AI hackathon. It is a competition to make UGREEN's AI NAS more useful through a genuinely valuable, **installable AI Skill**.

| The hackathon IS about | The hackathon is NOT about |
|---|---|
| Solving real-world problems | Optimizing NAS hardware, RAID, disk performance or kernel |
| Building AI agent workflows | Generic AI applications that merely sit on a NAS |
| Developing Skills using supported NAS capabilities | Necessarily building new AI models |

Implication: a project should become **substantially more useful because it runs on the user's own storage, local compute, and personal/business data** — not just be an impressive AI app dropped onto a NAS.

### 2.2 Key facts

| Item | Value | Status |
|---|---|---|
| Total prize pool | $46,000 | Confirmed |
| Maximum finalists | 30 | Confirmed |
| Round 1 deadline | Nov 15, 2026, 11:45 PM PT (= **Nov 16, 2026, 14:45 WIB**) | Confirmed |
| Round 2 final deadline | **Nov 30, 2026, 11:45 PM PT** (= Dec 1, 2026, 14:45 WIB) | Confirmed (corrected later in chat — see §28) |
| Finalists announced | Nov 21, 2026 (announcement time not specified; emailed to team representative) | Confirmed |
| Round 2 testing window | Nov 22–28, 2026 — one assigned 24-hour remote NAS day per finalist | Confirmed |
| Winner announcement | **Not confirmed** (earlier said Dec 6; later says official page doesn't specify) | See §28 |
| Indonesia eligible | Yes (explicitly in eligible Asia-Pacific countries) | Confirmed |
| Eligibility | Individuals must be adults under local age-of-majority; teams up to **3** individuals; companies/legal entities excluded as entrants | Confirmed |

### 2.3 The four tracks

| # | Track | What UGREEN wants | Theme |
|---|---|---|---|
| 01 | Automate Your Workflow | Turn repetitive work into executable AI workflows using authorized NAS files, documents, knowledge and system capabilities | Business productivity |
| 02 | Bring Memories to Life | Organize, search, extract, summarize, create albums from family photos, videos, documents | Personal and family data |
| 03 | Unleash Your Creativity | Help photographers/editors/creators search, tag, select, organize, reuse media libraries | Creative workflows |
| 04 | **Open Innovation** | Build an original AI Skill that solves a real user need and runs on UGREEN AI NAS; combine local AI, private data, storage, media, knowledge | Most room for differentiation |

**Foreman is submitted under Open Innovation** — deliberately *not* framed as "another document automation tool" (which would fit Track 01 but look generic). The chat's reasoning: Open Innovation gives room for an ambitious operational tool, provided it demonstrably uses supported NAS capabilities.

### 2.4 Submission requirements

| Requirement | Round 1 | Round 2 |
|---|---|---|
| Project proposal PDF | Required | Final project information |
| Skill package ZIP | Required | Required |
| Working on actual NAS | **Not required** | **Required** |
| Demo video | Not required by official rules | **Required** — public YouTube, **under 3 minutes** |
| Max ZIP size | 10 MB (ZIP and uncompressed) | Same package limits |
| Entry point | `SKILL.md` | `SKILL.md` |
| Language | English | English |

**Round 1 proposal PDF:**
- Max **500 English words** across ten answers; max file size **1 MB**.
- Must answer the ten questions:
  1. What the Skill does.
  2. Target user and problem.
  3. Proposed solution.
  4. Core user flow.
  5. Difference from existing tools.
  6. UGREEN NAS capabilities used and where.
  7. Technical approach — CLI capabilities, agent orchestration, inputs, permissions, models, data handling.
  8. Current development status.
  9. **Two core test cases and one edge case.**
  10. Known limitations, risks, dependencies.

**Round 1 Skill ZIP:**
- Must contain a valid `SKILL.md` (mandatory). Supporting Markdown reference files optional.
- **No executable scripts, binaries or separate manifests.**
- Does **not** need to be fully installable or operational in Round 1 (the detailed submission section says so; UGREEN's marketing copy mentions code — the chat says to follow the detailed rules).
- No code repository URL, no deployment to NAS, no demo video needed in Round 1.

**Discrepancy handled:** UGREEN's marketing challenge page mentions a preliminary walkthrough video; the official Devpost rules say a Round 1 video is **not** required. Decision in chat: **follow the official rules**, optionally prepare a short prototype video if time permits.

### 2.5 Hard technical restrictions (from the rules)

- Skills must follow UGREEN's official **Uliya Skill Development Standard**.
- Entry point is `SKILL.md`.
- Workflows must use **supported UGOS CLI capabilities through registered expert agents**.
- **Unsupported:** custom executable scripts, general-purpose programming runtimes, unauthorized direct NAS resource access.
- External APIs and third-party models **are allowed** when properly authorized, but data flows, sources and licenses **must be disclosed**.
- Users must **authorize** access to their data.
- **Destructive or external-sharing actions require confirmation.**

Consequence: design around a **sequence of supported agent actions**. Do **not** assume we can deploy a Python app, background server, or custom computer-vision runtime on the NAS.

### 2.6 Judging

Four criteria, **25% each**:

| Criterion | Weight | Official meaning |
|---|---|---|
| User Value | 25% | Clear problem, useful workflow, meaningful outcome |
| Innovation & Differentiation | 25% | Substantive new function/interaction/workflow beyond conventional AI tools and existing solutions |
| Technical Quality | 25% | Sound agent orchestration, supported CLI usage, permissions, error handling, reliable execution |
| AI NAS Fit & Validation | 25% | Meaningful use of NAS data, local AI, storage, computing, privacy — "rather than merely running on NAS" |

Process details:
- **Round 1 is a viability gate.** Judges first decide whether the project fits the theme and proposes a viable AI NAS solution; eligible ideas are then scored; up to 30 finalists advance.
- **Round 2 is a fresh competition.** Round 1 scores **do not carry over**; winners are determined entirely by Round 2 scores.
- Therefore two strategies: **Round 1** = clear compelling problem + convincing workflow + feasibility + credible test plan. **Round 2** = a reliable working Skill + impressive demo of the promised workflow.

### 2.7 Prizes

| Award | Prize |
|---|---|
| Gold | $20,000 |
| Silver | $10,000 |
| Bronze | $6,000 |
| Most Creative (×2) | $5,000 each |
| **Total** | **$46,000** |

The two Most Creative awards go to the highest-scoring eligible projects on **Innovation & Differentiation**. Each project can win only **one** award.


---

## 3. The platform: UGREEN AI NAS, UGOS, Uliya, Skills

### 3.1 Components

| Component | Purpose |
|---|---|
| UGREEN AI NAS | Local hardware: storage, memory, processing, AI compute |
| UGOS | UGREEN's Linux-based operating system |
| Uliya / Skill Creation Tool | AI Skill creation and execution environment |

The Skill Creation Tool lets developers create capabilities an AI assistant can invoke to perform supported NAS operations. Skills are distributed through the UGREEN ecosystem and **Skills Hub**. UGREEN's current creation-tool documentation recommends **WorkBuddy, Claude, and Codex**; the UGREEN local model is encouraged but **not mandatory**.

### 3.2 Finalist testing hardware: UGREEN iDX6011 Pro

| Spec | Value |
|---|---|
| Processor | Intel Core Ultra 7 255H |
| CPU | 16 cores / 16 threads |
| AI compute | Up to **96 TOPS** (per UGREEN) |
| RAM | 64 GB LPDDR5/x |
| Storage | Up to 208 TB advertised configuration |
| Network | 2 × 10GbE |
| Expansion | 2 × Thunderbolt 4 |
| OS | UGOS Pro |

**Caveat:** 96 TOPS is a hardware spec, **not** a guarantee that any large model or video-processing workload runs efficiently. We must validate the actual model and workflow.

### 3.3 Official capability categories (Starter Kit)

| Capability | What can be built |
|---|---|
| Files | Find, browse, organize, deduplicate, tag |
| Albums | Search photos by person, location, or time; create albums |
| Documents | Read, answer questions, extract, translate, reconcile |
| Knowledge | Search official documentation, transcribe recordings, save text |
| Video / Music | Search media, control playback, find subtitles |
| Surveillance | Query camera events and organize related details |

Capabilities **can be chained** (e.g., Find files → Read documents → Extract information → Reconcile → Organize results). **Each step must map to a genuinely supported capability.**

### 3.4 Uliya already has an agent system (critical finding)

UGREEN already provides:
- A **Smart Task Assistant** that plans and executes multi-step tasks.
- **Specialist assistants** for photos, surveillance, files, documents, learning.
- Multiple assistants that can collaborate on a task.
- Automatic and manual Skill selection.
- A visible execution chain.
- **Local, hybrid, and cloud** model options.
- Permission controls, including approval before sensitive operations.

**Strategic conclusion:** *We should not compete with Uliya. We should give Uliya a capability it doesn't already have.* A generic document Q&A assistant is not impressive when Uliya already offers document Q&A, OCR, cross-document search and extraction. Foreman must therefore: investigate a specific operational problem across multiple file types → connect evidence from different sources → detect inconsistencies/risks → produce a structured decision → (optionally) execute an approved corrective action → preserve an evidence trail.

### 3.5 Privacy fact that affects us

UGREEN **explicitly documents** that documents uploaded during chats and knowledge-base content are **sent to the selected cloud model when cloud mode is enabled**. Any proposal involving confidential information (like construction contracts and pricing) must account for this. See §18.

### 3.6 Why local AI matters (three application types)

| Application | Why local NAS matters |
|---|---|
| Personal data intelligence | Processes personal documents/memories locally |
| Business intelligence | Keeps private business records in the organization's own storage |
| Media intelligence | Works with large photo/video/audio libraries without continuous cloud upload |

Foreman is a **business intelligence** application with **media** components (recordings, photos).

---

## 4. Why UGREEN runs this hackathon (strategic context)

### 4.1 Company background **[Confirmed unless noted]**

| Milestone | Detail |
|---|---|
| 2012 | Founded; established consumer-electronics business |
| March–May 2024 | NASync raised $6.68M on Kickstarter |
| July 2024 | Listed on Shenzhen Stock Exchange (code 301606) |
| March–April 2026 | New AI NAS campaign raised $8.84M |
| Sept 1, 2026 | Announced **HomeAgent**, its first AIoT ecosystem |

Four product categories: smart charging & creative; smart office; smart audio & visual; smart storage. Reported operating revenue **9,491 (reporting unit) in 2025 vs 6,170 in 2024 ≈ +53.8%**.

### 4.2 HomeAgent (Sept 2026)

Ecosystem includes: local AI hubs, SynCare security cameras, smart speakers for Uliya, e-paper and LCD smart frames, Matter-compatible smart-home control, AI event recognition and summaries, cross-camera event timelines, local storage and processing. Stated goal: make household data useful through an intelligent system that can understand, assist and act while keeping users in control.

**Important:** HomeAgent is a **separate product ecosystem**. Our Skill must work with documented iDX6011 NAS capabilities and **cannot depend on unreleased HomeAgent hardware or future features.**

### 4.3 UGREEN's emerging ecosystem

Storage (private files/photos/videos/records) + Local intelligence (on-device AI/agentic workflows) + Connected devices (cameras/speakers/smart-home) + Developer ecosystem (Skills/packages/third-party capabilities).

### 4.4 Why UGREEN created the hackathon **[Interpretation — four hypotheses]**

1. **Make AI NAS useful beyond hardware specs** — a powerful NAS is hard to justify if it just stores files; Skills make it a daily-use tool.
2. **Create a developer ecosystem around Uliya** — UGREEN can't build every niche workflow internally.
3. **Demonstrate the value of private, local AI** — a Skill doing valuable work on personal/business data beats a generic chatbot as a demo.
4. **Increase product adoption and long-term engagement** — more useful Skills → more reasons to buy and keep using the hardware.

*Direct signal (confirmed):* the official hackathon page discusses expanding the Skills Hub, developer exposure, and potential future collaborations. The four objectives above are the chat's interpretation of that.

**What this means for us:** judges should think, *"This is exactly the kind of capability that makes UGREEN AI NAS more valuable as a platform."*

---

## 5. Product definition

### 5.1 What Foreman is

> An AI-powered investigation Skill that connects construction contracts, change orders, meeting records, site photographs, and invoices to uncover undocumented scope changes, missing approvals, and payment discrepancies.

It is **an AI investigator for construction projects**, not simply an AI project-management tool. It **does not replace** the project manager, quantity surveyor, or contract administrator — it gives them a much better investigation process.

### 5.2 The question it answers

> *"Are we paying for work that was never properly approved, and can we prove what actually happened during this project?"*

### 5.3 What it is NOT (positioning guardrails)

- Not a document summarizer or document Q&A tool (Uliya already has that).
- Not a "PDF Auditor" (the **weak version** — see §9.3).
- Not a legal interpreter (no verdict on entitlement to payment).
- Not a physical-progress verifier (photos alone can't establish quantity/quality of work).
- Not full project management (no scheduling, resource allocation, Gantt charts, general dashboards).
- Not a fraud detector — it identifies documentary anomalies that deserve verification.

*"Foreman should remain an investigator."*

### 5.4 Core promise

> Foreman transforms scattered construction records into a connected evidence trail, helping teams investigate scope changes, approval gaps and payment discrepancies before they become larger problems.

### 5.5 Example user requests

- *"Audit Project Alpha. Find all invoiced work that does not have documented approval, identify missing change orders, and prepare an evidence report."*
- *"Investigate Project Alpha. Compare the original contract, all approved change orders, meeting records and invoices. Identify any invoiced work that does not have documented approval, duplicate charges, and price discrepancies. Show the supporting evidence for every finding."*

### 5.6 Investigation types (user requests → investigation)

| User request | Investigation |
|---|---|
| Audit Project Alpha | Full scope and payment audit |
| Check October invoices | Invoice reconciliation |
| Find missing approvals | Approval evidence investigation |
| Compare contract revisions | Scope change investigation |
| Prepare project handover | Outstanding issues and evidence report |
| Investigate an old dispute | Historical evidence reconstruction |

**[Verify]** The chat warns: do **not** promise background monitoring, automatic file indexing, or advanced visual progress analysis unless the supported interfaces allow them. "Prepare project handover" and "historical reconstruction" are listed as intended uses but are secondary to the core audit; confirm feasibility before putting them in the proposal.

---

## 6. The problem and its evidence

### 6.1 The business problem

A construction project produces many disconnected records:
- Original contract and scope of work
- Change orders and approval records
- Daily site reports
- Progress photographs
- Meeting recordings and minutes
- Contractor invoices
- Completion and inspection records

Typical failure: a contractor performs extra work after a **verbal instruction**. Later the client disputes the additional payment because there is **no signed change order**. The contractor must dig through weeks of documents, recordings, photographs and invoices to establish what happened.

Work may have been *discussed, requested, performed, invoiced and partially documented — but the evidence is not connected.* **That is the gap Foreman addresses.**

### 6.2 Questions a project manager faces for each invoice

- Was this work in the original contract?
- Was it an additional requirement?
- Who approved the additional work?
- Is there a signed change order?
- Does the invoice match the approved amount?
- Is there evidence the work was actually performed?

### 6.3 How changes arise

Client requests, unexpected site conditions, design changes, coordination problems. A **change order** is the mechanism for recording revisions, additions or deletions to the original contractual scope; changes can affect contract value.

### 6.4 Evidence base (independently researched 2026-11-04)

The original chat cited only a few sources. The evidence below was researched afterwards from primary reports, journal papers and government publications. **Verification level** says how much of each source was actually read: **Read** = full report text or official page was read; **Abstract** = publisher/repository abstract and bibliographic data read; **Search only** = confirmed only through search-result summaries (re-check before quoting).

Evidence tiers used: **Government** · **Industry report** (survey-based, consultancy) · **Peer-reviewed** · **Practitioner** (law-firm/trade commentary — lowest weight).

#### 6.4.1 How big and how common are construction disputes?

| Finding | Source | Tier | Verification | Caveat |
|---|---|---|---|---|
| **2024 data (North America):** average dispute value **US$60.1M** (up from $43.0M in 2023; $30.1M in 2021); average time to resolve **12.5 months** (down from 14.4 in 2023; 16.7 in 2021) | Arcadis, *Construction Disputes in Motion* — **15th Annual Construction Disputes Report, North America, 2025** | Industry report | Read (full text) | Survey of North American industry. Arcadis defines dispute value as the **value claimed by the contractor**, so it is a claimed amount, not an awarded one. |
| **2025 data (United States only):** average dispute value **US$56.0M** (−6.82%); average length **12.2 months** (report text gives 12.16); 57.9% of respondents saw more disputes in 2025; 75% expect more in 2026 | Arcadis, *Disruption to Innovation* — **16th Annual Construction Disputes Report, United States, 2026** | Industry report | Read (full text) | This edition is **US-only** (earlier edition was North America), so the two editions are not a like-for-like time series. |
| Top causes (2024 data): (1) errors/omissions in contract documents, (2) failure to understand/comply with contractual obligations, (3) **owner-directed changes** | Arcadis 2025 report | Industry report | Read | Perception survey of practitioners. |
| Top causes (2025 data): (1) failure to understand/comply with contractual obligations, (2) errors/omissions in contract documents, (3) delays and time extensions; followed closely by **owner-directed changes** and differing site conditions | Arcadis 2026 report | Industry report | Read | As above. |
| Most effective avoidance techniques (2025): good communications, contract and specification reviews, risk management; for early resolution, respondents named transparent communication, willingness to compromise, accurate schedules, cost transparency and **clear change-order procedures** | Arcadis 2026 report | Industry report | Read | Perception survey. |
| Arcadis states its earlier reports "identified contractual ambiguities, **scope creep, and cascading change orders** as leading causes" of conflicts on fast-moving projects | Arcadis 2026 report (sector commentary) | Industry report | Read | Commentary, not a measured statistic. |

**This resolves the chat's discrepancy.** Both Arcadis figure sets in the chat are real and correct, but from different editions: **$60.1M / 12.5 months** = 2025 edition (North America, 2024 data); **$56M / 12.16 months** = 2026 edition (United States, 2025 data). When citing, always name the edition, region and data year.

**Honest framing rule:** these are averages of large claimed disputes in a survey of practitioners. They show the financial stakes of poor documentation. They are **not** the expected value or duration of a dispute for a small contractor, and they say nothing about how well Foreman would perform.

#### 6.4.2 Change orders measurably hurt cost, schedule and productivity (peer-reviewed)

| Finding | Source | Tier | Verification | Caveat |
|---|---|---|---|---|
| In **161 school-renovation projects (~$1B, Las Vegas Valley)** change orders raised cost by about **3.56% of contract value**, accounting for roughly **three-quarters of cost growth**; about **40%** of projects had schedule overruns linked to change orders. Cost impact by cause: unforeseen conditions 1.45%, design issues 1.36%, owner-initiated 0.75%. Projects with schedule overruns had a higher change-order share (5.26% vs 2.51%). | Shrestha, P. P. & Zeleke, H. (2018). *Effect of Change Orders on Cost and Schedule Overruns of School Building Renovation Projects.* **Journal of Legal Affairs and Dispute Resolution in Engineering and Construction**, 10(4). DOI 10.1061/(ASCE)LA.1943-4170.0000271 | Peer-reviewed | Abstract | One region and one project type (public school renovation). |
| In **large-scale projects of an Indonesian contractor**, design changes explained **56.5%** of cost overruns and **40%** of delays; planning errors explained 34.5% and 23.1%. Authors recommend **structured change-order protocols**, better stakeholder coordination and adoption of advanced technology. | Ramadhan, J. S. & Waty, M. (2025). *Impact of Change Orders on Cost Overruns and Delays in Large-Scale Construction Projects.* **Engineering, Technology & Applied Science Research**, 15(1), 20291–20299. DOI 10.48084/etasr.9449 | Peer-reviewed | Abstract | Survey of **127 practitioners at one contractor (PT XYZ)**; PLS-SEM model of perceptions, so the percentages are model-derived, not measured project data. Relevant because the team is Indonesia-based. |
| Systematic review of **80+ studies (2009–2022)** across twelve countries: most common causes of variation orders are **owner-originated changes, consultant design changes, design errors/omissions and poor coordination**; effects include disrupted progress, higher cost and **delayed payment** | Amzafi, N. et al. (2024). *A Systematic Review of the Causes and Effects of Variation Orders in the Sustainable Construction Industry in Developing Countries.* **International Journal of Integrated Engineering**, 16(4), 188–203 | Peer-reviewed (review) | Abstract | Authors note an imbalance in the stakeholders studied may bias findings. |
| Changed work runs at roughly **70% of normal labor efficiency (~30% loss)**; about a third of change-work days showed no loss; **timing of the change is the principal driver** — changes caught before work reaches the crews have minimal effect, late ones cause disruption; material deficiencies rose four-fold on change work | Construction Industry Institute (1994). *The Effects of Change on Labor Productivity: Why and How Much* (Research Team RT-027b, SD-99) | Industry research body | Read (official page) | 1994 field study of a small number of sites. Old but widely cited. |
| Data from **162 projects**: **late change is more disruptive than early change**, all else equal | Ibbs, W. (2005). *Impact of Change's Timing on Labor Productivity.* **Journal of Construction Engineering and Management**, 131(11), 1219. DOI 10.1061/(ASCE)0733-9364(2005)131:11(1219) | Peer-reviewed | Search only | Re-check abstract before quoting. |
| Statistical definition of when a project is "impacted" by change orders, using hypothesis testing and logistic regression to predict probability of impact | Hanna, A. S., Camlic, R., Peterson, P. A. & Nordheim, E. V. (2002). *Quantitative Definition of Projects Impacted by Change Orders.* **JCEM**, 128(1), 57–64. DOI 10.1061/(ASCE)0733-9364(2002)128:1(57) | Peer-reviewed | Abstract | Mechanical/electrical-contractor data. |
| Large projects across asset classes typically run **~20% past schedule and up to 80% over budget** | McKinsey (2016). *Imagining construction's digital future* (Agarwal, Chandrasekaran et al.), citing Global Projects Database / IHS Herold (2013) | Consultancy | Search only (text on mckinsey.com) | "Up to 80%" is a ceiling, not an average. Large-project data; not specific to change orders. |

**What the peer-reviewed literature supports for Foreman:** change orders are a leading, repeatedly measured driver of cost growth and delay; the **cause of change differs in cost** (unforeseen and design changes cost more than owner-initiated); and **late discovery** of a change is the most damaging. This supports Foreman's focus on finding changes and their approvals **early**, before invoices are paid.

#### 6.4.3 Documentation, approvals and evidence

| Finding | Source | Tier | Verification | Caveat |
|---|---|---|---|---|
| Survey of arbitrators in **seven U.S. cities**: they were asked to weigh written documentation against oral testimony and to name the documentation problems they see most often. Conclusion: **the party keeping the most comprehensive and detailed records has the decided advantage** in dispute resolution | Kangari, R. (1995). *Construction Documentation in Arbitration.* **JCEM**, 121(2), 201–208. DOI 10.1061/(ASCE)0733-9364(1995)121:2(201) | Peer-reviewed | Abstract | 1995 US arbitration survey; full results not read. Directly supports a documented evidence trail. |
| Canada's Procurement Ombudsman: **"verbal instructions not captured by way of formal amendments often give rise to disputes"** and "the contract does not allow for amendments to be made verbally"; he also noted "the continued absence of federal prompt payment legislation" and that subcontractors have no standing in disputes against government, only against the prime contractor | Wall, D. (22 Nov 2018). "New procurement ombudsman stresses alternative dispute resolution as key tool." *Daily Commercial News* (interview with Procurement Ombudsman Alexander Jeglic) | Trade press quoting a government official | Read | Secondary report of an interview; 2018. Federal Canadian context. |
| Office of the Procurement Ombud study (July 2025): recurring problems in administering federal construction contracts include **poorly defined scopes of work**, inconsistent use of standard contract documents, unclear substantial-performance clauses and inadequate dispute-resolution mechanisms; falls hardest on SMEs; **89 cases / 155 issues** (2020–2024) from complaints and dispute requests. The study lists "Scope of Work: Change Orders, Costing, and Payment" as an examined issue area. | Office of the Procurement Ombud (2025). *Contract Administration in Construction Contracts* (P114-33/2025E); news release, 14 Jul 2025 | Government | News release read; **study PDF not opened** (archived page only) | The release does not itself discuss change orders or payment; the chat's claims about **refusals to pay and holdback delays** were **not confirmed** by the sources read — do not cite them until the full study is checked. |
| Contract forms make **written, signed change instruments** the formal mechanism. AIA A201-2017 Article 7: a **Change Order** is a written instrument signed by owner, contractor and architect recording the change, price adjustment and time adjustment; a **Construction Change Directive** is a written order issued before price/time are agreed. FIDIC 2017 Sub-Clause 20.2 requires a **Notice of Claim within 28 days** of becoming aware of an event, with a fully detailed claim within 84 days; late notice can bar the claim | AIA Contract Documents learning pages; Fenwick Elliott commentary on the FIDIC 2017 Red Book | Practitioner commentary on standard forms | Search only | Section numbers and time limits come from secondary commentary — verify against the actual contract text. Foreman must treat each project's **own contract** as authoritative, not a generic standard. |
| **Contemporaneous** records (made at the time) carry the most weight; dated, located photographs support timing; **undated or unlocated photos are weak**; photos work best alongside daily logs and written records | Law-firm and trade articles, e.g. Verrill "The Value of Photographic Evidence in Construction Litigation" (*Construction Executive*) | Practitioner | Search only | Commercially motivated commentary; no formal study found. Supports Foreman using photos as **corroborating evidence only**. |

**Industry voice (not a statistic):** in the Arcadis 2025 report, a contractor executive commented that owner-directed changes are a growing dispute cause and that teams should "properly document these changes", adding "a return to the basics on documenting changes, but now with AI technology."

#### 6.4.4 Industry digitization and the AI gap

- Arcadis (2025 and 2026 reports, read): respondents increasingly use digital tools and AI; the 2026 report says AI "also creates its own challenges if not properly implemented" and that "disciplined fundamentals remain essential" — it flags **document-quality issues** and contract non-compliance as drivers of expected disputes.
- McKinsey (2016, search only) frames construction as a sector slow to digitize and prone to overruns (see 6.4.2).
- **Research gap found:** the search found **no peer-reviewed study that evaluates LLMs on extracting change orders or reconciling invoices against contracts in construction**. The closest peer-reviewed work is a 2021 JCEM paper on an NLP model for storing/retrieving similar change orders (ASCE DOI 10.1061/(ASCE)CO.1943-7862.0002172, **search only**); LLM contract-extraction evidence found was preprints and a thesis on general legal contracts (e.g. arXiv 2605.05532), with inconsistent performance across clause types. Vendor pages claiming accuracy figures were not credible and are not used here.
- **Implication:** Foreman's extraction accuracy cannot be justified by published evidence. It must be **measured on our own synthetic dataset** (§20–21), and the proposal must not claim a specific accuracy from literature.

#### 6.4.5 What the evidence means for Foreman (design implications)

| Evidence says | Foreman design consequence |
|---|---|
| Errors/omissions in contract documents and failure to comply with contractual obligations top the cause lists | Extract the **project's own contract terms** first (Contract Intelligence stage); never assume a standard form |
| Owner-directed changes, unforeseen conditions and design changes drive cost growth; verbal instructions not formalised cause disputes | Separate **formal approval / discussion / reported instruction** (§14); flag changes that appear in meetings or site reports but lack a signed instrument |
| Late discovery of change is most damaging; delayed payment is a documented effect | Run **before payment**, at invoice review; surface missing approvals early |
| Records kept comprehensively and contemporaneously win disputes; undated photos are weak | Ledger keeps **exact source paths and dates**; photos are corroboration only, flagged when undated or unlocated |
| Written, signed change instruments and notice deadlines are contractual | Report must say "no approval evidence found in accessible records", never "approval does not exist"; time-bar rules are **out of scope** unless taken from the project's contract |
| No published evidence for LLM change-order extraction accuracy | Measure precision/recall and false positives on the synthetic dataset; label results as test results |
| Dispute statistics are claimed values from large projects | Do not use them as expected savings; use them only to show the stakes |

#### 6.4.6 Limits of this background research
- Most peer-reviewed change-order studies are from single regions (US, Middle East, Indonesia) and use perception surveys; magnitudes differ widely between studies, so they are **not comparable** and should not be averaged.
- Arcadis figures are survey-based and reflect large disputes.
- Several items are marked **Search only** or **study PDF not opened**; re-check them before quoting in the proposal.
- No source here shows that a tool like Foreman reduces disputes; the evidence establishes the **problem**, not the **solution's effectiveness**.

---

## 7. Target users and positioning

### 7.1 Target users
- General contractors
- Construction project managers
- Contract administrators
- Quantity surveyors
- Construction finance teams

### 7.2 First-run value proposition
Foreman **doesn't need a huge dataset, marketplace analytics, or thousands of users** to be useful. A single company can put its existing project records on its NAS and use Foreman immediately — no cold-start dependency, no external business integrations, no external analytics dataset.

### 7.3 Official positioning statement
- **Name:** Foreman
- **Tagline:** Know what changed. Know what was approved. Know what you're paying for.
- **Category:** AI Construction Project Investigation
- **Primary track:** Open Innovation
- **Core technology:** UGREEN Uliya Skills; Documents, Files, Knowledge, Albums

### 7.4 Room to expand (post-v1)
Contractor operations, procurement, project risk management. (Not part of v1.)

---

## 8. The core product idea: Claim-to-Evidence Ledger

**The heart of Foreman.** *"The AI investigator is the interface, but the evidence relationships are the actual product differentiation."*

### 8.1 The five perspectives it connects

| Record | What it tells us |
|---|---|
| Contract | What was originally agreed |
| Change order | What was formally documented as changed |
| Meeting recording | What was discussed |
| Site report | What someone reported doing |
| Invoice | What someone is requesting payment for |

Instead of treating each document independently, Foreman **connects** all five to reconstruct the documentary history:

```
Original Contract → Original Scope
Change Order      → Additional Work
Meeting Recording → Documented Discussion
Site Report       → Reported Work
Invoice           → Claimed Payment
        ↓
 Evidence Reconciliation
   ├─ Matched Evidence
   ├─ Missing Approval
   ├─ Amount Discrepancy
   └─ Conflicting Records
        ↓
 Investigation Report
```

### 8.2 What the Ledger must contain
Every finding links an **invoice line** to:
1. its **original scope** item,
2. the relevant **change order**,
3. the supporting **meeting record**,
4. the **site report** (if any),
5. **missing evidence**,
6. **exact source file paths** (and page references where possible) so a judge/user can inspect where each conclusion came from.

### 8.3 Differentiation in one line
A typical document assistant reads a contract or summarizes an invoice. Foreman investigates the relationship between *what was originally agreed → what was subsequently requested → what was documented as approved → what was reported as performed → what was eventually invoiced.*

### 8.4 Next design task (not yet done)
The chat's explicit next step: **define the exact Claim-to-Evidence Ledger architecture** — what data each agent extracts, how records connect, how discrepancies are calculated, and how every AI conclusion traces back to its original document. **This is currently unspecified** (see §28, §29).

---

## 9. NAS-native design: Project Evidence Vault

This section exists because the user challenged the idea ("is Foreman really necessary for a NAS? it doesn't need a massive dataset"). The conclusion was to **make the NAS-native architecture the foundation of the product.**

### 9.1 Honest concession
Foreman does **not** need a huge dataset; 20 PDFs and a few recordings can demonstrate it. The NAS value is **not** "we need 100 TB." Don't artificially create thousands of files to make NAS seem necessary — a small realistic dataset is enough for a demo.

### 9.2 Four reasons NAS genuinely matters

**A. Construction projects generate continuous records.** A 12–24 month project continuously produces: contracts (agreement, amendments); financial (invoices, payment applications, receipts); engineering (drawings, specifications, revisions); site operations (daily reports, photographs, inspection records); communication (meeting recordings, minutes, correspondence); administration (change orders, approvals, handover records). Multiple projects + years of high-res photos, video and audio create a larger, longer-lived environment. The company's records *already have a natural home* on a NAS.

**B. Information must stay available over time.** Lifecycle: Jan — contract/drawings/specs stored → Mar — changes accumulate → Jun — invoices arrive, discrepancies need investigation → Dec — project closes, final accounts archived → next year — a dispute occurs and the company investigates history *without rebuilding the evidence collection.* A NAS is a natural persistent repository.

**C. Privacy and local processing.** Contracts, pricing, financial documents, client information are confidential. With a local-model workflow, sensitive records can be processed inside the company's own NAS environment rather than routinely uploaded to an external AI service. **But:** cloud models still transmit data; local storage alone does not make all AI processing private.

**D. NAS is the operational home for the Skill.** Foreman isn't used once and forgotten — it should investigate *any authorized project on the NAS, whenever needed* (Alpha, Beta, Gamma; handover reports; old-project reconstruction). It grows more useful as the archive grows. UGREEN itself describes NAS as a centralized place for team files, project files, collaboration, remote access and archiving.

### 9.3 Two versions of Foreman

| | **Weak version — AVOID** | **Strong version — RECOMMENDED** |
|---|---|---|
| Name | Foreman as a **PDF Auditor** | Foreman as a **Project Evidence Intelligence Skill** |
| Behavior | Upload a few documents → summarize with AI → find possible discrepancies → generate a PDF report | Investigate **persistent project archives**; connect contractual, financial, audio and visual records; reconstruct project history; maintain traceable evidence reports; investigate multiple projects; use local NAS intelligence for confidential records; **save investigation outputs back into the project archive** |
| Problem | Looks like a generic AI document app; NAS is only a place to read files | Gives UGREEN a stronger reason to showcase it in the Skills Hub |

### 9.4 The Project Evidence Vault
Treat the NAS as the company's **long-term project evidence repository**, containing:
- all original contracts,
- every change order and revision,
- all invoices and payment records,
- meeting recordings and minutes,
- site photographs and reports,
- **previous investigation reports.**

### 9.5 The decision rule for every future idea
> **If we remove the UGREEN NAS from the architecture, does the product lose a meaningful part of its value?**

For Foreman:
| Remove… | We lose… |
|---|---|
| NAS storage | The persistent project evidence repository |
| Local AI | An important privacy and processing option |
| Document capabilities | Contractual intelligence |
| Knowledge | Meeting-record investigation |
| Albums | Visual evidence discovery |

This does **not** mean NAS is the only possible platform — it means the NAS must be a **meaningful part of the design, not merely its deployment location.**

### 9.6 Backup caveat
NAS storage protection ≠ complete backup. RAID protects against certain drive failures but a **separate backup** is still needed against accidental deletion, ransomware, theft or total device loss (UGREEN's own backup guidance says this). The Evidence Vault must not be presented as the only copy of project evidence.

### 9.7 Verification warning
Persistent archive / saving investigation outputs back to the vault depends on supported "save" operations (Knowledge: "save text"; Files: organize/tag). **[Verify]** that saving reports and organizing evidence into folders is supported before promising it.

---

## 10. Investigation workflow (6 stages)

Foreman must **not** simply ask a model to read every document and summarize. It performs a **structured investigation**. Each stage has a defined input and output, and each stage passes its **actual output** to the next (the Starter Kit instructs developers to avoid vague references).

### Stage 01 — Project Discovery
Find relevant project records: original contracts; approved change orders; invoices and payment applications; meeting minutes and recordings; daily site reports; progress photographs.
**Output:** a list of discovered files with paths, dates, and document categories.

### Stage 02 — Contract Intelligence
Extract from the original contract: project scope; work descriptions; quantities; contract values; exclusions; payment terms; change-order references.
**Output:** **Original Scope Register.**

### Stage 03 — Change-Order Investigation
Identify all modifications: which work was added / removed; requested value; what approval evidence exists; is there a signed document; are there conflicting instructions.
**Output:** **Change-Order Register** with evidence references.

### Stage 04 — Project History Reconstruction *(important differentiator)*
Search meeting recordings and site records to discover **when** a change was discussed or documented. Example chronology:
- Oct 12: Client requests additional doors.
- Oct 13: Contractor discusses the change.
- Oct 15: Work appears in a site report.
- Oct 20: Invoice includes additional doors.
- No formal approval record found in the supplied files.

**Output:** **Chronological Evidence Timeline.**

### Stage 05 — Invoice Reconciliation
Compare invoices with original contract and change orders: Does the work already exist in original scope? Does it match an approved change order? Is the same work being invoiced twice? Does the amount match the documented amount? Are quantities inconsistent?
**Output:** **Invoice Exception Register.**

### Stage 06 — Evidence-Based Investigation Report
Assemble: summary of potential discrepancies; source documents and page references; timeline of relevant events; missing evidence; recommended human review actions.
**Output:** **Foreman Investigation Report**, saved with an evidence index, followed by **human review.**

### Compact flow (as in the Mermaid diagram)
User selects project and audit request → Find authorized project files → Extract contract and scope → Extract change orders and invoices → Transcribe project recordings → Find dated site photographs → Build approved scope register → Reconcile invoices and approvals → Build decision and approval timeline → Build visual evidence index → Cross-check all project evidence → Generate discrepancy report → Identify missing evidence → Save report and evidence index → Human review.

> This is an **orchestration plan, not a claim that every agent call is implemented.**

### Credibility requirements for the workflow
- Each step uses the actual output of the preceding step.
- The Skill specifies what happens when files are missing.
- **Ambiguous evidence is flagged, not invented.**
- Important file operations require confirmation.
- The output is defined **before** execution.
- The workflow can be tested against a known dataset.

---

## 11. Agent architecture

These are **proposed responsibilities**, *not* claims that UGREEN already provides agents with these names. An **orchestrator** controls the order of execution.

| Proposed agent | Responsibility |
|---|---|
| Project Finder | Locate authorized files belonging to the selected project |
| Contract Analyst | Extract original scope, quantities and contract values |
| Change Analyst | Extract and compare change orders |
| Meeting Analyst | Transcribe recordings and identify relevant discussions |
| Invoice Analyst | Extract invoice details and compare with documented scope |
| Evidence Investigator | Connect findings, identify conflicts, generate the report |

**[Verify]** The chat's explicit next step: validate these six responsibilities against the **actual UGREEN Developer Package** — exact CLI capabilities, inputs and outputs. Constraint: workflows must go through **registered expert agents** and supported UGOS CLI, so these role names may need to be mapped onto UGREEN's actual registered agents (Files/Documents/Knowledge/Albums/etc.) rather than invented ones. Also unresolved: exact CLI command identifiers and agent interfaces.

---

## 12. UGREEN capability mapping

Mapped against the official Starter Kit (section 6, "UGOS Skill Capability Scope"):

| UGREEN capability | Officially documented functionality | Foreman usage |
|---|---|---|
| **Files** | Find, browse, organize, deduplicate, tag | Discover project records; locate project folders and supporting documents; organize evidence |
| **Documents** | Read, answer, extract, translate, reconcile | Extract/understand contracts, invoices and change orders |
| **Knowledge** | Look up documentation, transcribe recordings, save text | Transcribe meeting recordings to recover discussions; save reports |
| **Albums** | Find photos by person, location or time; organize albums | Find relevant site photographs by date or location |

UGREEN itself gives examples of (a) using Documents to extract project information from contracts and invoices, and (b) transcribing a meeting recording and saving it as meeting minutes — **so we are combining documented capabilities into a more specialized investigation workflow, not inventing base capabilities.**

Capabilities **not used**: Video/Music and Surveillance.

---

## 13. Outputs and deliverables

### 13.1 Output set (two views in the chat — reconcile at spec time)

**View A (first answer) — six outputs:**

| Output | Contents |
|---|---|
| Scope Register | Original work and approved changes |
| Change Order Register | All discovered changes and approval status |
| Invoice Reconciliation | Invoice-to-scope discrepancies |
| Evidence Timeline | Dates and supporting documents |
| Missing Evidence | Approvals or records that could not be found |
| Executive Report | Main discrepancies and recommended review actions |

**View B (later answer) — five interconnected outputs:**

| Output | Purpose |
|---|---|
| Project Overview | Contract value, scope and project information |
| Scope Register | Original and modified work |
| Change-Order Register | Approval and evidence status |
| Invoice Exception Register | Duplicate, mismatched or unsupported charges |
| Investigation Report | Findings, source references and next actions |

*(Evidence Timeline and Missing Evidence appear inside the report in View B.)* **[Decision needed]** Pick one canonical output list for `SKILL.md`. A reasonable union: Project Overview, Scope Register, Change-Order Register, Invoice Exception Register, Evidence Timeline, Missing Evidence, Investigation Report (with Executive summary).

**Most important component: the Exception Register** (using the classifications in §14).

### 13.2 Report must include
- Summary of potential discrepancies
- Source documents with **exact file paths** and page references
- Timeline of relevant events
- Missing evidence
- Recommended **human review** actions
- Per-finding link to contract, change order, meeting record, and any missing evidence

### 13.3 Saving
The report and evidence index are saved back to the NAS (Knowledge "save text" / Files organization). File-moving/organizing operations require **user confirmation**.

---

## 14. Finding classifications and trust rules

### 14.1 Classifications

| Classification | Meaning |
|---|---|
| **Matched** | Supporting documentation is consistent |
| **Review** | A discrepancy needs human verification |
| **Missing evidence** | Required supporting evidence was not found |
| **Conflicting** | Two or more records disagree |
| **Insufficient data** | Not enough information to determine a result |

*(An earlier example table also used "Verify" as a result label, e.g., HVAC modification: Not invoiced / Meeting approval recorded / Verify. Normalize to the five classes above.)*

### 14.2 Non-negotiable trust rules

1. **Not finding an approval document does not prove approval never happened.** The correct wording is: **"No approval evidence found in the accessible project records."**
2. **A meeting recording mentioning a client's request does not automatically establish a formally approved change order.** Keep **formal approval**, **discussion**, and **reported instruction** as separate evidence types.
3. **Never** declare the contractor fraudulent or the invoice legally invalid. Identify a discrepancy, explain why it matters, show the evidence.
4. **Never** make legal conclusions about entitlement to payment.
5. **Never** invent an answer when records are missing — flag it.
6. When two versions of a record conflict, **do not choose an unsupported version**; mark for review.
7. **Never** execute payments or modify anything financial.
8. Every finding carries source references.
9. Destructive or external-sharing actions require user confirmation.

---

## 15. Worked example: Project Alpha

**[Illustrative]** — numbers are invented for demonstration; the reasoning process is what matters.

### 15.1 Setting
A contractor is constructing a commercial building; all documents are on the company's UGREEN NAS. A project manager wants to check whether all additional payments have supporting documentation.

(Narrative contract example from the chat: install 100 windows; build 20 internal walls; install one HVAC system; electrical work per approved drawings. The numeric contract below uses different quantities — they are separate illustrations.)

### 15.2 Original contract — CONTRACT-001

| Work | Agreed quantity | Contract value |
|---|---|---|
| Install windows | 100 units | $20,000 |
| Electrical installation | 500 m | $15,000 |
| Internal walls | 200 m² | $12,000 |
| HVAC installation | 1 system | $18,000 |
| **Total** | | **$65,000** |

### 15.3 Change-order register

| Ref | Additional work | Value | Evidence |
|---|---|---|---|
| CO-001 | Additional electrical work | $3,000 | Signed |
| CO-002 | Additional windows | $4,000 | Signed |
| CO-003 | Flooring modification | $2,000 | Signed |
| CO-004 | Additional doors | $2,500 | **No signed approval located** |

### 15.4 Invoice register

| Invoice | Description | Amount |
|---|---|---|
| INV-001 | Original electrical work | $15,000 |
| INV-002 | Additional electrical work | $3,000 |
| INV-003 | Additional windows | $4,000 |
| INV-004 | Flooring modification | $2,000 |
| INV-005 | Additional doors | **$8,500** |

### 15.5 What Foreman discovers

**Finding A — Additional doors: missing formal approval evidence**
- Invoice: INV-005, **$8,500**
- Related change order: CO-004, **$2,500**
- Difference: **$6,000**
- Supporting document: a meeting recording mentioning additional doors.
- Investigation: the recording references additional work, but the accessible project records do not contain sufficient formal approval evidence for the invoiced amount.

**Finding B — Potential amount discrepancy:** the invoice exceeds the documented change-order amount by **$6,000**; the difference needs a separate explanation or supporting approval.

**Recommended action:** ask the project administrator to verify the amount and locate any missing approval **before accepting the invoice.**

### 15.6 ⚠ Internal inconsistency in the source chat
The chat's summary tiles read "3 matched invoices / 1 approval concern / 1 additional invoice to investigate / 1 potential unsupported amount." But the data shows **INV-001 through INV-004 all match** (four), and **INV-005 is the single problem invoice** (which yields both a missing-approval concern *and* an amount discrepancy). The tiles over-count findings. **Treat the correct expected result as: 4 matched invoices, 1 problem invoice (INV-005) with two linked findings (missing formal approval + $6,000 over CO-004).** Fix before using in any demo or proposal.

Also note: CO-004 itself is *unsigned*, so "difference vs CO-004's $2,500" is measured against an unapproved amount. The report should say so explicitly rather than treat $2,500 as an approved ceiling.

### 15.7 Chronological evidence timeline (illustrative, doors)
Oct 12 client requests doors → Oct 13 contractor discusses → Oct 15 work appears in site report → Oct 20 invoice includes doors → no formal approval record found.

---

## 16. Scope: what is in and out of version 1

### 16.1 In scope (v1)
- Compare **documentary evidence, metadata, approvals, and invoice details**.
- Simple **item / quantity / value** comparisons (start simple; construction invoices can be hard to reconcile).
- Duplicate-charge detection; amount mismatch; unsupported/unapproved additional work; conflicting versions.
- Meeting-recording transcription as *discussion evidence*.
- Photo discovery by date/location as *visual evidence index*.
- Evidence-linked report with source paths; saved back to NAS.
- Human review at the end.

### 16.2 Explicitly out of v1 (deliberately excluded)
1. **Automatic legal interpretation** — no ruling on whether a contractor is legally entitled to payment.
2. **Automated physical progress verification** — photos alone can't establish that a specified quantity of work was completed correctly. *(v1 must not claim to measure physical construction progress from photographs.)*
3. **Full project management** — no scheduling, resource allocation, Gantt charts, general project dashboards.
4. **3D / BIM models** — not covered by the research or the confirmed UGREEN capability list; add only if UGREEN's CLI is verified to read them.

Also out unless verified against the real CLI: background monitoring, automatic file indexing, advanced visual progress analysis, custom executable code, independent background services, direct NAS database/resource access, unsupported custom integrations, external OpenAI API dependency in v1.

*"Those features would make the project bigger but not necessarily better."*

---

## 17. Technical constraints and design rules

- Follow the **Uliya Skill Development Standard**; entry point `SKILL.md`.
- Use **only verified UGOS CLI operations** and registered expert agents.
- **No** executable scripts, binaries, or separate manifests in the ZIP (max 10 MB).
- Do **not** assume we can: install a Python processing engine; deploy an independent background service; directly access NAS databases/internal resources; run arbitrary executables; create unsupported custom integrations.
- Each stage must consume the **actual output** of the previous stage (no vague references).
- Must define behavior for **missing files**, **conflicting records**, **incomplete extraction**, **ambiguous approval evidence**.
- Must define the **output format before execution**.
- Users must **authorize** data access; **destructive/external-sharing actions require confirmation** (including moving/organizing files).
- Third-party models/APIs only when authorized and **disclosed** (data flow, source, license).
- Preserve **source references** (exact paths + page refs) in all outputs.
- Mark deliberate simplifications and ceilings honestly in the proposal.
- **Open item:** exact CLI command identifiers and agent interfaces must be verified against the downloaded creation-tool archive — the public capability list establishes direction, **not** implementation detail.

---

## 18. Privacy and model strategy

### 18.1 Recommended model strategy
- **Default to Uliya's local model** for sensitive project documents.
- Use **specialist agents** for document extraction, file discovery and transcription.
- Use the **reasoning model** for cross-document reconciliation.
- **Preserve source references** in the final report.
- Use **cloud models only when necessary, authorized and properly disclosed.**
- **No external OpenAI API dependency in v1** — it adds another integration to validate; the challenge already provides an agent-based environment.

### 18.2 Privacy honesty rules
- Local storage ≠ local processing. In cloud mode, uploaded chat documents and knowledge-base content go to the selected cloud model (UGREEN documented).
- The proposal's data-handling answer must say which mode the sensitive-record flow uses and disclose any cloud use.
- The OpenAI latest-model guide used in research is **guidance for the research process only, not a requirement** to use OpenAI in the project.

### 18.3 Performance caveat
Local-model quality/speed (including recording transcription and cross-document reasoning) on the iDX6011 must be **validated**, not assumed from "96 TOPS".

---

## 19. SKILL.md specification

### 19.1 What SKILL.md is
The instruction manual and workflow definition for the Skill. For Foreman it must explain:
1. What Foreman does.
2. What inputs the user must provide.
3. Which UGREEN NAS capabilities it uses.
4. Which specialist agents are involved.
5. The exact execution sequence.
6. How agents pass information to each other.
7. What happens when documents are missing.
8. How errors and conflicting evidence are handled.
9. What the final report must contain.

### 19.2 Illustrative starting skeleton
*(Only an illustration — **not** the complete UGREEN-compliant package.)*

```markdown
---
name: foreman
description: >
  Investigate construction project records,
  reconcile contractual scope, change orders,
  invoices and supporting evidence.
---

# Foreman

## User Goal
Investigate construction project records
and identify undocumented scope changes,
missing approvals and payment discrepancies.

## Required Inputs
- Project folder
- Investigation type
- Optional date range

## Supported NAS Capabilities
- Files
- Documents
- Knowledge
- Albums

## Workflow
1. Discover project documents.
2. Extract original contractual scope.
3. Identify change orders.
4. Recover project history.
5. Reconcile invoices.
6. Generate evidence-backed findings.

## Error Handling
- Missing documents
- Conflicting records
- Incomplete extraction
- Ambiguous approval evidence

## Completion
Generate a structured investigation report
with source references and recommended actions.
```

### 19.3 Gaps to fill before this is submission-ready
- Real UGREEN front-matter/format per the Uliya Skill Development Standard **[Verify]**.
- Per-step capability calls with real CLI identifiers **[Verify]**.
- Exact input/output schema per stage and the Ledger fields (§8.4).
- Permission/confirmation points (file moves, saves, any external sharing).
- Missing-file, conflicting-record, extraction-failure and ambiguous-approval handlers.
- Evidence-type taxonomy (formal approval vs. discussion vs. reported instruction).
- Output templates (registers + report).
- Supporting Markdown reference files (optional): classification definitions, report template, Ledger schema, test cases.

---

## 20. Test plan and metrics

Round 1 requires **two core test cases and one edge case**.

### Test 1 — Successful reconciliation *(core)*
- **Input:** original contract; signed change order; matching invoice; supporting site report.
- **Expected:** correctly identify original scope; match the change order; reconcile the invoice amount; produce source-linked findings.

### Test 2 — Undocumented additional work *(core)*
- **Input:** original contract; invoice containing additional work; meeting recording mentioning the additional work; **no** signed change order in accessible files.
- **Expected:** identify the additional work; find the meeting reference; flag missing formal approval evidence; recommend human verification.

### Test 3 — Conflicting evidence *(edge case)*
- **Input:** two different change-order versions; different approval dates; different amounts; an invoice referring to an older version.
- **Expected:** detect the conflict; identify the relevant source records; **avoid choosing an unsupported version**; mark the finding for review.

*(An earlier shorter draft of the tests, from the first answer: Test 1 signed CO matched with invoice; Test 2 invoice with additional work without documented approval; Edge — meeting transcript and signed document have conflicting approval dates. Use the later, fuller versions above; the "conflicting approval dates" scenario can be folded into Test 3.)*

### Metrics to measure
- Correctly matched invoice lines
- Correctly detected discrepancies
- **False-positive** findings
- **Source-reference accuracy**
- Missing-evidence detection
- Successful completion of the entire workflow

This gives measurable performance, not "our AI is smart."

### Demo guidance (for judges)
- User Value: show a specific invoice discrepancy and exactly which contract, change order and meeting record support it.
- Technical Quality: show a successful investigation, a missing document, **and** a conflicting approval record — handled without invented answers.
- NAS Fit: run a full investigation on files stored on the actual iDX6011 Pro, **preferably with the local AI model** for sensitive processing.
- Innovation: make the **Claim-to-Evidence Ledger** the signature visible feature.

---

## 21. Synthetic test dataset

Build **one synthetic construction project** with deliberately planted, known discrepancies so the correct output is known in advance:

- 1 original construction contract
- 3 approved change orders
- 2 unapproved change orders
- 5 invoices
- 3 meeting recordings
- several dated site photographs
- 1 contradictory approval record

**Notes / [Decision needed]:**
- The Project Alpha example (§15) has **3 signed + 1 unsigned** change orders and 5 invoices; the dataset spec above has **3 approved + 2 unapproved**. Reconcile into one master dataset and a written **answer key** (expected finding per planted discrepancy) before testing.
- Avoids cold-start dependence on marketplace data, user analytics or external integrations.
- Must be prepared **before** the finalist NAS day (only one assigned day of access; can't rely on weeks).
- Synthetic data only — never real client documents in demo material.

---

## 22. Judging criteria fit

*(Chat's qualitative assessment — not official scores, not a win guarantee.)*

| Criterion (25% each) | Fit | Why / how to impress |
|---|---|---|
| **User Value** | Very strong | Clear target user; financially important problem (missing approvals, scope discrepancies, invoice disputes); easy workflow; actionable evidence-backed exception register + report. *Demo:* one specific invoice discrepancy with the exact contract, change order and meeting record behind it. |
| **Innovation & Differentiation** | Strong, needs careful execution | Not document Q&A; connects what was agreed / requested / approved / reported / invoiced. *Demo:* the **Claim-to-Evidence Ledger** as signature feature. |
| **Technical Quality** | Strong *if implementation is reliable* | Multiple supported capabilities; defined stage inputs/outputs; specialist document + recording analysis; missing-doc and conflicting-evidence handling; user authorization and approval before sensitive file ops. *Demo:* success, missing doc, conflict. |
| **AI NAS Fit & Validation** | Excellent conceptual fit (conditional on NAS-native design, §9) | Data already lives on NAS; contracts+invoices+recordings+photos combined; benefits from local document/media access; local AI for confidential records. *Demo:* full run on iDX6011 Pro with local model. |

Self-assessment table from the research:

| Question | Assessment |
|---|---|
| Is the problem real? | Yes — supported by government procurement research |
| Is the target user clear? | Yes |
| Does UGREEN support the necessary data categories? | Yes, per the Starter Kit |
| Beyond generic AI? | Yes, if cross-record evidence reconciliation is delivered |
| Meaningfully uses NAS? | Yes |
| Demonstrable with synthetic data? | Yes |
| Technical risk? | **Yes** — especially agent orchestration and document extraction |
| Worth pursuing? | Definitely |

---

## 23. Risks and mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Too similar to document Q&A | Judges may see a wrapper around existing Uliya functionality | Focus on cross-record investigation and evidence traceability (Ledger) |
| Hallucinated approval | AI could mistake a discussion for formal authorization | Separate formal approval / discussion / reported instruction; "no evidence found in accessible records" wording |
| Poor document extraction | Scans/inconsistent documents cause errors | Controlled test dataset; validate extraction; "insufficient data" class |
| Complex quantity calculations | Construction invoices are hard to reconcile | Start with simple item / quantity / value comparisons |
| Weak technical integration | Concept may exceed supported NAS capabilities | Only verified UGOS CLI operations and registered agents |
| Insufficient demonstration | Report without traceable evidence looks like generic AI output | Show the full evidence chain in the demo |
| NAS used only as a file location (weak NAS fit) | Loses the 25% NAS-fit score | Strong version: persistent Evidence Vault, saved reports, multi-project, local model |
| Cloud-mode data leakage | UGREEN sends chat/knowledge content to cloud model in cloud mode | Default local model; disclose any cloud use |
| Local model too slow/weak for reasoning or transcription | 96 TOPS ≠ guaranteed performance | Validate real model/workflow early; keep workflow simple |
| Only one NAS test day | Can't iterate on the real device | Prepare Skill, references, data, validation instructions beforehand |
| Unsupported capability assumed | Could fail the viability gate | Verify every step against the creation-tool archive |

---

## 24. Round 1 submission plan

### 24.1 Deliverables
1. **Proposal PDF** — ≤500 English words total, ≤1 MB, ten answers.
2. **Skill package ZIP** — valid `SKILL.md`, optional Markdown references, **no scripts/binaries/manifests**, ≤10 MB. Also verify originality and third-party disclosures.

### 24.2 Suggested word budget (500 total)

| Section | Words |
|---|---|
| 1 Skill description | 25 |
| 2 Target user and problem | 55 |
| 3 Proposed solution | 55 |
| 4 Core user flow | 65 |
| 5 Differentiation | 55 |
| 6 UGREEN capabilities | 60 |
| 7 Technical approach | 85 |
| 8 Development status | 30 |
| 9 Validation plan (2 core + 1 edge) | 40 |
| 10 Limitations | 30 |
| **Total** | **500** |

### 24.3 Three things the proposal must emphasize
1. A **real financial problem** that already exists.
2. A **multi-agent workflow** making meaningful use of UGREEN NAS capabilities.
3. A **measurable outcome** — source-backed discrepancies and missing-evidence detection.

### 24.4 Honest wording requirements
- Development status: orchestration is **a plan**, not yet implemented/validated on a real NAS.
- Don't claim capabilities not verified.
- Always cite Arcadis figures with edition, region and data year (§6.4.1); describe them as claimed values from a practitioner survey.
- Don't cite the OPO study's change-order/payment findings until the full study PDF is read (§6.4.3).
- Don't claim extraction accuracy from literature; none exists for this task (§6.4.4).
- Disclose model/data flows.

---

## 25. Timeline and deadlines

### 25.1 Official schedule (corrected version)

| # | Date | Event |
|---|---|---|
| 1 | **Nov 15, 2026, 11:45 PM PST** (= Nov 16, 14:45 WIB) | Round 1 deadline — proposal PDF + Pre-test Skill ZIP |
| 2 | **Nov 21, 2026** | Finalists announced — up to 30 invited by email to the team representative (time not specified) |
| 3 | **Nov 22–28, 2026** | Round 2 development/testing — each finalist gets one assigned day (24-hour remote access) on a real iDX6011 Pro |
| 4 | **Nov 30, 2026, 11:45 PM PST** (= Dec 1, 14:45 WIB) | Final submission — final Skill ZIP + public YouTube demo video (≤3 min) |
| 5 | Not confirmed | Winner announcement (see §28) |

The chat's first draft said Round 2 closes Dec 1 PT and winner announcement ≈ Dec 6/7; the later, re-checked version corrects Round 2 to **Nov 30 PT** and says no winner date is confirmed. Use the corrected version and **re-check the Devpost page**.

### 25.2 Our internal plan (Round 1, as of Nov 4, 2026)

| Dates | Task |
|---|---|
| **Nov 4–5** | Finalize concept: select Foreman; verify every required NAS capability against the official creation-tool archive; finalize exact workflow |
| **Nov 6–8** | Build the Skill: `SKILL.md`, references, agent instructions, error handling, permission requirements |
| **Nov 9–11** | Validate: run creation-tool checks, review instructions, test workflow logic against the synthetic dataset |
| **Nov 12–14** | Submission prep: finish ten proposal answers, verify 500-word limit, ZIP structure, originality, third-party disclosures |
| **Nov 15–16** | Final review and submit **well before Nov 16, 14:45 WIB** |

---

## 26. Round 2 / finalist plan

- Finalists get **one** assigned day of remote access to an iDX6011 Pro (64 GB). Not continuous access through Nov 22–28.
- Therefore **prepare in advance:** the Skill package, reference files, synthetic test data, and validation instructions.
- Required in Round 2: Skill running on the actual NAS; final Skill ZIP; **public YouTube demo ≤ 3 minutes**.
- Round 1 scores do not carry over — Round 2 demonstrates a **reliable working Skill** and an impressive demonstration of the promised workflow.
- Demo should show: a successful investigation; a missing-document case; a conflicting-approval case; the Claim-to-Evidence Ledger; local-model processing; saved report back to NAS.

---

## 27. Why Foreman: selection checks

### 27.1 Seven screening questions, answered
| # | Question | Answer for Foreman |
|---|---|---|
| 1 | Does the problem exist independently of AI? | Yes — scope/change-order/payment disputes are documented in government procurement research |
| 2 | Can value be shown with a realistic dataset from day one? | Yes — synthetic project with planted discrepancies (§21) |
| 3 | Does it perform a meaningful workflow rather than just answer questions? | Yes — six-stage investigation ending in a Claim-to-Evidence Ledger |
| 4 | Does it combine at least two or three NAS capabilities? | Yes — Files, Documents, Knowledge, Albums |
| 5 | Is the core workflow achievable without custom scripts or unsupported infrastructure? | Yes on paper — **[Verify]** against the real CLI (§28.2) |
| 6 | Does local storage or private processing materially improve it? | Yes — confidential contracts and pricing, local model by default (§18) |
| 7 | Can measurable results be shown in the limited finalist window? | Yes — known planted discrepancies give a right/wrong answer key (§20, §21) |

### 27.2 Why this product
- Solves a costly business problem with a clear target customer.
- Uses four distinct NAS capability areas.
- Doesn't depend on external APIs or a pre-existing analytics dataset.
- Has a clear, testable output.
- Demonstrates local AI as a useful operational tool.
- Has room to expand into contractor operations, procurement and project risk management.
- Strong balance of user value, technical orchestration and business differentiation.

**Condition:** proceed *unless a technical limitation in the Developer Package prevents reliable cross-document reconciliation*, and only with the NAS-native architecture (§9) as the foundation.

---

## 28. Open questions, discrepancies and things to verify

### 28.1 Discrepancies inside the source chat (resolve before using)

| # | Item | What the chat says | Recommended handling |
|---|---|---|---|
| 1 | Round 2 deadline | First: Dec 1 PT/≈Dec 1 14:45 WIB window; later **corrected to Nov 30, 11:45 PM PST** (= Dec 1, 14:45 WIB) | Use Nov 30 PT; re-check Devpost |
| 2 | Winner announcement | First: "Dec 6 scheduled" (and ≈Dec 7 05:00 WIB); later: official page "does not specify a confirmed winner date" | Treat as unconfirmed; re-check Devpost |
| 3 | Arcadis statistics | 2026 report: $56M / 12.16 months; 2025 report: $60.1M / 12.5 months (North America, 2024) | **Resolved (2026-11-04):** both are correct and verified from the full reports — 2025 edition = North America, 2024 data ($60.1M / 12.5 mo); 2026 edition = **United States only**, 2025 data ($56.0M / 12.2 mo, text gives 12.16). Cite edition, region and data year (§6.4.1) |
| 4 | Project Alpha summary tiles | "3 matched invoices / 1 concern / 1 additional / 1 unsupported" vs. data showing 4 matched + 1 problem invoice | Use 4 matched + INV-005 flagged (§15.6) |
| 5 | Change-order counts | Alpha example: 3 signed + 1 unsigned; dataset: 3 approved + 2 unapproved | Build one master dataset + answer key |
| 6 | Output list | Six outputs vs. five outputs | Pick one canonical list (§13.1) |
| 7 | Round 1 video | Marketing page says walkthrough video; Devpost rules say not required | Follow rules; video optional |
| 8 | Code in Round 1 | Marketing copy mentions code; detailed rules say package need not be installable/operational | Follow detailed rules; no code/scripts allowed anyway |
| 9 | Contract narrative vs. table | Narrative: 100 windows, 20 walls, 1 HVAC; table: 100 windows, 500 m electrical, 200 m² walls, 1 HVAC ($65,000) | Illustrations only; use the table for the dataset |

### 28.2 Must be verified against the official creation-tool archive / Developer Package
- Exact **UGOS CLI command identifiers**, agent interfaces, inputs and outputs for each capability.
- Whether the six proposed agent roles map to **registered expert agents** (and how to express them in `SKILL.md`).
- The real **Uliya Skill Development Standard** format and any required front-matter fields.
- That **transcription** (Knowledge) works on the meeting-recording formats we'll use, and its accuracy/speed on the local model.
- That **Documents extraction** handles scanned/poorly-formatted contracts, invoices and change orders, and what page-reference granularity it exposes.
- That **Albums** can find photos by date/location the way Foreman needs for site photography (and that site photos can be organized by project/date).
- That **saving outputs** (reports, evidence index) and **organizing files into folders** are supported, plus the confirmation flow.
- Whether multi-project / historical investigation is feasible without unsupported indexing or monitoring.
- Local vs. cloud model behavior for each step and what exactly is transmitted in cloud mode.
- Whether the **Skill Creation Tool's checks** pass with our package.

### 28.3 Unresolved product decisions
- **[Decision needed]** Exact Claim-to-Evidence Ledger schema (fields per agent, linkage keys, discrepancy computation, citation format).
- **[Decision needed]** Canonical output list and report template.
- **[Decision needed]** Master synthetic dataset + answer key.
- **[Decision needed]** Whether "handover report" and "historical dispute reconstruction" appear in the v1 proposal or are future work.
- **[Decision needed]** How to express evidence types (formal approval / discussion / reported instruction / site-reported work) in the schema.
- **[Decision needed]** Team composition (up to 3 eligible individuals) and which person is the team representative who receives the finalist email.
- **[Decision needed]** Language/locale of demo documents (the research was done for an Indonesian-based team; the problem evidence is mostly Canada/North America). Keep demo English per rules.

### 28.4 Honesty constraints to carry into every document
- Don't claim UGREEN already has dedicated functionality for Foreman, nor that agent names are existing UGREEN agents.
- Don't claim a literal two-hour unattended research session.
- Don't claim 96 TOPS guarantees model performance.
- Don't claim to measure physical progress from photos or determine legal entitlement.
- Illustrative numbers must be labelled as illustrative.

---

## 29. Next steps

Recommended by the chat, in priority order:

1. **Validate the six agent responsibilities against the actual UGREEN Developer Package** — exact CLI capabilities, inputs, outputs — to confirm Foreman is buildable, not just good on paper.
2. **Define the Claim-to-Evidence Ledger architecture** — per-agent extracted data, record linkage, discrepancy calculation, traceability back to the source document.
3. **Draft the initial `SKILL.md` package** with every capability checked against the Starter Kit.
4. **Write the 500-word Round 1 proposal** (ten answers, §24.2 word budget), verify word limit, ≤1 MB PDF.
5. **Build the synthetic project dataset** and answer key.
6. **Run the creation-tool validation checks**, then review and test workflow logic against the dataset.
7. **Re-check the Devpost page** for the final dates and rules (Round 2 deadline, winner announcement).
8. **Submit Round 1 well before Nov 16, 14:45 WIB.**
9. **Prepare finalist materials** (Skill, references, test data, validation instructions, demo plan) before the single NAS testing day.

---

## 30. References

Keep these open while developing (from the chat):

1. UGREEN official **Devpost rules** — especially Sections 4 and 6 (submission requirements, judging).
2. UGREEN **Hackathon Starter Kit** — especially sections 5, 6 (UGOS Skill Capability Scope) and 7.
3. **Canadian Office of the Procurement Ombud** — *Contract Administration in Construction Contracts* (P114-33/2025E, July 2025): https://publications.gc.ca/collections/collection_2026/spac-pspc/P114-33-2025-eng.pdf ; news release (14 Jul 2025): https://www.canada.ca/en/procurement-ombudsman/news/2025/07/procurement-ombud-urges-use-of-mediation-services-to-address-issues-in-administration-of-federal-construction-contracts.html ; interview coverage: https://canada.constructconnect.com/?p=186740
4. **Arcadis Construction Disputes Reports** (both read in full): 15th Annual, North America, 2025 — *Construction Disputes in Motion* (PDF copy: https://www.cmaanet.org/sites/default/files/2025-09/202515~1.PDF); 16th Annual, United States, 2026 — *Disruption to Innovation* (https://media.arcadis.com/-/media/project/arcadiscom/com/expertise/global/contract-solutions/2026/2026_construction-disputes-report.pdf). Index: https://www.arcadis.com/en-us/expertise/contract-solutions
5. UGREEN Uliya user guide / Knowledge Center (support.ugnas.com) — assistants, cloud-model data handling, permissions.
6. UGREEN AI NAS pages (nas.ugreen.com, ai.ugreen.com) — hardware specs, capability pages, creation-tool documentation.
7. UGREEN backup guidance — NAS vs. backup.
8. Context sources used in the chat: Shenzhen Stock Exchange / UGREEN investor profile; two UGREEN Kickstarter campaigns; HomeAgent announcement (IFA 2026); Arcadis.

### 30.1 Academic and industry sources added by independent research (2026-11-04)

Verification levels: **Read** / **Abstract** / **Search only** (see §6.4).

| # | Source | Used for | Verification |
|---|---|---|---|
| A1 | Shrestha, P. P. & Zeleke, H. (2018). Effect of Change Orders on Cost and Schedule Overruns of School Building Renovation Projects. *J. Legal Affairs and Dispute Resolution in Eng. and Constr.*, 10(4). https://doi.org/10.1061/(ASCE)LA.1943-4170.0000271 | Change-order cost/schedule impact | Abstract |
| A2 | Ramadhan, J. S. & Waty, M. (2025). Impact of Change Orders on Cost Overruns and Delays in Large-Scale Construction Projects. *Eng., Technol. & Applied Sci. Research*, 15(1), 20291–20299. https://etasr.com/index.php/ETASR/article/view/9449 | Indonesian evidence on change orders | Abstract |
| A3 | Amzafi, N. et al. (2024). A Systematic Review of the Causes and Effects of Variation Orders… *Int. J. Integrated Engineering*, 16(4), 188–203. https://journal.uthm.edu.my/index.php/ijie/article/view/16252 | Causes/effects of variation orders | Abstract |
| A4 | Construction Industry Institute (1994). The Effects of Change on Labor Productivity: Why and How Much (SD-99). https://www.construction-institute.org/the-effects-of-change-on-labor-productivity-why-and-how-much | Productivity loss, timing of change | Read |
| A5 | Ibbs, W. (2005). Impact of Change's Timing on Labor Productivity. *JCEM*, 131(11), 1219. https://doi.org/10.1061/(ASCE)0733-9364(2005)131:11(1219) | Late vs early change | Search only |
| A6 | Hanna, A. S., Camlic, R., Peterson, P. A. & Nordheim, E. V. (2002). Quantitative Definition of Projects Impacted by Change Orders. *JCEM*, 128(1), 57–64. https://doi.org/10.1061/(ASCE)0733-9364(2002)128:1(57) | Statistical definition of change-order impact | Abstract |
| A7 | Kangari, R. (1995). Construction Documentation in Arbitration. *JCEM*, 121(2), 201–208. https://doi.org/10.1061/(ASCE)0733-9364(1995)121:2(201) | Value of comprehensive records | Abstract |
| A8 | McKinsey & Company (2016). Imagining construction's digital future. https://www.mckinsey.com/capabilities/operations/our-insights/imagining-constructions-digital-future | Large-project overrun context | Search only |
| A9 | 2021 JCEM paper on an NLP model for change-order retrieval. https://ascelibrary.com/doi/10.1061/%28ASCE%29CO.1943-7862.0002172 | Closest peer-reviewed NLP work; research gap | Search only (publisher page blocked) |
| A10 | AIA Contract Documents — differences between Change Orders and Construction Change Directives. https://learn.aiacontracts.com/articles/6449229-changes-to-the-contract-differences-between-change-orders-and-construction-change-directives/ | Written change instruments | Search only |
| A11 | Fenwick Elliott — Changes to the Claims provisions in the 2017 FIDIC Red Book. https://www.fenwickelliott.com/knowledge-hub/international-quarterlies/issue-25/changes-to-the-claims-provisions-in-the-2017-fidic-red-book/ | Notice-of-claim time limits | Search only |
| A12 | Verrill — The Value of Photographic Evidence in Construction Litigation (*Construction Executive*). https://constructionexec.com/article/the-value-of-photographic-evidence-in-construction-litigation | Photos as evidence (practitioner) | Search only |

*Statistics about UGREEN, the hackathon and the Project Alpha example come from the source chat and have not been independently re-verified. Statistics in §6.4 were researched independently and carry the verification level shown.*
