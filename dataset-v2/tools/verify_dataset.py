#!/usr/bin/env python3
"""Independently re-derive the expected findings from the FILES (not from the generator's data) and diff them
against ground-truth/answer_key.json. Also checks markers, hint-word leaks, EXIF, audio durations and whisper output.

Usage: python verify_dataset.py <dataset-v2 dir> <scratch dir> [whisper_txt_dir]
Needs: pdftotext, pdftoppm, ffprobe, osascript (macOS Vision OCR via tools/ocr_vision.js), piexif.
"""
import json, math, re, subprocess, sys, difflib, datetime as dt
from pathlib import Path
import piexif

ROOT, SCR = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
WH = Path(sys.argv[3]) if len(sys.argv) > 3 else None
NAS = ROOT / "nas-upload"; AL = NAS / "Project-Alpha"
KEY = json.loads((ROOT / "ground-truth/answer_key.json").read_text())
report, problems = [], []


def log(msg): report.append(msg); print(msg)
def bad(msg): problems.append(msg); log("  MISMATCH: " + msg)
def r(p): return str(p.relative_to(ROOT))
def num(s):
    """'$4,400.00', '-$3,750.00' or OCR's '$4.400.00' -> float (last separator is the decimal point)."""
    s = s.replace("$", "").replace(" ", ""); neg = s.startswith("-"); parts = re.split(r"[.,]", s.lstrip("-"))
    v = float("".join(parts[:-1]) + "." + parts[-1]) if len(parts) > 1 else float(parts[0])
    return -v if neg else v
def days(a, b): return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


# ---------------------------------------------------------------- 1. text of every PDF
TXT, OCRED = {}, []
for p in sorted(NAS.rglob("*.pdf")):
    t = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
    if len(t.strip()) < 20:
        png = SCR / "ocr"; png.mkdir(exist_ok=True)
        base = png / p.stem.replace(" ", "_")
        subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", str(p), str(base)], check=True)
        t = subprocess.run(["osascript", "-l", "JavaScript", str(ROOT / "tools/ocr_vision.js"), str(base) + ".png"],
                           capture_output=True, text=True).stdout
        OCRED.append(r(p))
    TXT[p] = t
log(f"PDFs read: {len(TXT)} (OCR needed for: {OCRED})")
for p, t in TXT.items():
    if "SYNTHETIC TEST DATA" not in t:
        bad(f"no SYNTHETIC TEST DATA marker in {r(p)}")


def T(rel): return TXT[AL / rel]


# ---------------------------------------------------------------- 2. parse Alpha records
c = T("01-Contract/CONTRACT-001_Original-Agreement.pdf")
contract = {m[0]: dict(work=m[1].strip(), qty=float(m[2]), unit=m[3], rate=num(m[4]), value=num(m[5]))
            for m in re.findall(r"^\s*(\d)\s+(.+?)\s{2,}(\d+) (units|m2|m|system)\s+(\$[\d,.]+)\s+(\$[\d,.]+)", c, re.M)}
csum = num(re.search(r"TOTAL CONTRACT SUM\s+(\$[\d,.]+)", c)[1])
assert len(contract) == 6 and sum(i["value"] for i in contract.values()) == csum, contract
excl = re.search(r"Excluded from the Contract Sum:(.+?)\n\s*\n", c, re.S)[1].lower()
cert_days = int(re.search(r"certifies each Payment Application within (\d+) days", c)[1])
notice_days = int(re.search(r"in writing within (\d+) days of encountering", c, re.S)[1]) if re.search(r"in writing within (\d+) days of encountering", c, re.S) else int(re.search(r"within (\d+) days of\s+encountering", c, re.S)[1])
email_co_days = int(re.search(r"within (\d+) days of that email", c, re.S)[1]) if "days of that email" in c else 14
gps_ref = lambda txt: tuple(map(float, re.search(r"GPS\):\s*(-?[\d.]+),\s*(-?[\d.]+)", txt).groups()))
alpha_gps = gps_ref(c)
log(f"Contract: sum {csum}, exclusions '{excl.strip()[:60]}...', certify {cert_days} d, notice {notice_days} d, GPS {alpha_gps}")

cos = {}
for p, t in TXT.items():
    if AL in p.parents and "CHANGE ORDER" in t:
        m = re.search(r"Change Order No\. (CO-\d+)(?: - Revision (\w))?", t)
        signed = re.findall(r"Signed (\d{4}-\d{2}-\d{2})", t)
        cos[m[1] + (m[2] or "")] = dict(no=m[1], rev=m[2], amount=num(re.search(r"Adjustment to Contract Sum\s+(-?\$[\d,.]+)", t)[1]),
                                        signed=signed[0] if len(signed) >= 2 else None, file=r(p), text=t)
