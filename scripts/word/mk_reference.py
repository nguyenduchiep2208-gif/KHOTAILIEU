#!/usr/bin/env python3
"""Tao reference.docx theo the thuc Nghi dinh 30/2020/ND-CP."""
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SERIF, MONO = "Times New Roman", "Courier New"
doc = Document("ref-base.docx")
ST = {s.name: s for s in doc.styles}

for sec in doc.sections:
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin, sec.right_margin = Cm(3.0), Cm(2.0)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    sec.header_distance = sec.footer_distance = Cm(1.25)


def font(st, name=SERIF, size=None, bold=None, italic=None, color=None):
    f = st.font
    f.name = name
    if size is not None: f.size = Pt(size)
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic
    if color is not None: f.color.rgb = RGBColor(*color)
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = rpr.makeelement(qn("w:rFonts"), {}); rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)


def para(st, before=0, after=6, line=1.15, first=None, left=None, align=None, keep=False):
    pf = st.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing, pf.line_spacing_rule = line, WD_LINE_SPACING.MULTIPLE
    if first is not None: pf.first_line_indent = Cm(first)
    if left is not None: pf.left_indent = Cm(left)
    if align is not None: pf.alignment = align
    pf.keep_with_next, pf.widow_control = keep, True


J, C, L = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT

font(ST["Normal"], SERIF, 14)
para(ST["Normal"], 0, 6, 1.15, first=1.0, align=J)
for n in ("Body Text", "First Paragraph"):
    if n in ST:
        font(ST[n], SERIF, 14); para(ST[n], 0, 6, 1.15, first=1.0, align=J)
if "Compact" in ST:
    font(ST["Compact"], SERIF, 14); para(ST["Compact"], 0, 3, 1.15, first=0, align=J)

HEAD = {"Heading 1": (15, 20, 12, C, False), "Heading 2": (14, 14, 8, L, False),
        "Heading 3": (14, 10, 6, L, False), "Heading 4": (14, 8, 6, L, True),
        "Heading 5": (14, 6, 4, L, True), "Heading 6": (14, 6, 4, L, True)}
for n, (sz, bf, af, al, it) in HEAD.items():
    if n in ST:
        font(ST[n], SERIF, sz, bold=True, italic=it, color=(0, 0, 0))
        para(ST[n], bf, af, 1.15, first=0, align=al, keep=True)
        if n == "Heading 1":
            ST[n].paragraph_format.page_break_before = True

if "Title" in ST:
    font(ST["Title"], SERIF, 18, bold=True, color=(0, 0, 0))
    para(ST["Title"], 0, 12, 1.2, first=0, align=C)
if "Subtitle" in ST:
    font(ST["Subtitle"], SERIF, 14, italic=True, color=(0, 0, 0))
    para(ST["Subtitle"], 0, 10, 1.2, first=0, align=C)

for n in ("Caption", "Table Caption", "Image Caption"):
    if n in ST:
        font(ST[n], SERIF, 12, italic=True); para(ST[n], 3, 6, 1.0, first=0, align=C)

if "Block Text" in ST:
    font(ST["Block Text"], SERIF, 14)
    para(ST["Block Text"], 3, 6, 1.15, first=0, left=0.8, align=J)

# Khoi so do ASCII: them style SourceCode cho pandoc
if "Source Code" not in ST:
    sc = doc.styles.add_style("Source Code", WD_STYLE_TYPE.PARAGRAPH)
    sc.element.set(qn("w:styleId"), "SourceCode")
    ST["Source Code"] = sc
font(ST["Source Code"], MONO, 9)
para(ST["Source Code"], 4, 8, 1.0, first=0, left=0, align=L)
ST["Source Code"].paragraph_format.keep_together = False
if "Verbatim Char" in ST:
    font(ST["Verbatim Char"], MONO, 9)

# Bang
if "Table" in ST:
    font(ST["Table"], SERIF, 11)
if "Table Text" not in ST:
    tt = doc.styles.add_style("Table Text", WD_STYLE_TYPE.PARAGRAPH)
    tt.element.set(qn("w:styleId"), "TableText")
    ST["Table Text"] = tt
font(ST["Table Text"], SERIF, 11)
para(ST["Table Text"], 2, 2, 1.0, first=0, left=0, align=L)

for n in ("TOC Heading",):
    if n in ST:
        font(ST[n], SERIF, 15, bold=True, color=(0, 0, 0))
        para(ST[n], 0, 14, 1.15, first=0, align=C)

doc.save("reference.docx")
print("reference.docx: A4 | lề T3 P2 Tr2 D2 cm | Times New Roman 14 | giãn 1,15 | lùi đầu dòng 1cm")
print("                bảng 11pt | sơ đồ Courier New 9pt | tiêu đề in đậm, màu đen")
