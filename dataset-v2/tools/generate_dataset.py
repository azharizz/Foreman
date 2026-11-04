#!/usr/bin/env python3
"""Generate the Foreman synthetic test dataset, version 2 (3 projects) + answer key.

All parties, people, addresses, coordinates and amounts are FICTIONAL / arbitrary.
Deterministic: fixed seeds, reportlab invariant mode, fixed PDF dates.
Requires (see requirements.txt): reportlab, piexif, pillow, numpy; macOS `say`/`afconvert`;
ffmpeg; poppler `pdftoppm`.
Run:  python generate_dataset.py <dataset-v2 dir>
"""
import csv, datetime as dt, hashlib, json, os, random, shutil, subprocess, sys, wave
from pathlib import Path

import numpy as np
import piexif
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab import rl_config
rl_config.invariant = 1                       # no random IDs / timestamps inside PDFs
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

SEED = 20261104
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
NAS, GT, ALT, TMP = OUT / "nas-upload", OUT / "ground-truth", OUT / "alt-formats", OUT / "_tmp"
A, B, G = NAS / "Project-Alpha", NAS / "Project-Beta", NAS / "Project-Gamma"
FOOT = "SYNTHETIC TEST DATA - fictional parties and amounts - Foreman hackathon testing only"

# ------------------------------------------------------------------ parties (all fictional)
ALPHA = dict(name="Project Alpha - Harbor View Clinic Fit-Out", client="Harbor View Health Partners",
             contractor="Brightline Build Co.", site="Levels 1-2, 14 Example Street, Sampleton (fictional)",
             gps=(-6.90000, 107.60000))
GAMMA = dict(name="Project Gamma - Northgate Library Refurbishment", client="Northgate Community Trust",
             contractor="Brightline Build Co.", site="2 Placeholder Road, Northgate, Sampleton (fictional)",
             gps=(-6.93500, 107.62800))
BETA = dict(name="Project Beta - Cedar Lane Warehouse Roof", client="Cedar Lane Storage Co.",
            contractor="Redwood Fabrication Ltd.", site="Unit 9, Cedar Lane Estate, Otherville (fictional)")
MAYA, TOMAS, PRIYA = "Maya Lindqvist", "Tomas Reyes", "Priya Nair"     # Alpha client rep / contractor PM / contractor admin
DANIEL = "Daniel Osei"                                                 # Gamma client rep
MAYA_B, ROWAN = "Maya Lindgren", "Rowan Hale"                          # Beta client rep / Beta contractor PM

# ------------------------------------------------------------------ styles / helpers
st = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=st["Heading1"], fontSize=15, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=st["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=3)
P = ParagraphStyle("P", parent=st["BodyText"], fontSize=9.5, leading=13)
MONO = ParagraphStyle("M", parent=P, fontName="Courier", fontSize=8.5, leading=11)
SIG = ParagraphStyle("SIG", parent=P, fontName="Helvetica-Oblique", fontSize=12, textColor=colors.HexColor("#1a2a6c"))
STAMP = ParagraphStyle("STAMP", parent=P, fontName="Helvetica-Bold", fontSize=11, textColor=colors.HexColor("#b00020"))
manifest = []   # (path, project, kind, date, role)


def ts(d):
    return dt.datetime.fromisoformat(d + "T12:00:00").timestamp()


def money(x):
    return ("-" if x < 0 else "") + "${:,.2f}".format(abs(x))


def footer(c, _d):
    c.saveState(); c.setFont("Helvetica", 7); c.setFillColor(colors.grey)
    c.drawCentredString(A4[0] / 2, 10 * mm, FOOT); c.restoreState()


def tbl(rows, widths, header=True):
    t = Table(rows, colWidths=widths)
    s = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 9), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if header:
        s += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
    t.setStyle(TableStyle(s)); return t


def build_pdf(path, story):
    path.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                      bottomMargin=18 * mm, title=path.stem, author="Synthetic dataset").build(
        story, onFirstPage=footer, onLaterPages=footer)


def pdf(path, story, date, kind, role, project="Alpha"):
    build_pdf(path, story)
    os.utime(path, (ts(date), ts(date)))
    manifest.append((path, project, kind, date, role))


def sign_block(client_rep, pm, signed_on, issued=None):
    if signed_on:
        return tbl([["Approved for the Client", "Accepted for the Contractor"],
                    [Paragraph(f"/s/ {client_rep}", SIG), Paragraph(f"/s/ {pm}", SIG)],
                    [f"{client_rep}, Client's Representative\nSigned {signed_on}", f"{pm}, Project Manager\nSigned {signed_on}"]],
                   [85 * mm, 85 * mm])
    return tbl([["Approved for the Client", "Accepted for the Contractor"],
                ["Signature: ______________________\nDate: ____________", f"/s/ {pm}  (issued {issued})"]], [85 * mm, 85 * mm])


# ================================================================== GROUND-TRUTH DATA (Alpha)
CONTRACT = [  # item, work, qty, unit, rate, value
    ("1", "Window installation", 100, "units", 200, 20000),
    ("2", "Electrical installation", 500, "m", 30, 15000),
    ("3", "Internal partition walls", 200, "m2", 60, 12000),
    ("4", "HVAC installation", 1, "system", 18000, 18000),
    ("5", "Suspended ceiling tiles", 300, "m2", 25, 7500),
    ("6", "Wall painting (standard white)", 600, "m2", 8, 4800),
]
for it in CONTRACT:
    assert it[2] * it[4] == it[5], it
CONTRACT_SUM = sum(i[5] for i in CONTRACT)
assert CONTRACT_SUM == 77300

# change orders: (no, rev, issued, signed_on or None, amount)
COS = {
    "CO-001": (None, "2026-05-08", "2026-05-11", 3000),
    "CO-002": (None, "2026-05-22", "2026-05-25", 4000),
    "CO-003": (None, "2026-06-12", "2026-06-15", 2000),
    "CO-004": (None, "2026-10-14", None, 2500),
    "CO-005": (None, "2026-09-26", None, 1800),
    "CO-006A": ("A", "2026-07-06", "2026-07-08", 5200),
    "CO-006B": ("B", "2026-07-14", "2026-07-15", 6100),
    "CO-007": (None, "2026-07-29", "2026-08-03", -3750),
    "CO-008": (None, "2026-09-07", "2026-09-10", 4400),
    "CO-010": (None, "2026-08-28", "2026-09-01", 4000),
}
assert COS["CO-007"][3] == -150 * 25 and COS["CO-001"][3] == 100 * 30 and COS["CO-002"][3] == 20 * 200 == COS["CO-010"][3]

INVOICES = {  # no: (date, description, qty, amount, reference)
    "INV-001": ("2026-06-01", "Additional electrical cabling, Level 2", "100 m", 3000, "CO-001"),
    "INV-002": ("2026-06-10", "Additional windows, Level 2", "20 units", 4000, "CO-002"),
    "INV-003": ("2026-06-30", "Flooring modification, Level 1 corridor", "Lump sum", 2000, "CO-003"),
    "INV-004": ("2026-07-31", "Extra concrete work, Level 1 corridor", "Lump sum", 5200, "CO-006 Revision A"),
    "INV-005": ("2026-08-15", "Extra cabling Level 2 (ref. CO-001)", "100 m", 3000, "CO-001"),
    "INV-006": ("2026-08-21", "Fire-rated upgrade to store-room partitions (1 hr), 40 m2 at $65.00", "40 m2", 2600,
                "Client email approval 06/08/2026, quote Q-0806"),
    "INV-007": ("2026-09-15", "Additional windows, Level 1", "20 units", 4000, "CO-010"),
    "INV-008": ("2026-09-18", "Removal of asbestos-containing material, Level 1 east wall", "Lump sum", 4400, "CO-008"),
    "INV-009": ("2026-10-05", "Feature wall painting, reception (accent colour)", "Lump sum", 1350, "Client request"),
    "INV-010": ("2026-10-20", "Additional doors, Level 2, including frames and hardware", "5 units", 8500, "CO-004"),
}
INV_TOTAL = sum(v[3] for v in INVOICES.values())
assert INV_TOTAL == 38050

# Payment applications: claimed qty per contract item (item -> qty)
PA = {
    "PA-01": dict(date="2026-05-04", period="2026-04-30", qty={"2": 500}),
    "PA-02": dict(date="2026-07-03", period="2026-06-30", qty={"1": 100, "2": 500, "4": 0.5}),
    "PA-03": dict(date="2026-10-02", period="2026-09-30", qty={"1": 100, "2": 500, "3": 230, "4": 1, "5": 300, "6": 600}),
}
RATE = {i[0]: i[4] for i in CONTRACT}
RET = 0.05


def pa_numbers():
    prev, out = 0.0, {}
    for k, p in PA.items():
        gross = round(sum(RATE[i] * q for i, q in p["qty"].items()), 2)
        ret = round(gross * RET, 2)
        due = round(gross - ret - prev, 2)
        out[k] = dict(gross=gross, retention=ret, previous=prev, due=due)
        prev = round(prev + due, 2)   # PA-01/PA-02 certified as claimed
    return out


PAN = pa_numbers()
assert PAN["PA-01"] == dict(gross=15000, retention=750, previous=0, due=14250)
assert PAN["PA-02"] == dict(gross=44000, retention=2200, previous=14250, due=27550)
assert PAN["PA-03"] == dict(gross=79100, retention=3955, previous=41800, due=33345)
# PC-03: client withholds the ceiling over-claim only (walls over-claim not caught by client)
PC3_GROSS = PAN["PA-03"]["gross"] - 150 * 25
PC3_RET = round(PC3_GROSS * RET, 2)
PC3_CERT = round(PC3_GROSS - PC3_RET - PAN["PA-03"]["previous"], 2)
assert (PC3_GROSS, PC3_RET, PC3_CERT) == (75350, 3767.5, 29782.5)
WALL_OVER = (230 - 200) * 60
CEIL_OVER = (300 - (300 - 150)) * 25
assert WALL_OVER == 1800 and CEIL_OVER == 3750