log("Change orders: " + ", ".join(f"{k} {v['amount']:+,.0f} {'signed ' + v['signed'] if v['signed'] else 'NOT signed'}" for k, v in sorted(cos.items())))

inv = {}
for p in sorted((AL / "03-Invoices").glob("*.pdf")):
    t = TXT[p]
    amts = [num(a) for a in re.findall(r"\$\s?[\d][\d,.]*\d", t)]
    inv[re.search(r"INV-\d+", t)[0]] = dict(date=re.search(r"Invoice date: ([\d-]+)", t)[1], ref=re.search(r"Reference: (.+)", t)[1].strip(),
                                            amount=max(amts), qty=(re.search(r"(\d+ (?:units|m2|m))\s+\$", t) or [None, "Lump sum"])[1],
                                            desc=re.search(r"Description.*\n\s*(.+?)(?:\s{2,}|$)", t, re.M)[1] if "Description" in t else "", file=r(p))
log("Invoices: " + ", ".join(f"{k} {v['amount']:,.0f} ref {v['ref']}" for k, v in inv.items()))

emails = {r(p): t for p, t in TXT.items() if "Printed email thread" in t and AL in p.parents}
diaries = {}
for p, t in TXT.items():
    if "DAILY SITE DIARY" in t:
        d = re.search(r"Date: (.+)", t)[1].strip()
        for f in ("%d/%m/%Y", "%Y-%m-%d", "%d %b %Y", "%d.%m.%Y"):
            try: diaries[dt.datetime.strptime(d, f).date().isoformat()] = (r(p), t); break
            except ValueError: pass
assert len(diaries) == 4, diaries.keys()

# ---------------------------------------------------------------- 3. re-derive findings
derived = {}   # target -> (class, amount)
rev_by_no = {}
for k, v in cos.items(): rev_by_no.setdefault(v["no"], []).append(v)
seen = {}
for no, v in sorted(inv.items(), key=lambda x: x[1]["date"]):
    ref = v["ref"]; m = re.match(r"(CO-\d+)(?: Revision (\w))?", ref)
    if m:
        revs = rev_by_no.get(m[1], [])
        if len([x for x in revs if x["signed"]]) > 1:
            derived[no] = ("Conflicting", v["amount"]); continue
        co = revs[0]
        if not co["signed"]:
            derived[no] = ("Missing evidence", v["amount"]); derived[no + ":diff"] = v["amount"] - co["amount"]; continue
        dup = seen.get((m[1], v["amount"]))
        seen[(m[1], v["amount"])] = no
        if dup:
            derived[no] = ("Review", v["amount"]); continue
        # work started before signature? (look for diary entries that the CO text points at)
        started = [d for d, (f, t) in diaries.items() if "removal" in t.lower() and "started" in t.lower() and "removal" in co["text"].lower()]
        if started and min(started) < co["signed"]:
            derived[no] = ("Review", v["amount"]); continue
        derived[no] = ("Matched", v["amount"]) if abs(co["amount"] - v["amount"]) < 0.01 else ("Review", v["amount"])
    elif "email" in ref.lower():
        amt_s = f"${v['amount']:,.2f}"
        ok = [f for f, t in emails.items() if re.search(r"\bapproved\b", t, re.I) and amt_s in t]
        co9 = re.search(r"\((CO-\d+)\)", " ".join(emails[f] for f in ok)) if ok else None
        derived[no] = ("Review" if ok else "Missing evidence", v["amount"])
        if co9 and co9[1] not in rev_by_no:
            log(f"  {no}: approval only in email {ok}; {co9[1]} referenced but no such change order file")
    else:
        words = [w for w in ("painting", "decorative", "feature", "door", "floor", "hazardous") if w in v["desc"].lower() and w in excl]
        derived[no] = ("Missing evidence", v["amount"]) if words else ("Review", v["amount"])

# payment applications
pas = {}
for p, t in TXT.items():
    if "PAYMENT APPLICATION" in t and AL in p.parents:
        k = re.search(r"Application No\. (PA-\d+)", t)[1]
        claimed = {m[0]: m[1] for m in re.findall(r"^\s*(\d)\s+.+?\s{2,}\d+ \w+\s+(\d+(?:\.\d+)? \w+|\d+%)\s", t, re.M)}
        g = lambda lbl: num(re.search(lbl + r"\s+(-?\$[\d,.]+)", t)[1])
        pas[k] = dict(gross=g("Gross value to date"), ret=-g("Less retention 5%"), prev=-g("Less previously certified"),
                      due=g("AMOUNT DUE THIS APPLICATION"), claimed=claimed, date=re.search(r"Date of application: ([\d-]+)", t)[1])
