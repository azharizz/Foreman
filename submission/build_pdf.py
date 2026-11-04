#!/usr/bin/env python3
"""Render PROPOSAL.md to a PDF (A4) and check the Round 1 limits (500 words in the ten answers, 1 MB file).
Usage: python build_pdf.py PROPOSAL.md Foreman_Proposal.pdf   (needs reportlab)"""
import re, sys
from pathlib import Path
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

src, out = Path(sys.argv[1]), Path(sys.argv[2])
md = src.read_text(encoding="utf-8")
import os
if os.environ.get("DRAFT") == "1":   # draft build: show unfilled fields visibly
    md = re.sub(r"\{([A-Z_]+)\}", r"[TO FILL: \1]", md)
assert not re.search(r"\{[A-Z_]+\}", md), "unfilled placeholder in proposal (set DRAFT=1 for a draft)"

# word limit: ten answers only (team and third-party block after '---' is excluded by the rules)
answers = md.split("\n---\n")[0]
words = sum(len(re.findall(r"[A-Za-z0-9$][A-Za-z0-9'’.,/$%+-]*", b.partition("\n")[2]))
            for b in re.split(r"^## ", answers, flags=re.M)[1:])
print("answer words:", words)
assert words <= 500, "over 500 words"

st = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=st["Title"], fontSize=15, spaceAfter=2)
H2 = ParagraphStyle("H2", parent=st["Heading2"], fontSize=10.5, spaceBefore=6, spaceAfter=1)
P = ParagraphStyle("P", parent=st["BodyText"], fontSize=9.2, leading=12, spaceAfter=2)


def inline(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", s)


story, bullets = [], []


def flush():
    global bullets
    if bullets:
        story.append(ListFlowable([ListItem(Paragraph(inline(b), P), leftIndent=10) for b in bullets],
                                  bulletType="bullet", start="•", leftIndent=10))
        bullets = []


for line in md.splitlines():
    if line.startswith("- "):
        bullets.append(line[2:]); continue
    flush()
    if line.startswith("# "):
        story.append(Paragraph(inline(line[2:]), H1))
    elif line.startswith("## "):
        story.append(Paragraph(inline(line[3:]), H2))
    elif line.strip() == "---":
        story.append(Spacer(1, 6))
    elif line.strip():
        story.append(Paragraph(inline(line), P))
flush()
SimpleDocTemplate(str(out), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=14 * mm, bottomMargin=14 * mm,
                  title="Foreman - Round 1 proposal", author="Foreman team").build(story)
size = out.stat().st_size
print("pdf bytes:", size)
assert size <= 1024 * 1024, "PDF over 1 MB"