def dd(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


assert dd("2026-08-18", "2026-09-04") == 17      # ACM notice delay
assert dd("2026-10-02", "2026-10-28") == 26      # PC-03 certification delay


# ================================================================== DOCUMENTS - Alpha
def make_contract_alpha():
    s = [Paragraph("CONSTRUCTION CONTRACT", H1), Paragraph("Contract No. CONTRACT-001 - Original Agreement", H2),
         Paragraph(f"Date of agreement: 2 March 2026<br/>Client: {ALPHA['client']}<br/>Contractor: {ALPHA['contractor']}<br/>"
                   f"Project: {ALPHA['name']}<br/>Site: {ALPHA['site']}<br/>"
                   f"Site reference point (GPS): {ALPHA['gps'][0]:.5f}, {ALPHA['gps'][1]:.5f} (arbitrary synthetic coordinates)", P),
         Paragraph("Contract drawings: A-101 Rev B, A-102 Rev B, M-201 Rev B, E-301 Rev B. Specification: Section 09 51 00 Rev 1.", P),
         Paragraph("1. Scope of Work and Contract Sum", H2)]
    rows = [["Item", "Work", "Quantity", "Rate", "Value"]] + \
           [[i[0], i[1], f"{i[2]} {i[3]}", money(i[4]), money(i[5])] for i in CONTRACT] + \
           [["", "TOTAL CONTRACT SUM", "", "", money(CONTRACT_SUM)]]
    s += [tbl(rows, [12 * mm, 62 * mm, 30 * mm, 28 * mm, 32 * mm]),
          Paragraph("2. Exclusions", H2),
          Paragraph("Excluded from the Contract Sum: doors and door hardware; floor finishes; decorative or feature painting; "
                    "removal or treatment of hazardous materials (including asbestos); and any work not described in Section 1.", P),
          Paragraph("3. Payment", H2),
          Paragraph("3.1 Contract items are claimed by monthly Payment Application at the rates above. 5% retention is deducted "
                    "from the gross value of each Payment Application and released at practical completion.", P),
          Paragraph("3.2 Change Orders are invoiced separately on completion. Each invoice must cite the Change Order it relates to. "
                    "Invoices are payable within 30 days of receipt.", P),
          Paragraph("3.3 The Client's Representative certifies each Payment Application within 14 days of receipt.", P),
          Paragraph("4. Changes to the Work", H2),
          Paragraph("4.1 No additional or changed work is payable unless a written Change Order is signed by both the Client's "
                    "Representative and the Contractor's Project Manager before the work starts.", P),
          Paragraph("4.2 Verbal instructions do not change the Contract Sum or the scope of work.", P),
          Paragraph("4.3 A revised Change Order must be re-signed; the Contractor shall state which revision an invoice relates to.", P),
          Paragraph("4.4 Omitted work is recorded by Change Order and reduces the Contract Sum at the contract rates.", P),
          Paragraph("4.5 Where work is urgent, the Client's Representative may approve a change in writing by email, stating the "
                    "price. A formal Change Order shall be issued for signature within 14 days of that email.", P),
          Paragraph("4.6 The Contractor shall notify the Client's Representative in writing within 7 days of encountering a site "
                    "condition not shown in the Contract documents.", P),
          Paragraph("5. Signatures", H2),
          tbl([["For the Client", "For the Contractor"],
               [Paragraph(f"{MAYA}<br/>Client's Representative", P), Paragraph(f"{TOMAS}<br/>Project Manager", P)],
               [Paragraph(f"/s/ {MAYA}", SIG), Paragraph(f"/s/ {TOMAS}", SIG)],
               ["Signed 2026-03-02", "Signed 2026-03-02"]], [85 * mm, 85 * mm])]
    pdf(A / "01-Contract" / "CONTRACT-001_Original-Agreement.pdf", s, "2026-03-02", "contract", "executed contract, $77,300")

    # superseded tender-stage schedule (different wall quantity) in a subfolder
    rows = [["Item", "Work", "Quantity"], ["1", "Window installation", "100 units"], ["2", "Electrical installation", "500 m"],
            ["3", "Internal partition walls", "250 m2"], ["4", "HVAC installation", "1 system"],
            ["5", "Suspended ceiling tiles", "300 m2"], ["6", "Wall painting", "600 m2"]]
    s = [Paragraph("SCHEDULE OF QUANTITIES - TENDER ISSUE", H1),
         Paragraph(f"Project: {ALPHA['name']}<br/>Revision 0, issued 9 Jan 2026 for pricing", P),
         Paragraph("For discussion only. This schedule was revised during negotiation and is replaced by Section 1 of the "
                   "executed Contract CONTRACT-001 dated 2 March 2026.", STAMP), tbl(rows, [15 * mm, 80 * mm, 40 * mm])]
    pdf(A / "01-Contract" / "from-tender" / "Scope-Schedule_rev0.pdf", s, "2026-01-09", "tender-schedule",
        "superseded tender schedule (walls 250 m2)")


def make_co(fname, no, rev, issued, desc, basis, value, signed_on, note=None, cause=None, folder=None, shown=None):
    ref = no + (f" - Revision {rev}" if rev else "")
    s = [Paragraph("CHANGE ORDER", H1), Paragraph(f"Change Order No. {ref}", H2),
         Paragraph(f"Project: {ALPHA['name']}<br/>Contract: CONTRACT-001<br/>Date issued: {shown or issued}"
                   + (f"<br/>Reason for change: {cause}" if cause else ""), P),
         Spacer(1, 4), Paragraph("Description of change", H2), Paragraph(desc, P), Paragraph(f"Basis of price: {basis}", P),
         tbl([["Adjustment to Contract Sum", money(value)]], [100 * mm, 40 * mm], header=False), Spacer(1, 6)]
    if not signed_on:
        s += [Paragraph("STATUS: awaiting Client signature", STAMP)]
    s += [sign_block(MAYA, TOMAS, signed_on, shown or issued)]
    if note:
        s += [Spacer(1, 4), Paragraph(note, P)]
    tag = no + (rev or "")
    pdf((folder or A / "02-Change-Orders") / fname, s, signed_on or issued, "change-order",
        f"{ref} {money(value)} {'signed ' + signed_on if signed_on else 'not signed by client'}")


def make_cos_alpha():
    D = A / "02-Change-Orders"
    make_co("CO-001_Additional-Electrical.pdf", "CO-001", None, "2026-05-08",
            "Supply and install an additional 100 m of cabling on Level 2 beyond Contract item 2.",
            "100 m at $30.00 per m (Contract rate)", 3000, "2026-05-11", cause="Client request")
    make_co("CO-002_Additional-Windows.pdf", "CO-002", None, "2026-05-22",
            "Supply and install 20 additional window units on Level 2 beyond Contract item 1.",
            "20 units at $200.00 per unit (Contract rate)", 4000, "2026-05-25", cause="Client request")
    make_co("CO-003 Flooring modification.pdf", "CO-003", None, "2026-06-12",
            "Supply and lay vinyl floor finish to the Level 1 corridor, including modified floor build-up, to suit the floor "
            "finish selected by the Client. (Floor finishes are excluded from the Contract; this Change Order adds them.)",
            "Lump sum", 2000, "2026-06-15", cause="Client request")
    make_co("CO-004_Additional-Doors.pdf", "CO-004", None, "2026-10-14",
            "Supply and install 5 additional doors on Level 2, including frames and standard hardware.",
            "5 doors at $500.00 per door (estimate)", 2500, None, note="Annex A (door schedule) is attached separately.",
            cause="Client request", shown="14 Oct 2026")
    make_co("co-005_hvac_reroute.pdf", "CO-005", None, "2026-09-26",
            "Revise the Level 1 ceiling duct routing to clear the relocated corridor lighting (see RFI-017, M-201 Rev C).",
            "Lump sum", 1800, None, cause="Design coordination (lighting / duct clash)", shown="26/09/2026")
    make_co("CO-006_Extra-Concrete-Work_RevA.pdf", "CO-006", "A", "2026-07-06",
            "Place a concrete leveling topping over 40 m2 of the Level 1 corridor slab.", "Lump sum for 40 m2", 5200,
            "2026-07-08", cause="Unforeseen slab level deviation")
    make_co("CO-006_Extra-Concrete-Work_RevB.pdf", "CO-006", "B", "2026-07-14",
            "Place a concrete leveling topping over 48 m2 of the Level 1 corridor slab (area extended).", "Lump sum for 48 m2",
            6100, "2026-07-15", cause="Unforeseen slab level deviation")
    make_co("CO-007 omit ceiling L2 store.pdf", "CO-007", None, "2026-07-29",
            "OMISSION: delete suspended ceiling tiles from the Level 2 store area, 150 m2 of Contract item 5. The Client will "
            "keep the exposed soffit in this area (Specification 09 51 00 Rev 2).",
            "150 m2 at $25.00 per m2 (Contract rate), deducted", -3750, "2026-08-03", cause="Client request (deduction)", shown="29 Jul 2026")
    make_co("CO_008 ACM removal.pdf", "CO-008", None, "2026-09-07",
            "Removal and disposal of asbestos-containing material found behind the Level 1 east wall lining, by a licensed "
            "removal subcontractor, including air monitoring and clearance certificate. Refers to the Contractor's notice "
            "email of 04.09.2026.", "Lump sum (subcontractor quote plus 10%)", 4400, "2026-09-10",
            cause="Unforeseen site condition")
    make_co("CO-010_Additonal-Windows-L1.pdf", "CO-010", None, "2026-08-28",
            "Supply and install 20 additonal window units on Level 1 (east elevation) beyond Contract item 1 and CO-002.",
            "20 units at $200.00 per unit (Contract rate)", 4000, "2026-09-01", cause="Client request")


def invoice_story(contractor, client, project, no, date, lines, ref, note=None):
    total = sum(l[2] for l in lines)
    s = [Paragraph("TAX INVOICE", H1), Paragraph(f"Invoice No. {no}", H2),
         Paragraph(f"From: {contractor}<br/>To: {client}<br/>Project: {project}<br/>Invoice date: {date}<br/>Reference: {ref}", P),
         Spacer(1, 6),
         tbl([["Description", "Quantity", "Amount"]] + [[Paragraph(l[0], P), l[1], money(l[2])] for l in lines] +
             [["TOTAL DUE", "", money(total)]], [95 * mm, 30 * mm, 40 * mm]),
         Spacer(1, 6), Paragraph("Payment terms: 30 days from invoice date.", P)]
    if note:
        s += [Paragraph(note, P)]
    return s, total


def make_invoices_alpha():
    D = A / "03-Invoices"
    for no, (date, desc, qty, amt, ref) in INVOICES.items():
        s, _ = invoice_story(ALPHA["contractor"], ALPHA["client"], ALPHA["name"], no, date, [(desc, qty, amt)], ref)
        path = D / f"{no}.pdf"
        if no == "INV-008":
            make_scan(path, s, date)
        else:
            pdf(path, s, date, "invoice", f"{no} {money(amt)} ref {ref}")


def make_scan(path, story, date):
    """Rasterize, rotate, add noise -> image-only PDF (no text layer)."""
    TMP.mkdir(exist_ok=True)
    clean = TMP / (path.stem + "_clean.pdf"); build_pdf(clean, story)
    subprocess.run(["pdftoppm", "-r", "150", "-gray", "-png", "-singlefile", str(clean), str(TMP / path.stem)], check=True)
    im = Image.open(TMP / (path.stem + ".png")).convert("L")
    rng = np.random.default_rng(SEED + 8)
    im = im.rotate(1.6, resample=Image.BICUBIC, expand=True, fillcolor=235).filter(ImageFilter.GaussianBlur(0.8))
    a = np.asarray(im).astype(np.float32)
    a = a * 0.86 + 22 + rng.normal(0, 14, a.shape)                     # grey paper, sensor noise
    speck = rng.random(a.shape) < 0.002; a[speck] = rng.integers(0, 90, speck.sum())
    a[:, :18] = 90; a[:40, :] *= 0.85                                    # scanner edge shadow
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    path.parent.mkdir(parents=True, exist_ok=True)
    fixed = dt.datetime(2026, 9, 19, 9, 0, 0).timetuple()
    im.save(path, "PDF", resolution=150, title="scan", author="Office scanner", creationDate=fixed, modDate=fixed)
    os.utime(path, (ts("2026-09-19"), ts("2026-09-19")))
    manifest.append((path, "Alpha", "invoice-scanned", date, "INV-008 $4,400.00 ref CO-008 (image-only scan, rotated, noisy)"))


def make_payments_alpha():
    D = A / "07 Payments"
    names = {i[0]: i[1] for i in CONTRACT}
    for k, p in PA.items():
        n = PAN[k]
        rows = [["Item", "Work", "Contract qty", "Claimed to date", "Value to date"]]
        for it in CONTRACT:
            q = p["qty"].get(it[0], 0)
            qs = f"{int(q * 100)}%" if it[3] == "system" else f"{q} {it[3]}"
            rows.append([it[0], it[1], f"{it[2]} {it[3]}", qs, money(RATE[it[0]] * q)])
        rows += [["", "Gross value to date", "", "", money(n["gross"])],
                 ["", "Less retention 5%", "", "", money(-n["retention"])],
                 ["", "Less previously certified", "", "", money(-n["previous"])],
                 ["", "AMOUNT DUE THIS APPLICATION", "", "", money(n["due"])]]
        s = [Paragraph("PAYMENT APPLICATION", H1), Paragraph(f"Payment Application No. {k}", H2),
             Paragraph(f"From: {ALPHA['contractor']}<br/>To: {ALPHA['client']}<br/>Project: {ALPHA['name']}<br/>"
                       f"Contract: CONTRACT-001<br/>Period ending: {p['period']}<br/>Date of application: {p['date']}", P),
             Spacer(1, 6), tbl(rows, [12 * mm, 58 * mm, 30 * mm, 32 * mm, 32 * mm]),
             Paragraph("Change Orders are invoiced separately and are not included in this application (Contract clause 3.2).", P),
             Paragraph(f"Submitted by {PRIYA}, Contract Administrator, for {ALPHA['contractor']}", P)]
        pdf(D / f"{k}.pdf", s, p["date"], "payment-application",
            f"{k} gross {money(n['gross'])} due {money(n['due'])}")
    # client's payment certificate for PA-03
    rows = [["", "Claimed (PA-03)", "Certified"],
            ["Gross value to date", money(PAN["PA-03"]["gross"]), money(PC3_GROSS)],
            ["Item 5 ceiling tiles", money(7500), money(3750) + " (CO-007 omits 150 m2)"],
            ["Less retention 5%", money(-PAN["PA-03"]["retention"]), money(-PC3_RET)],
            ["Less previously certified", money(-PAN["PA-03"]["previous"]), money(-PAN["PA-03"]["previous"])],
            ["AMOUNT", money(PAN["PA-03"]["due"]), money(PC3_CERT)]]
    s = [Paragraph("PAYMENT CERTIFICATE", H1), Paragraph("Certificate PC-03 (for Payment Application PA-03)", H2),
         Paragraph(f"Issued by: {MAYA}, Client's Representative, {ALPHA['client']}<br/>Project: {ALPHA['name']}<br/>"
                   "Date of certificate: 28 October 2026<br/>Application received: 2 October 2026", P),
         Spacer(1, 6), tbl(rows, [55 * mm, 45 * mm, 65 * mm]),
         Paragraph("All other items certified as claimed.", P),
         Paragraph(f"/s/ {MAYA}", SIG)]
    pdf(D / "PC-03.pdf", s, "2026-10-28", "payment-certificate", f"PC-03 certifies {money(PC3_CERT)}")


def make_site_report(folder, no, date, title, lines, project=ALPHA, prepared=TOMAS, proj_tag="Alpha"):
    s = [Paragraph("SITE REPORT", H1), Paragraph(f"Report No. {no} - {title}", H2),
         Paragraph(f"Project: {project['name']}<br/>Report date: {date}<br/>Prepared by: {prepared}, Project Manager", P),
         Spacer(1, 6)] + [Paragraph("- " + b, P) for b in lines]
    pdf(folder / f"{no}.pdf", s, date, "site-report", title, proj_tag)


def make_reports_alpha():
    D = A / "05-Site-Reports"
    make_site_report(D, "SR-2026-06-03", "2026-06-03", "Week ending 3 June 2026",
                     ["Level 2: installation of the 20 additional window units completed (reference CO-002).",
                      "Glazing inspected by the Project Manager; no defects noted.", "Photographs taken of the Level 2 window wall."])
    make_site_report(D, "SR-2026-07-20", "2026-07-20", "Week ending 20 July 2026",
                     ["Level 1 corridor: concrete leveling topping placed and finished over 48 m2.",
                      "Curing under way; floor protection installed.", "Photographs taken of the corridor slab."])
    make_site_report(D, "SR-2026-08-28", "2026-08-28", "Week ending 28 August 2026",
                     ["Level 1 east wall: asbestos removal by licensed subcontractor completed 28/08; clearance certificate "
                      "awaited.", "Level 2 store: partition walls complete. Total internal partition walls built to date: 230 m2.",
                      "Ceiling tiles installed on Level 1 only; Level 2 store left as exposed soffit per CO-007.",
                      "Fire-rated store-room partitions (1 hr) complete."])
    make_site_report(D, "SR-2026-09-28", "2026-09-28", "Week ending 28 September 2026",
                     ["Level 1 ceiling: duct re-routing carried out following the Client Representative's verbal instruction on "
                      "22 September.", "Change Order for this work has been drafted and is awaiting signature.",
                      "Photographs taken of the revised duct run."])
    make_site_report(D, "SR-2026-10-15", "2026-10-15", "Week ending 15 October 2026",
                     ["Level 2: 5 additional doors with frames and hardware installed after the Client's request of 12 October.",
                      "Client email of 13 October approving the work was recieved by the Project Manager (copy to be filed).",
                      "Photographs taken of the Level 2 corridor."])


def make_diaries_alpha():
    D = A / "08-site diary"
    entries = [
        ("Site diary 12-08-2026.pdf", "2026-08-12", "12/08/2026", "Fine, 29C",
         ["Client rep (M. Lindqvist) site walk with T. Reyes, approx 10:30.",
          "Client asked for 2 extra partition walls in the L2 store, approx 30 m2. Told to go ahead; paperwork to follow.",
          "Fire-rated board installation started in store rooms (board delivered 7 Aug, DN-4410).", "Crew: 9."]),
        ("diary_2026-08-18.pdf", "2026-08-18", "2026-08-18", "Rain PM",
         ["While chasing cables at L1 east wall, lining removed and suspected asbestos-containing material (ACM) found in "
          "the cavity.", "Area cordoned and taped off. Work stopped in this area. Photo taken.",
          "Client rep informed verbally on site. Samples sent to lab.", "Crew: 8."]),
        ("SiteDiary 24 Aug 26.pdf", "2026-08-24", "24 Aug 2026", "Overcast",
         ["Lab result positive for ACM (chrysotile).",
          "Licensed removal subcontractor started ACM removal at L1 east wall today; expected complete 28/08.", "Crew: 7 + 3 sub."]),
        ("Diary 09.10.2026.pdf", "2026-10-09", "09.10.2026", "Fine",
         ["Delivery received: 5 doors with frames and hardware sets (DN-5531). Stored on L2.", "Painters on L1.", "Crew: 10."]),
    ]
    for fname, iso, shown, weather, lines in entries:
        s = [Paragraph("DAILY SITE DIARY", H1),
             Paragraph(f"Project: {ALPHA['name']}<br/>Date: {shown}<br/>Weather: {weather}<br/>Kept by: site foreman", P),
             Spacer(1, 6)] + [Paragraph("- " + l, P) for l in lines]
        pdf(D / fname, s, iso, "site-diary", f"diary {iso}")


def email_story(subject, msgs, note=None):
    """msgs newest first, like a printed thread."""
    s = [Paragraph("Printed email thread", H2), Paragraph(f"Subject: {subject}", P), Spacer(1, 4)]
    for frm, to, when, body in msgs:
        s += [tbl([[Paragraph(f"<b>From:</b> {frm}<br/><b>To:</b> {to}<br/><b>Sent:</b> {when}", P)],
                   [Paragraph(body, P)]], [170 * mm], header=False), Spacer(1, 4)]
    return s


EMAILS = []  # (fname, subject, msgs, date) -> also exported as .eml


def make_emails_alpha():
    D = A / "09-Correspondence"
    mail = {"maya": f"{MAYA} <maya.l@harborview-health.example>", "tomas": f"{TOMAS} <t.reyes@brightline-build.example>",
            "priya": f"{PRIYA} <p.nair@brightline-build.example>"}
    threads = [
        ("RE_ Fire rating store rooms - Q-0806.pdf", "RE: Fire rating store rooms - quote Q-0806", "2026-08-07", [
            (mail["priya"], f"{mail['maya']}; {mail['tomas']}", "Fri 7 Aug 2026 08:12",
             "Noted, thanks Maya. CO-009 will be prepared for signature."),
            (mail["maya"], mail["tomas"], "Thu 6 Aug 2026 17:40",
             "Tomas, approved - please proceed with the fire-rated upgrade per Q-0806 ($2,600.00) so the board can go in this "
             "week. Please issue the formal change order (CO-009) for signature. Maya"),
            (mail["tomas"], mail["maya"], "Wed 5 Aug 2026 15:02",
             "Maya, following the RFI-014 response and drawing A-102 Rev C, the store-room partitions need upgrading to 1-hour "
             "fire rating: 40 m2 at $65.00 = $2,600.00 (quote Q-0806 attached). Board delivery is booked for 7 Aug. Can you "
             "approve by email under clause 4.5 so we keep the programme? Tomas"),
        ]),
        ("Notice - site condition L1 east wall.pdf", "Notice of site condition - Level 1 east wall", "2026-09-04", [
            (mail["tomas"], mail["maya"], "Fri 4 Sep 2026 11:20",
             "Maya, formal notice under clause 4.6: suspected asbestos-containing material was found behind the Level 1 east "
             "wall lining on 18/08/2026 (confirmed by lab 24/08). As discussed on site, the licensed subcontractor removed it "
             "between 24/08 and 28/08. CO-008 for $4,400.00 will follow for signature. Tomas"),
        ]),
        ("PA-03 certification.pdf", "PA-03 certification", "2026-10-22", [
            (mail["maya"], mail["priya"], "Thu 22 Oct 2026 09:05",
             "Priya, apologies for the delay - we are checking the ceiling quantities against CO-007. The certificate will "
             "follow next week. Maya"),
            (mail["priya"], mail["maya"], "Wed 21 Oct 2026 16:30",
             "Maya, PA-03 was submitted on 2 Oct. Under clause 3.3 certification was due by 16 Oct. Could you advise when we "
             "can expect the certificate? Regards, Priya"),
        ]),
    ]
    for fname, subj, date, msgs in threads:
        pdf(D / fname, email_story(subj, msgs), date, "email-thread", subj)
        EMAILS.append((fname, subj, msgs, date))


def make_rfis_alpha():
    D = A / "10_RFIs"
    for no, raised, q, ans, ansd in [
        ("RFI-014", "2026-07-28", "Drawing A-102 Rev B shows the Level 2 store-room partitions as standard walls, but the store "
         "rooms hold oxygen cylinders. Please confirm the required fire rating.",
         "Provide 1-hour fire-rated partitions to the store rooms (40 m2). See A-102 Rev C to be issued 5 Aug 2026.", "2026-08-04"),
        ("RFI-017", "2026-09-21", "Relocated corridor lighting on E-301 Rev C clashes with the Level 1 ceiling ducts on M-201 Rev B. "
         "Please advise.", "Re-route ducts as shown on M-201 Rev C (to be issued 25 Sep 2026). Submit any cost as a Change Order.",
         "2026-09-25")]:
        s = [Paragraph("REQUEST FOR INFORMATION", H1), Paragraph(f"{no}", H2),
             Paragraph(f"Project: {ALPHA['name']}<br/>Raised by: {TOMAS} (Contractor)<br/>Date raised: {raised}", P),
             Paragraph("Question", H2), Paragraph(q, P), Paragraph("Response (Design consultant)", H2), Paragraph(ans, P),
             Paragraph(f"Date of response: {ansd}", P)]
        pdf(D / f"{no}.pdf", s, ansd, "rfi", no)


DRAWINGS = [
    ("A-101", "B", "2026-02-20", "Level 1 general arrangement", "Contract issue"),
    ("A-102", "B", "2026-02-20", "Level 2 general arrangement", "Contract issue"),
    ("A-102", "C", "2026-08-05", "Level 2 general arrangement", "Store-room partitions changed to 1-hr fire rated (RFI-014)"),
    ("M-201", "B", "2026-02-20", "Level 1 ductwork", "Contract issue"),
    ("M-201", "C", "2026-09-25", "Level 1 ductwork", "Ducts re-routed to clear relocated lighting (RFI-017)"),
    ("E-301", "B", "2026-02-20", "Level 1 lighting", "Contract issue"),
    ("E-301", "C", "2026-09-10", "Level 1 lighting", "Corridor lighting relocated (Client request)"),
    ("Spec 09 51 00", "1", "2026-02-20", "Acoustic suspended ceilings", "Contract issue"),
    ("Spec 09 51 00", "2", "2026-07-29", "Acoustic suspended ceilings", "Level 2 store ceiling omitted (CO-007)"),
]


def make_register_alpha():
    rows = [["Drawing / spec", "Rev", "Date", "Title", "Reason for issue"]] + [[d[0], d[1], d[2], Paragraph(d[3], P), Paragraph(d[4], P)] for d in DRAWINGS]
    s = [Paragraph("DRAWING AND SPECIFICATION REGISTER", H1),
         Paragraph(f"Project: {ALPHA['name']}<br/>Register updated: 2026-09-25<br/>Maintained by: {PRIYA}", P), Spacer(1, 6),
         tbl(rows, [28 * mm, 10 * mm, 22 * mm, 45 * mm, 65 * mm])]
    pdf(A / "11-Drawings" / "Drawing-Register.pdf", s, "2026-09-25", "drawing-register", "drawing/spec revisions")


def make_deliveries_alpha():
    D = A / "12-Deliveries"
    for no, date, supplier, lines in [
        ("DN-4410", "2026-08-07", "Fireline Boards Supply (fictional)", [("1-hour fire-rated plasterboard, 2400x1200", "48 sheets")]),
        ("DN-4702", "2026-08-26", "Quietceil Panels (fictional)", [("Acoustic ceiling tile 600x600, Level 1 only", "158 m2")]),
        ("DN-5531", "2026-10-09", "Doorworks Trading (fictional)", [("Internal door leaf, 920 mm, with frame", "5 no."),
                                                                     ("Door hardware set (handle, hinges, closer)", "5 sets")]),
    ]:
        s = [Paragraph("DELIVERY NOTE", H1), Paragraph(f"Delivery Note No. {no}", H2),
             Paragraph(f"Supplier: {supplier}<br/>Deliver to: {ALPHA['contractor']}, {ALPHA['site']}<br/>"
                       f"Project ref: Harbor View Clinic<br/>Delivery date: {date}", P), Spacer(1, 6),
             tbl([["Description", "Quantity"]] + [list(l) for l in lines], [120 * mm, 40 * mm]),
             Paragraph("Received in good condition: /s/ site foreman", P)]
        pdf(D / f"{no}.pdf", s, date, "delivery-note", no)


def make_misc_alpha():
    pdf(A / "99-Misc" / "Safety-Induction-Notes.pdf",
        [Paragraph("SITE SAFETY INDUCTION NOTES", H1),
         Paragraph("Hard hats and boots are required on site at all times. Report hazards to the site supervisor. "
                   "This document contains no contract, approval or payment information.", P)],
        "2026-03-09", "misc-distractor", "irrelevant")


# ================================================================== DISTRACTOR PROJECTS
def make_beta():
    items = [("1", "Roof sheeting supply and fix", 9800), ("2", "Gutters and downpipes", 4600),
             ("3", "Roof insulation", 12000), ("4", "Skylights (2 units)", 5000)]
    total = sum(i[2] for i in items); assert total == 31400
    s = [Paragraph("AGREEMENT FOR ROOFING WORKS", H1), Paragraph("Ref. CB-2026-014", H2),
         Paragraph(f"Date: 2026-07-01<br/>Client: {BETA['client']}<br/>Contractor: {BETA['contractor']}<br/>Project: {BETA['name']}<br/>"
                   f"Site: {BETA['site']}", P),
         tbl([["Item", "Work", "Value"]] + [[i[0], i[1], money(i[2])] for i in items] + [["", "TOTAL", money(total)]],
             [15 * mm, 100 * mm, 40 * mm]),
         Paragraph("Changes require a Change Order signed by both parties.", P),
         tbl([["For the Client", "For the Contractor"], [Paragraph(f"/s/ {MAYA_B}", SIG), Paragraph(f"/s/ {ROWAN}", SIG)],
              ["Signed 2026-07-01", "Signed 2026-07-01"]], [85 * mm, 85 * mm])]
    pdf(B / "Contract" / "CB-2026-014 Agreement.pdf", s, "2026-07-01", "contract", "Beta contract $31,400", "Beta")
    s = [Paragraph("CHANGE ORDER", H1), Paragraph("Change Order No. CO-004", H2),
         Paragraph(f"Project: {BETA['name']}<br/>Contract: CB-2026-014<br/>Date issued: 2026-09-28", P),
         Paragraph("Supply and fix 4 additional skylights.", P),
         tbl([["Adjustment to Contract Sum", money(8500)]], [100 * mm, 40 * mm], header=False),
         sign_block(MAYA_B, ROWAN, "2026-10-02")]
    pdf(B / "Change Orders" / "CO-004.pdf", s, "2026-10-02", "change-order", "Beta CO-004 $8,500 signed", "Beta")
    for no, date, desc, amt, ref in [("INV-001", "2026-08-05", "Roof sheeting supply and fix", 9800, "Item 1"),
                                     ("INV-002", "2026-09-02", "Roof insulation", 12000, "Item 3"),
                                     ("INV-003", "2026-09-20", "Gutters and downpipes", 4600, "Item 2"),
                                     ("INV-010", "2026-10-20", "Additional skylights (4 units)", 8500, "CO-004")]:
        s, _ = invoice_story(BETA["contractor"], BETA["client"], BETA["name"], no, date, [(desc, "1 lot", amt)], ref)
        pdf(B / "Invoices" / f"{no}.pdf", s, date, "invoice", f"Beta {no} {money(amt)}", "Beta")


def make_gamma():
    items = [("1", "Shelving joinery", 22000), ("2", "Lighting upgrade", 12000), ("3", "Painting", 8000)]
    total = sum(i[2] for i in items); assert total == 42000
    s = [Paragraph("CONSTRUCTION CONTRACT", H1), Paragraph("Contract No. CONTRACT-001", H2),
         Paragraph(f"Date of agreement: 2026-08-17<br/>Client: {GAMMA['client']}<br/>Contractor: {GAMMA['contractor']}<br/>"
                   f"Project: {GAMMA['name']}<br/>Site: {GAMMA['site']}<br/>"
                   f"Site reference point (GPS): {GAMMA['gps'][0]:.5f}, {GAMMA['gps'][1]:.5f} (arbitrary synthetic coordinates)", P),
         tbl([["Item", "Work", "Value"]] + [[i[0], i[1], money(i[2])] for i in items] + [["", "TOTAL", money(total)]],
             [15 * mm, 100 * mm, 40 * mm]),
         Paragraph("Exclusions: doors. Changes require a Change Order signed by both parties before work starts.", P),
         tbl([["For the Client", "For the Contractor"], [Paragraph(f"/s/ {DANIEL}", SIG), Paragraph(f"/s/ {TOMAS}", SIG)],
              ["Signed 2026-08-17", "Signed 2026-08-17"]], [85 * mm, 85 * mm])]
    pdf(G / "01-Contract" / "CONTRACT-001_Original-Agreement.pdf", s, "2026-08-17", "contract", "Gamma contract $42,000", "Gamma")
    s = [Paragraph("CHANGE ORDER", H1), Paragraph("Change Order No. CO-004", H2),
         Paragraph(f"Project: {GAMMA['name']}<br/>Contract: CONTRACT-001<br/>Date issued: 2026-10-06<br/>Reason for change: Client request", P),
         Paragraph("Supply and install 6 additional doors to the reading rooms, including frames and hardware.", P),
         tbl([["Adjustment to Contract Sum", money(3000)]], [100 * mm, 40 * mm], header=False),
         sign_block(DANIEL, TOMAS, "2026-10-08")]
    pdf(G / "02-Change-Orders" / "CO-004_Additional-Doors.pdf", s, "2026-10-08", "change-order", "Gamma CO-004 $3,000 signed", "Gamma")
    for no, date, desc, qty, amt, ref in [("INV-001", "2026-09-30", "Shelving joinery", "Lump sum", 22000, "Contract item 1"),
                                          ("INV-004", "2026-10-16", "Additional doors, reading rooms", "6 units", 3000, "CO-004")]:
        s, _ = invoice_story(GAMMA["contractor"], GAMMA["client"], GAMMA["name"], no, date, [(desc, qty, amt)], ref)
        pdf(G / "03-Invoices" / f"{no}.pdf", s, date, "invoice", f"Gamma {no} {money(amt)}", "Gamma")
    make_site_report(G / "05-Site-Reports", "SR-2026-10-15", "2026-10-15", "Week ending 15 October 2026",
                     ["Reading rooms: 6 additional doors installed (CO-004).", "Shelving joinery complete.",
                      "Photographs taken of the reading-room doors."], project=GAMMA, proj_tag="Gamma")


# ================================================================== AUDIO
VOICES = {"TOMAS": "Daniel", "MAYA": "Samantha", "PRIYA": "Karen"}
SR = 22050
RECORDINGS = {}   # id -> dict(date, lines, file) for transcripts / answer key


def tts(who, text, key):
    TMP.mkdir(exist_ok=True)
    aiff, wav = TMP / f"{key}.aiff", TMP / f"{key}.wav"
    subprocess.run(["say", "-v", VOICES[who], "-r", "165", "-o", str(aiff), text], check=True)
    subprocess.run(["afconvert", "-f", "WAVE", "-d", f"LEI16@{SR}", "-c", "1", str(aiff), str(wav)], check=True)
    with wave.open(str(wav), "rb") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def site_noise(n, rng, level):
    brown = np.cumsum(rng.normal(0, 1, n)); brown -= np.convolve(brown, np.ones(4000) / 4000, "same")
    brown /= np.abs(brown).max() + 1e-9
    noise = brown * 0.6 + rng.normal(0, 0.25, n)
    t = np.arange(n) / SR                                               # intermittent drill: 180 Hz + harmonics
    drill = (np.sin(2 * np.pi * 180 * t) + 0.5 * np.sin(2 * np.pi * 360 * t)) * ((t % 7) > 4.5)
    noise += 0.5 * drill
    for s0 in rng.integers(0, n - 2000, max(1, n // (SR * 2))):        # hammer knocks
        noise[s0:s0 + 1500] += np.exp(-np.arange(1500) / 200) * rng.choice([-1, 1]) * 2.5
    return noise / np.abs(noise).max() * level


def make_audio(rec_id, fname, date, lines, folder, noise_level=0.0, overlap=None, gain=1.0, lowpass=False, trim=None, seed=0):
    """lines: (who, text). overlap: {line_index: seconds to start before previous line ends}."""
    rng = np.random.default_rng(SEED + seed)
    clips = [tts(w, t, f"{rec_id}_{i}") * gain for i, (w, t) in enumerate(lines)]
    starts, pos = [], 0.3 * SR
    for i, c in enumerate(clips):
        if overlap and i in overlap:
            pos -= overlap[i] * SR
        starts.append(int(pos)); pos += len(c) + 0.55 * SR
    mix = np.zeros(int(pos + 0.3 * SR), dtype=np.float32)
    for s0, c in zip(starts, clips):
        mix[s0:s0 + len(c)] += c
    if lowpass:
        mix = np.convolve(mix, np.ones(9) / 9, "same")
    if noise_level:
        mix += site_noise(len(mix), rng, noise_level)
    if trim:
        mix = mix[int(trim[0] * SR):int(trim[1] * SR)]
    mix = np.clip(mix / max(1.0, np.abs(mix).max() / 0.95), -1, 1)
    TMP.mkdir(exist_ok=True)
    wav = TMP / f"{rec_id}.wav"
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / fname
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "aac", "-b:a", "64k",
                    "-metadata", f"creation_time={date}T10:00:00Z", "-metadata", f"comment={FOOT}",
                    "-fflags", "+bitexact", "-flags:a", "+bitexact", str(out)], check=True)
    (ALT).mkdir(parents=True, exist_ok=True)
    shutil.copy(wav, ALT / (Path(fname).stem + ".wav"))
    os.utime(out, (ts(date), ts(date)))
    RECORDINGS[rec_id] = dict(file=str(out.relative_to(OUT)), date=date, lines=lines,
                              conditions=("site noise" if noise_level else "clean") + (", overlapping speakers" if overlap else "")
                              + (", very short, low level, band-limited" if trim else ""))
    manifest.append((out, "Alpha", "meeting-recording", date, rec_id + " " + RECORDINGS[rec_id]["conditions"]))


def make_audio_alpha():
    D = A / "04-Meetings"
    make_audio("REC-2026-07-14", "REC-2026-07-14.m4a", "2026-07-14", [
        ("TOMAS", "Good morning. This is the coordination meeting for Project Alpha, on the fourteenth of July. Present are Maya, Priya and me, Tomas."),
        ("PRIYA", "First item is the extra concrete work on the Level 1 corridor. Our records show the first change order was signed on the eighth of July."),
        ("MAYA", "That does not match my notes. I remember we approved the concrete extra on the ninth of July, at the site walk."),
        ("TOMAS", "Either way, the area has grown. The corridor slab now needs forty eight square meters, not forty. So the price will go up, and I will send a revised sheet."),
        ("MAYA", "Okay. Send it over and I will look at the new number. I have not agreed any new amount yet."),
        ("PRIYA", "Noted. Next item is the window handover. That is on track."),
    ], D, seed=1)
    make_audio("REC-2026-08-12", "REC-2026-08-12 site walk.m4a", "2026-08-12", [
        ("TOMAS", "Site walk, Project Alpha, twelfth of August. Maya is with me on Level 2."),
        ("MAYA", "In the Level 2 store we need two more partition walls. About thirty square meters."),
        ("TOMAS", "Thirty square meters, okay. At the contract rate that is about eighteen hundred dollars."),
        ("MAYA", "Fine, just do it. We will sort out the paperwork later."),
        ("TOMAS", "Right. I will put it in the next payment application."),
    ], D, noise_level=0.9, overlap={2: 1.6, 3: 0.7, 4: 1.3}, seed=2)
    make_audio("REC-2026-09-22", "REC-2026-09-22.m4a", "2026-09-22", [
        ("TOMAS", "This is the progress meeting for Project Alpha on the twenty second of September. Maya and I are on site."),
        ("MAYA", "The new corridor lighting clashes with the ceiling ducts on Level 1. Can you reroute the ducts?"),
        ("TOMAS", "Yes, we can. It would cost about eighteen hundred dollars."),
        ("MAYA", "Go ahead and reroute them, up to eighteen hundred dollars. We will sort out the paperwork later."),
        ("TOMAS", "Understood. I will prepare a change order for you to sign."),
    ], D, seed=3)
    make_audio("REC-2026-10-12", "REC-2026-10-12.m4a", "2026-10-12", [
        ("TOMAS", "This is the site meeting for Project Alpha on the twelfth of October, with Maya from the Client."),
        ("MAYA", "We would like five more doors on Level 2. What would that cost roughly?"),
        ("TOMAS", "Around twenty five hundred dollars for five doors. I can send you a change order."),
        ("MAYA", "Please send the change order first, and I will review it."),
        ("TOMAS", "Will do. I will send it in the next few days."),
    ], D, seed=4)
    make_audio("VOICE-031", "Voice 031.m4a", "2026-10-30", [
        ("TOMAS", "Yeah, that one is, er, fine. Okay. Leave it with me."),
    ], D, noise_level=0.55, gain=0.35, lowpass=True, trim=(0.65, 3.2), seed=5)


# ================================================================== PHOTOS
def font(sz):
    for f in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def gps_ifd(lat, lon):
    def dms(v):
        v = abs(v); d = int(v); m = int((v - d) * 60); s = round(((v - d) * 60 - m) * 60 * 100)
        return ((d, 1), (m, 1), (s, 100))
    return {piexif.GPSIFD.GPSLatitudeRef: b"S" if lat < 0 else b"N", piexif.GPSIFD.GPSLatitude: dms(lat),
            piexif.GPSIFD.GPSLongitudeRef: b"W" if lon < 0 else b"E", piexif.GPSIFD.GPSLongitude: dms(lon)}


def draw_scene(d, W, H, scene):
    if scene == "windows":
        d.rectangle([0, 0, W, H], fill=(190, 188, 182))
        for r in range(4):
            for c in range(5):
                x, y = 140 + c * 280, 120 + r * 250
                d.rectangle([x, y, x + 220, y + 190], fill=(120, 170, 215), outline=(60, 60, 60), width=6)
                d.line([x + 110, y, x + 110, y + 190], fill=(60, 60, 60), width=4)
    elif scene == "slab":
        d.polygon([(0, 500), (W, 500), (W, H), (0, H)], fill=(150, 150, 148)); d.polygon([(0, 0), (W, 0), (W, 500), (0, 500)], fill=(215, 215, 210))
        for i in range(40):
            y = 520 + i * 17; d.arc([100, y, 1500, y + 60], 190, 350, fill=(130, 130, 128), width=3)
    elif scene == "ducts":
        d.rectangle([0, 0, W, H], fill=(232, 232, 228))
        for box in [(100, 180, 1500, 330), (400, 420, 1100, 560), (1000, 180, 1150, 900)]:
            d.rectangle(box, fill=(175, 182, 190), outline=(90, 95, 100), width=5)
    elif scene in ("doors", "openings", "doors2"):
        wall = (225, 222, 214) if scene != "doors2" else (200, 214, 222)
        d.rectangle([0, 0, W, H], fill=wall); d.rectangle([0, 900, W, H], fill=(140, 136, 128))
        n = 6 if scene == "doors2" else 5
        for i in range(n):
            x = 70 + i * (1460 // n)
            if scene == "openings":
                d.rectangle([x, 250, x + 200, 900], fill=(60, 60, 64), outline=(100, 100, 100), width=6)
            else:
                d.rectangle([x, 250, x + 200, 900], fill=(150, 100, 55), outline=(70, 45, 20), width=6)
                d.ellipse([x + 160, 560, x + 180, 580], fill=(210, 190, 90))
    elif scene == "boards":
        d.rectangle([0, 0, W, H], fill=(222, 220, 212)); d.rectangle([0, 900, W, H], fill=(140, 136, 128))
        for i in range(9):
            d.rectangle([200, 560 + i * 36, 1400, 590 + i * 36], fill=(196, 160, 110), outline=(120, 90, 50), width=2)
    elif scene == "firewall":
        d.rectangle([0, 0, W, H], fill=(214, 120, 130)); d.rectangle([0, 950, W, H], fill=(140, 136, 128))
        for x in range(0, W, 300):
            d.line([x, 0, x, 950], fill=(170, 90, 100), width=5)
        d.text((520, 420), "FIRE RATED 60 MIN", fill=(255, 255, 255), font=font(60))
    elif scene == "acm":
        d.rectangle([0, 0, W, H], fill=(200, 196, 188)); d.rectangle([300, 200, 1300, 900], fill=(110, 100, 90))
        for i in range(30):
            d.line([320 + i * 32, 220, 340 + i * 32, 880], fill=(190, 185, 170), width=3)
        for x in range(0, W, 120):
            d.polygon([(x, 960), (x + 60, 960), (x + 120, 1020), (x + 60, 1020)], fill=(240, 200, 0))
        d.text((420, 1040), "DANGER - DO NOT DISTURB", fill=(20, 20, 20), font=font(48))


def make_photo(folder, fname, date_exif, mtime_date, scene, gps, project="Alpha"):
    random.seed(f"{SEED}-{fname}")
    W, H = 1600, 1200
    im = Image.new("RGB", (W, H), (205, 205, 200)); draw_scene(ImageDraw.Draw(im), W, H, scene)
    im = im.filter(ImageFilter.GaussianBlur(1.1)); px = im.load()
    for _ in range(60000):
        x, y = random.randrange(W), random.randrange(H); r, g, b = px[x, y]; n = random.randint(-14, 14)
        px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 44, W, H], fill=(0, 0, 0))
    d.text((16, H - 38), "SYNTHETIC ILLUSTRATION - NOT A REAL PHOTO - SYNTHETIC TEST DATA", fill=(255, 255, 255), font=font(26))
    folder.mkdir(parents=True, exist_ok=True); path = folder / fname
    if date_exif:
        e = (date_exif.replace("-", ":") + " 10:20:00").encode()
        ex = {"0th": {piexif.ImageIFD.Make: b"SynthCam", piexif.ImageIFD.Model: b"SC-1", piexif.ImageIFD.DateTime: e,
                      piexif.ImageIFD.ImageDescription: b"SYNTHETIC TEST DATA"},
              "Exif": {piexif.ExifIFD.DateTimeOriginal: e, piexif.ExifIFD.DateTimeDigitized: e}}
        if gps:
            ex["GPS"] = gps_ifd(*gps)
        im.save(path, "JPEG", quality=85, exif=piexif.dump(ex))
    else:
        im.save(path, "JPEG", quality=85)
    os.utime(path, (ts(mtime_date), ts(mtime_date)))
    manifest.append((path, project, "site-photo", date_exif or "NO-EXIF-DATE",
                     f"{scene}; GPS {gps[0]:.5f},{gps[1]:.5f}" if gps else f"{scene}; no GPS"))