for k, v in sorted(pas.items()):
    arith = abs(v["gross"] * 0.95 - v["prev"] - v["due"]) < 0.01
    if not arith: bad(f"{k} arithmetic does not reconcile")
    derived[k] = ("Matched", v["due"]) if arith else ("Review", v["due"])
assert pas["PA-03"]["prev"] == pas["PA-01"]["due"] + pas["PA-02"]["due"]
# contract quantities adjusted by signed omission COs
adj = {i: x["qty"] for i, x in contract.items()}
for v in cos.values():
    m = re.search(r"delete .+? (\d+) m2 of Contract item (\d)", v["text"].replace("\n", " "))
    if m and v["signed"]: adj[m[2]] -= float(m[1])
for item, q in pas["PA-03"]["claimed"].items():
    qn = float(q.split()[0]) if "%" not in q else float(q[:-1]) / 100 * contract[item]["qty"]
    if qn > adj[item] + 1e-9:
        over = (qn - adj[item]) * contract[item]["rate"]
        lbl = {"3": "PA-03 item 3 (internal walls)", "5": "PA-03 item 5 (ceiling tiles)"}.get(item, f"PA-03 item {item}")
        derived[lbl] = ("Review", over)
derived["PA-03"] = ("Review", pas["PA-03"]["due"])     # PA-03 has line findings; whole-application class not scored
pc = TXT[AL / "07 Payments/PC-03.pdf"]
pc_date = dt.datetime.strptime(re.search(r"Date of certificate: (.+)", pc)[1].strip(), "%d %B %Y").date().isoformat()
lag = days(pas["PA-03"]["date"], pc_date)
derived["PC-03 timing"] = ("Review" if lag > cert_days else "Matched", None)
log(f"PA-03 due {pas['PA-03']['due']:,.2f}; PC-03 dated {pc_date}, {lag} days after PA-03 (limit {cert_days})")

# ACM notice timing
first = min(d for d, (f, t) in diaries.items() if "asbestos" in t.lower())
notice = [t for f, t in emails.items() if "clause 4.6" in t]
nd = re.search(r"Sent: \w+ (\d+ \w+ \d{4})", notice[0])[1]
nd = dt.datetime.strptime(nd, "%d %b %Y").date().isoformat()
log(f"ACM first recorded {first}, written notice {nd}: {days(first, nd)} days (limit {notice_days}); CO-008 signed {cos['CO-008']['signed']}")

# unsigned, uninvoiced CO
for k, v in cos.items():
    if not v["signed"] and not any(x["ref"].startswith(v["no"]) for x in inv.values()):
        derived[v["no"]] = ("Missing evidence", v["amount"])
# referenced but missing email
for p, t in TXT.items():
    m = re.search(r"Client email of (\d+) (\w+)", t)
    if m and AL in p.parents:
        found = [f for f, et in emails.items() if re.search(rf"\b{m[1]} {m[2][:3]}", et)]
        if not found: derived[f"Client email of 2026-10-{int(m[1]):02d}"] = ("Missing evidence", None)

# photos
def hav(a, b):
    R = 6371.0; la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
def gps_of(ex):
    g = ex.get("GPS") or {}
    if 2 not in g: return None
    f = lambda v: v[0][0] / v[0][1] + v[1][0] / v[1][1] / 60 + v[2][0] / v[2][1] / 3600
    return ((-1 if g[1] == b"S" else 1) * f(g[2]), (-1 if g[3] == b"W" else 1) * f(g[4]))
gamma_gps = gps_ref(TXT[NAS / "Project-Gamma/01-Contract/CONTRACT-001_Original-Agreement.pdf"])
for p in sorted(NAS.rglob("*.jpg")):
    try: ex = piexif.load(str(p))
    except Exception: ex = {}
    date = (ex.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal) or b"").decode()
    g = gps_of(ex); dist = hav(g, alpha_gps if AL in p.parents else gamma_gps) if g else None
    log(f"photo {r(p)}: EXIF {date or 'none'}, GPS {g and tuple(round(x, 5) for x in g)}, {f'{dist:.2f} km from own site' if dist is not None else 'no GPS'}")
    if AL in p.parents:
        if not date: derived[p.name] = ("Insufficient data", None)
        elif dist > 1.0:
            derived[p.name] = ("Review", None); log(f"  {p.name} is {hav(g, gamma_gps):.2f} km from Gamma site reference")

# audio
for p in sorted(NAS.rglob("*.m4a")):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                             capture_output=True, text=True).stdout)
    log(f"audio {r(p)}: {d:.2f} s")
    if d < 5: derived[p.name] = ("Insufficient data", None)