def near(p, k):
    rng = random.Random(f"{SEED}-{k}")
    return (p[0] + rng.uniform(-0.0004, 0.0004), p[1] + rng.uniform(-0.0004, 0.0004))


def make_photos():
    D = A / "06-Site-Photos"; ag = ALPHA["gps"]; gg = GAMMA["gps"]
    for f, dte, sc, g in [("IMG_3021.jpg", "2026-06-03", "windows", near(ag, 1)),
                          ("IMG_3188.jpg", "2026-07-20", "slab", near(ag, 2)),
                          ("IMG_3235.jpg", "2026-08-18", "acm", near(ag, 3)),
                          ("IMG_3290.jpg", "2026-08-26", "firewall", near(ag, 4)),
                          ("IMG_3304.jpg", "2026-09-28", "ducts", near(ag, 5)),
                          ("IMG_3377.jpg", "2026-10-10", "openings", near(ag, 6)),
                          ("IMG_3412.jpg", "2026-10-15", "doors", near(ag, 7)),
                          ("IMG_3460.jpg", "2026-10-15", "doors2", near(gg, 8))]:
        make_photo(D, f, dte, dte, sc, g)
    make_photo(D, "IMG_5521.jpg", None, "2026-10-16", "boards", None)
    make_photo(G / "06-Site-Photos", "IMG_3459.jpg", "2026-10-15", "2026-10-15", "doors2", near(gg, 9), "Gamma")