# distractor projects: every invoice must match its own contract item or signed CO
for proj in ("Project-Beta", "Project-Gamma"):
    texts = {p: t for p, t in TXT.items() if NAS / proj in p.parents}
    ok = 0; total = 0
    for p, t in texts.items():
        if "TAX INVOICE" not in t: continue
        amt = max(num(a) for a in re.findall(r"\$[\d,.]+\d", t)); ref = re.search(r"Reference: (.+)", t)[1].strip(); total += amt
        src = [x for x in texts.values() if ("CHANGE ORDER" in x and ref in x and len(re.findall(r"Signed \d{4}", x)) >= 2)
               or ("TOTAL" in x and "TAX INVOICE" not in x and "CHANGE ORDER" not in x)]
        ok += any(f"${amt:,.2f}" in x for x in src)
    log(f"{proj}: {ok}/{sum('TAX INVOICE' in t for t in texts.values())} invoices matched to own contract/CO; invoiced {total:,.2f}")
    if ok != sum("TAX INVOICE" in t for t in texts.values()) or total != KEY["distractor_projects"][proj]["invoiced"]:
        bad(f"{proj} distractor invoices do not all match")

# ---------------------------------------------------------------- 4. diff against the answer key
log("\nDerived vs answer key:")
for f in KEY["findings"]:
    tgt = f["target"]; dv = derived.get(tgt)
    if dv is None: bad(f"{f['id']} {tgt}: not derived from files"); continue
    ok_cls = dv[0] in (f["cls"], f.get("also"))
    ok_amt = "amount" not in f or dv[1] is None or abs(dv[1] - f["amount"]) < 0.01
    log(f"  {f['id']:4} {tgt:32} key={f['cls']:18} derived={dv[0]:18} {'OK' if ok_cls and ok_amt else 'DIFF'}")
    if not (ok_cls and ok_amt): bad(f"{f['id']} {tgt}: key {f['cls']} {f.get('amount')} vs derived {dv}")
for f in KEY["findings"]:
    for e in f["evidence"]:
        if not (ROOT / e).exists(): bad(f"{f['id']} evidence path does not exist: {e}")
log(f"  evidence paths: {sum(len(f['evidence']) for f in KEY['findings'])} checked")
if derived.get("INV-010:diff") != KEY["totals"]["inv010_over_unsigned_co"]: bad("INV-010 difference")
inv_total = sum(v["amount"] for v in inv.values())
matched = sum(v["amount"] for k, v in inv.items() if derived[k][0] == "Matched")
for name, val in [("invoiced", inv_total), ("invoices_matched", matched), ("invoices_flagged", inv_total - matched),
                  ("pa03_claimed_due", pas["PA-03"]["due"]), ("pc03_certified", num(re.search(r"AMOUNT\s+\$[\d,.]+\s+(\$[\d,.]+)", pc)[1])),
                  ("contract_sum", csum)]:
    if abs(val - KEY["totals"][name]) > 0.01: bad(f"total {name}: files {val} vs key {KEY['totals'][name]}")
    else: log(f"  total {name}: {val:,.2f} OK")

# ---------------------------------------------------------------- 5. leaks
HINTS = re.compile(r"signed|draft|duplicate|dup\b|approved|unapproved|final|superseded|fake|wrong|missing|copy|trap|answer", re.I)
for p in NAS.rglob("*"):
    if HINTS.search(str(p.relative_to(NAS))): bad(f"hint word in path {r(p)}")
LEAK = re.compile(r"answer key|expected class|false.positive|\bF\d{2}\b|\bTP-\d|forbidden|ground.truth", re.I)
for p, t in TXT.items():
    if LEAK.search(t): bad(f"answer-key wording inside {r(p)}: {LEAK.search(t)[0]}")
log("hint/leak scan done")

# ---------------------------------------------------------------- 6. whisper vs scripts
if WH and WH.exists():
    log("\nWhisper (small.en) vs scripts:")
    for tf in sorted((ROOT / "ground-truth/transcripts").glob("*.txt")):
        script = " ".join(l.split(": ", 1)[1] for l in tf.read_text().splitlines()[2:] if ": " in l)
        src = json.loads((ROOT / "ground-truth/answer_key.json").read_text())["recordings"][tf.stem]["file"]
        wt = WH / (Path(src).stem + ".txt")
        hyp = wt.read_text() if wt.exists() else ""
        norm = lambda s: re.findall(r"[a-z0-9]+", s.lower())
        a, b = norm(script), norm(hyp)
        sm = difflib.SequenceMatcher(None, a, b)
        wer = 1 - sum(x.size for x in sm.get_matching_blocks()) / max(1, len(a))
        log(f"  {tf.stem}: script {len(a)} words, whisper {len(b)} words, word error approx {wer:.0%}")
        log(f"     whisper: {' '.join(hyp.split())[:300]}")

(SCR / "verification_results.json").write_text(json.dumps(dict(problems=problems, log=report), indent=2))
print(f"\n{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