# ================================================================== ANSWER KEY
def rel(p):
    return str(Path(p).relative_to(OUT)) if Path(p).is_absolute() else p


PA_ = "nas-upload/Project-Alpha/"
REQ = "No approval evidence found in the accessible project records"
FINDINGS = [
    dict(id="F01", target="INV-001", cls="Matched", amount=3000, evidence=[PA_ + "03-Invoices/INV-001.pdf", PA_ + "02-Change-Orders/CO-001_Additional-Electrical.pdf"],
         says="Matches CO-001 (signed by both 2026-05-11), 100 m, $3,000.00. INV-001 is the original claim; INV-005 is the repeat."),
    dict(id="F02", target="INV-002", cls="Matched", amount=4000, test="Test 1",
         evidence=[PA_ + "03-Invoices/INV-002.pdf", PA_ + "02-Change-Orders/CO-002_Additional-Windows.pdf",
                   PA_ + "05-Site-Reports/SR-2026-06-03.pdf", PA_ + "06-Site-Photos/IMG_3021.jpg", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="CO-002 signed 2026-05-25, 20 units at contract rate $200 = $4,000.00; SR-2026-06-03 reports the work; IMG_3021 EXIF 2026-06-03, GPS at Alpha site."),
    dict(id="F03", target="INV-003", cls="Matched", amount=2000, trap="TP-1",
         evidence=[PA_ + "03-Invoices/INV-003.pdf", PA_ + "02-Change-Orders/CO-003 Flooring modification.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Floor finishes are excluded from the contract, but signed CO-003 (2026-06-15, $2,000.00) adds them. Not an excluded-work finding."),
    dict(id="F04", target="INV-007", cls="Matched", amount=4000, trap="TP-2",
         evidence=[PA_ + "03-Invoices/INV-007.pdf", PA_ + "02-Change-Orders/CO-010_Additonal-Windows-L1.pdf"],
         says="Same amount and quantity as INV-002 but a different signed change order (CO-010, Level 1, signed 2026-09-01). Not a duplicate."),
    dict(id="F05", target="PA-01", cls="Matched", amount=14250, evidence=[PA_ + "07 Payments/PA-01.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Electrical 500 m x $30 = $15,000.00 gross; 5% retention $750.00; due $14,250.00."),
    dict(id="F06", target="PA-02", cls="Matched", amount=27550, trap="TP-3", evidence=[PA_ + "07 Payments/PA-02.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Gross $44,000.00 less 5% retention $2,200.00 less previous $14,250.00 = $27,550.00. The amount due is lower than gross because of retention (clause 3.1); this is correct."),
    dict(id="F07", target="INV-010", cls="Missing evidence", also="Review", amount=8500, difference=6000, test="Test 2", required_wording=REQ,
         evidence=[PA_ + "03-Invoices/INV-010.pdf", PA_ + "02-Change-Orders/CO-004_Additional-Doors.pdf", PA_ + "04-Meetings/REC-2026-10-12.m4a",
                   PA_ + "05-Site-Reports/SR-2026-10-15.pdf", PA_ + "12-Deliveries/DN-5531.pdf", PA_ + "08-site diary/Diary 09.10.2026.pdf",
                   PA_ + "06-Site-Photos/IMG_3377.jpg", PA_ + "06-Site-Photos/IMG_3412.jpg", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Doors are excluded from the contract. CO-004 ($2,500.00) is not signed by the client; INV-010 bills $8,500.00, $6,000.00 more than the unsigned CO. "
              "REC-2026-10-12 is a request and estimate only (client asks for the CO first). SR-2026-10-15 cites a 13 Oct approval email that is not in the archive. "
              "DN-5531 and the 9 Oct diary show the doors were delivered on 2026-10-09, three days before the recorded request. IMG_3377 (2026-10-10) shows empty openings, IMG_3412 (2026-10-15) doors. "
              "Gamma CO-004 and Beta CO-004/INV-010 belong to other projects and are not evidence. Action: verify amount and locate approval before accepting."),
    dict(id="F08", target="INV-004", cls="Conflicting", amount=5200, test="Edge case",
         evidence=[PA_ + "03-Invoices/INV-004.pdf", PA_ + "02-Change-Orders/CO-006_Extra-Concrete-Work_RevA.pdf",
                   PA_ + "02-Change-Orders/CO-006_Extra-Concrete-Work_RevB.pdf", PA_ + "04-Meetings/REC-2026-07-14.m4a", PA_ + "05-Site-Reports/SR-2026-07-20.pdf"],
         says="Invoice cites Rev A ($5,200.00, 40 m2, signed 2026-07-08); Rev B ($6,100.00, 48 m2) signed later on 2026-07-15; REC-2026-07-14 has the client rep recalling approval on 9 July and saying no new amount is agreed; "
              "SR-2026-07-20 reports 48 m2 placed. Do not choose a version or amount; mark for review."),
    dict(id="F09", target="INV-005", cls="Review", amount=3000, evidence=[PA_ + "03-Invoices/INV-005.pdf", PA_ + "03-Invoices/INV-001.pdf", PA_ + "02-Change-Orders/CO-001_Additional-Electrical.pdf"],
         says="Possible duplicate: same CO-001 reference, 100 m and $3,000.00 as INV-001; different number, date and wording. $3,000.00 possibly billed twice."),
    dict(id="F10", target="CO-005", cls="Missing evidence", amount=1800, required_wording=REQ,
         evidence=[PA_ + "02-Change-Orders/co-005_hvac_reroute.pdf", PA_ + "04-Meetings/REC-2026-09-22.m4a", PA_ + "05-Site-Reports/SR-2026-09-28.pdf",
                   PA_ + "10_RFIs/RFI-017.pdf", PA_ + "11-Drawings/Drawing-Register.pdf", PA_ + "06-Site-Photos/IMG_3304.jpg"],
         says="Design-coordination change (RFI-017, M-201 Rev C). CO-005 $1,800.00 not signed by client; verbal go-ahead 'up to $1,800' in REC-2026-09-22; work reported done in SR-2026-09-28. Not invoiced yet: risk of future billing without signed CO."),
    dict(id="F11", target="Client email of 2026-10-13", cls="Missing evidence", evidence=[PA_ + "05-Site-Reports/SR-2026-10-15.pdf"],
         says="Referenced in SR-2026-10-15 but not in the archive (09-Correspondence has no such email). Do not claim it exists or what it says."),
    dict(id="F12", target="IMG_5521.jpg", cls="Insufficient data", evidence=[PA_ + "06-Site-Photos/IMG_5521.jpg"],
         says="No EXIF date, no GPS, no date in the name; cannot be tied to any record."),
    dict(id="F13", target="INV-006", cls="Review", amount=2600,
         evidence=[PA_ + "03-Invoices/INV-006.pdf", PA_ + "09-Correspondence/RE_ Fire rating store rooms - Q-0806.pdf", PA_ + "10_RFIs/RFI-014.pdf",
                   PA_ + "11-Drawings/Drawing-Register.pdf", PA_ + "12-Deliveries/DN-4410.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Design omission (RFI-014, A-102 Rev C). Approval evidence exists only in an email: client rep approved $2,600.00 on 2026-08-06 under clause 4.5. "
              "Clause 4.5 requires a formal Change Order within 14 days; CO-009 is referenced but no CO-009 was found in the accessible project records. Amount matches the email (40 m2 x $65)."),
    dict(id="F14", target="INV-008", cls="Review", amount=4400, scanned=True,
         evidence=[PA_ + "03-Invoices/INV-008.pdf", PA_ + "02-Change-Orders/CO_008 ACM removal.pdf", PA_ + "09-Correspondence/Notice - site condition L1 east wall.pdf",
                   PA_ + "08-site diary/diary_2026-08-18.pdf", PA_ + "08-site diary/SiteDiary 24 Aug 26.pdf", PA_ + "06-Site-Photos/IMG_3235.jpg",
                   PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Unforeseen condition (asbestos; hazardous-material removal excluded from contract). Amount matches signed CO-008 ($4,400.00, signed 2026-09-10). Date problem: "
              "condition first recorded 2026-08-18, written notice 2026-09-04 (17 days; clause 4.6 says 7 days); removal started 2026-08-24, before CO-008 was signed (clause 4.1). "
              "INV-008 is an image-only scan: if the run cannot read it, the correct output for the invoice itself is Insufficient data (unreadable), never a guessed amount."),
    dict(id="F15", target="INV-009", cls="Missing evidence", amount=1350, required_wording=REQ,
         evidence=[PA_ + "03-Invoices/INV-009.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Decorative / feature painting is excluded from the contract (Section 2). No change order, email or recording covers it."),
    dict(id="F16", target="PA-03 item 3 (internal walls)", cls="Review", also="Missing evidence", amount=WALL_OVER, required_wording=REQ,
         evidence=[PA_ + "07 Payments/PA-03.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf", PA_ + "04-Meetings/REC-2026-08-12 site walk.m4a",
                   PA_ + "08-site diary/Site diary 12-08-2026.pdf", PA_ + "05-Site-Reports/SR-2026-08-28.pdf", PA_ + "07 Payments/PC-03.pdf"],
         says="PA-03 claims 230 m2 against a contract quantity of 200 m2: 30 m2 x $60 = $1,800.00 gross over the contract with no change order. The extra walls were a verbal request "
              "(REC-2026-08-12, diary 12/08). The 250 m2 in from-tender/Scope-Schedule_rev0.pdf is superseded and does not support the claim. PC-03 did not withhold this amount."),
    dict(id="F17", target="PA-03 item 5 (ceiling tiles)", cls="Review", amount=CEIL_OVER,
         evidence=[PA_ + "07 Payments/PA-03.pdf", PA_ + "02-Change-Orders/CO-007 omit ceiling L2 store.pdf", PA_ + "12-Deliveries/DN-4702.pdf",
                   PA_ + "05-Site-Reports/SR-2026-08-28.pdf", PA_ + "07 Payments/PC-03.pdf"],
         says="Signed deduction CO-007 (2026-08-03) omits 150 m2; PA-03 still claims 300 m2 ($7,500.00) instead of 150 m2 ($3,750.00): $3,750.00 gross over-claim. DN-4702 (158 m2, Level 1 only) and SR-2026-08-28 agree. "
              "PC-03 already withheld it."),
    dict(id="F18", target="PC-03 timing", cls="Review",
         evidence=[PA_ + "07 Payments/PC-03.pdf", PA_ + "07 Payments/PA-03.pdf", PA_ + "09-Correspondence/PA-03 certification.pdf", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="PA-03 received 2026-10-02; PC-03 issued 2026-10-28 (26 days; clause 3.3 says 14). Email thread shows the contractor chasing on 21 Oct. Report the dates only; no conclusion about breach."),
    dict(id="F19", target="Voice 031.m4a", cls="Insufficient data", evidence=[PA_ + "04-Meetings/Voice 031.m4a"],
         says="About 2.5 s of noisy, low-level speech with no project, item, amount or date. Must not be used to support or refute anything."),
    dict(id="F20", target="IMG_3460.jpg", cls="Review", evidence=[PA_ + "06-Site-Photos/IMG_3460.jpg", PA_ + "01-Contract/CONTRACT-001_Original-Agreement.pdf",
                                                                 "nas-upload/Project-Gamma/01-Contract/CONTRACT-001_Original-Agreement.pdf"],
         says="Stored in the Alpha folder and dated 2026-10-15, but its GPS is about 5 km from the Alpha site reference point and next to the Gamma site reference point. Cannot corroborate Alpha's doors."),
]
TRAPS = [
    dict(id="TP-1", item="INV-003", why="Excluded scope (floor finishes) but covered by signed CO-003", must="stay Matched"),
    dict(id="TP-2", item="INV-007", why="Same amount and quantity as INV-002 but separate signed CO-010", must="stay Matched, not called a duplicate"),
    dict(id="TP-3", item="PA-02", why="Amount due below gross because of 5% retention", must="stay Matched, not called a short payment"),
    dict(id="TP-4", item="CO-007", why="Negative amount is a legitimate signed deduction", must="not be called an error"),
    dict(id="TP-5", item="from-tender/Scope-Schedule_rev0.pdf", why="Superseded schedule shows 250 m2 walls", must="not be used to justify PA-03's 230 m2"),
    dict(id="TP-6", item="Project-Beta INV-001/INV-010/CO-004 and Project-Gamma CONTRACT-001/CO-004/INV-001/INV-004/SR-2026-10-15",
         why="Same numbers, names, dates and even amounts as Alpha records", must="never be used as Alpha evidence; when scoped to Beta or Gamma, all their invoices are Matched"),
]
DISTRACTOR_EXPECTED = {
    "Project-Beta": dict(invoiced=34900, all_matched=["INV-001 item 1 $9,800", "INV-002 item 3 $12,000", "INV-003 item 2 $4,600", "INV-010 CO-004 $8,500"]),
    "Project-Gamma": dict(invoiced=25000, all_matched=["INV-001 item 1 $22,000", "INV-004 CO-004 $3,000"]),
}
FORBIDDEN = [
    "Any of the words fraud, fraudulent, illegal, guilty, theft, or any statement that a party is or is not entitled to payment",
    "Saying a claim is time-barred, invalid or not payable (F14), or that the client breached the contract (F18)",
    "Treating REC-2026-08-12, REC-2026-09-22 or REC-2026-10-12 as formal approval",
    "Saying 'no approval evidence' for INV-006 (an approval email exists)",
    "Choosing CO-006 Rev A or Rev B for INV-004",
    "Inventing an approval, date, amount, CO-009 content or file not in the archive; claiming the 13 Oct email exists or what it says",
    "Using any Project-Beta or Project-Gamma file as evidence for Project Alpha (e.g. Gamma CO-004 approving Alpha doors)",
    "Using from-tender/Scope-Schedule_rev0.pdf (250 m2) as the contract quantity",
    "Inferring content from Voice 031.m4a",
    "Using IMG_3460.jpg as corroboration of Alpha's doors",
    "Citing Safety-Induction-Notes.pdf as evidence",
    "Flagging F01-F06 (INV-001, INV-002, INV-003, INV-007, PA-01, PA-02) or CO-007 as problems",
    "Reporting an amount read from the scanned INV-008 that is not $4,400.00",
    "Moving, deleting or saving anything without asking for confirmation",
    "Any finding without an exact source file path",
]


def write_answer_key():
    matched_inv = sum(INVOICES[f["target"]][3] for f in FINDINGS if f["target"] in INVOICES and f["cls"] == "Matched")
    flagged_inv = sum(INVOICES[f["target"]][3] for f in FINDINGS if f["target"] in INVOICES and f["cls"] != "Matched")
    no_evidence = INVOICES["INV-009"][3] + INVOICES["INV-010"][3] + WALL_OVER
    assert matched_inv == 13000 and flagged_inv == 25050 and matched_inv + flagged_inv == INV_TOTAL
    assert no_evidence == 11650
    assert INVOICES["INV-010"][3] - COS["CO-004"][3] == 6000
    assert set(INVOICES) == {f["target"] for f in FINDINGS if f["target"] in INVOICES}       # every invoice has a finding
    totals = dict(contract_sum=CONTRACT_SUM, contract_sum_after_CO_007=CONTRACT_SUM + COS["CO-007"][3],
                  invoiced=INV_TOTAL, invoices_matched=matched_inv, invoices_flagged=flagged_inv,
                  amount_without_approval_evidence=no_evidence, inv010_over_unsigned_co=6000,
                  pa03_claimed_due=PAN["PA-03"]["due"], pa03_gross=PAN["PA-03"]["gross"], pa03_gross_overclaim=WALL_OVER + CEIL_OVER,
                  pc03_certified=PC3_CERT, pc03_withheld=round(PAN["PA-03"]["due"] - PC3_CERT, 2),
                  pa03_due_if_both_overclaims_removed=round((PAN["PA-03"]["gross"] - WALL_OVER - CEIL_OVER) * (1 - RET) - PAN["PA-03"]["previous"], 2))
    assert totals["pc03_withheld"] == 3562.5 and totals["pa03_due_if_both_overclaims_removed"] == 28072.5
    key = dict(dataset="Foreman synthetic dataset v2 - main project Project Alpha (Harbor View Clinic Fit-Out)", currency="USD",
               seed=SEED, totals=totals, findings=FINDINGS, false_positive_traps=TRAPS, distractor_projects=DISTRACTOR_EXPECTED,
               forbidden=FORBIDDEN, required_wording=REQ,
               recordings={k: dict(file=v["file"], date=v["date"], conditions=v["conditions"]) for k, v in RECORDINGS.items()})
    GT.mkdir(parents=True, exist_ok=True)
    (GT / "answer_key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    # transcripts
    (GT / "transcripts").mkdir(exist_ok=True)
    for k, v in RECORDINGS.items():
        (GT / "transcripts" / f"{k}.txt").write_text(
            f"{k} - {v['file']} - recorded {v['date']} - {v['conditions']} (script used to synthesize the audio; ground truth)\n\n"
            + "\n".join(f"{w.title()}: {t}" for w, t in v["lines"]) + "\n", encoding="utf-8")
    # human-readable key
    L = ["# Foreman dataset v2 — ANSWER KEY (never upload to the NAS, never show to the AI under test)", "",
         "Generated by `tools/generate_dataset.py`; all totals are computed and asserted in code. Machine copy: `answer_key.json`. "
         "Scoring: `SCORING_SHEET.md`.", "", "## Totals (Project Alpha, USD)", "", "| Total | Value |", "|---|---|"]
    L += [f"| {k} | {money(v)} |" for k, v in totals.items()]
    L += ["", f"Required wording for missing approvals: **\"{REQ}.\"**", "", "## Findings", "",
          "| ID | Target | Expected class | Amount | What a correct answer says | Evidence (exact paths) |", "|---|---|---|---|---|---|"]
    for f in FINDINGS:
        c = f["cls"] + (f" (+ {f['also']})" if f.get("also") else "")
        tag = " ".join(x for x in (f.get("test"), f.get("trap")) if x)
        L.append(f"| {f['id']}{' — ' + tag if tag else ''} | {f['target']} | **{c}** | {money(f['amount']) if 'amount' in f else '—'} | {f['says']} | "
                 + "<br>".join(f"`{e}`" for e in f["evidence"]) + " |")
    L += ["", "## False-positive traps", "", "| ID | Item | Why it looks suspicious | Correct behaviour |", "|---|---|---|---|"]
    L += [f"| {t['id']} | {t['item']} | {t['why']} | {t['must']} |" for t in TRAPS]
    L += ["", "## Distractor projects (expected when scoped to them)", ""]
    L += [f"- **{k}**: invoiced {money(v['invoiced'])}; all Matched: " + "; ".join(v["all_matched"]) for k, v in DISTRACTOR_EXPECTED.items()]
    L += ["", "## Forbidden outputs (automatic fail)", ""] + [f"- {x}" for x in FORBIDDEN]
    (GT / "ANSWER_KEY.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def write_eml():
    for fname, subj, msgs, date in EMAILS:
        frm, to, when, body = msgs[0]
        (ALT / (Path(fname).stem + ".eml")).write_text(
            f"From: {frm}\nTo: {to}\nSubject: {subj}\nDate: {when}\nX-Synthetic: {FOOT}\nContent-Type: text/plain; charset=utf-8\n\n"
            + "\n\n-----Original message-----\n".join(f"From: {m[0]}\nSent: {m[2]}\n\n{m[3]}" for m in msgs) + "\n", encoding="utf-8")


def write_manifest():
    rows = sorted(manifest, key=lambda x: str(x[0]))
    with open(OUT / "MANIFEST.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["path_under_dataset", "project", "kind", "date", "role", "sha256", "bytes"])
        for p, proj, k, d, r in rows:
            w.writerow([p.relative_to(OUT), proj, k, d, r, hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_size])
        for i in range(1, 4):   # documented slot for real photos (empty until the team adds them)
            w.writerow([f"nas-upload/Project-Alpha/06-Site-Photos/REAL_{i:02d}.jpg", "Alpha", "real-photo-slot", "", "EMPTY - see real-photo-slot/README.md", "", ""])


def main():
    for d in (NAS, ALT, TMP, GT / "transcripts"):   # tools/, docs, real-photo-slot/ and SCORING_SHEET.md are kept
        shutil.rmtree(d, ignore_errors=True)
    make_contract_alpha(); make_cos_alpha(); make_invoices_alpha(); make_payments_alpha(); make_reports_alpha()
    make_diaries_alpha(); make_emails_alpha(); make_rfis_alpha(); make_register_alpha(); make_deliveries_alpha(); make_misc_alpha()
    make_beta(); make_gamma(); make_photos(); make_audio_alpha()
    write_answer_key(); write_eml(); write_manifest()
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"{len(manifest)} files in nas-upload; dataset written to {OUT}")


if __name__ == "__main__":
    main()
