#!/usr/bin/env python3
"""Ghep cac tep Markdown cua mot bo tai lieu thanh mot ban thao cho Word.

Bo tai lieu chon bang bien moi truong BO (mac dinh: SO-TAY-DIEU-TRA-VIEN).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent))
import bo_tai_lieu  # noqa: E402

CFG = bo_tai_lieu.lay()
SRC = bo_tai_lieu.thu_muc()
OUT = HERE / "combined.md"

PAGEBREAK = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

LINK = re.compile(r"\[([^\]]+)\]\((?!https?://)[^)]*\)")
LINK_ANY = re.compile(r"\[([^\]]+)\]\([^)]*\)")
NAV = re.compile(r"^\s*\[[^\]]+\]\([^)]*\)(\s*\|\s*\[[^\]]+\]\([^)]*\))*\s*$")


def strip_nav(text: str) -> str:
    out, prev_blank = [], True
    for line in text.split("\n"):
        if NAV.match(line):
            continue
        out.append(line)
    s = "\n".join(out)
    # bo cac duong ke ngang lien tiep va khoang trang thua o cuoi
    s = re.sub(r"\n-{3,}\s*\n\s*-{3,}\s*\n", "\n---\n", s)
    s = re.sub(r"\n-{3,}\s*$", "", s.rstrip()) + "\n"
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s


def flatten_links(text: str) -> str:
    return LINK_ANY.sub(r"\1", text)


def load(p: Path) -> str:
    return flatten_links(strip_nav(p.read_text(encoding="utf-8")))


# ---- Phan mo dau lay tu README cua So tay ----
# Muc "III. MUC LUC" cua README bi bo vi ban in da co muc luc rieng co so trang;
# cac muc con lai duoc danh so lai lien tuc.
readme = (SRC / "README.md").read_text(encoding="utf-8")
WANT = (("## I. LỜI NÓI ĐẦU", "I. LỜI NÓI ĐẦU"),
        ("## II. CẢNH BÁO SỬ DỤNG", "II. CẢNH BÁO SỬ DỤNG"),
        ("## V. QUY ƯỚC TRÌNH BÀY", "III. QUY ƯỚC TRÌNH BÀY VÀ TỪ VIẾT TẮT"),
        ("## IV. TRA CỨU NHANH THEO TÌNH HUỐNG", "IV. TRA CỨU NHANH THEO TÌNH HUỐNG"),
        ("## VI. CẤU TRÚC ĐỌC KHUYẾN NGHỊ", "V. CẤU TRÚC ĐỌC KHUYẾN NGHỊ"))
intro_parts = []
for head, title in WANT:
    i = readme.index(head)
    j = readme.find("\n## ", i + 5)
    chunk = readme[i:j if j != -1 else len(readme)].strip()
    chunk = chunk.split("\n---\n")[0].rstrip()   # bo duong ke cuoi muc
    intro_parts.append("## " + title + chunk[len(head):])
intro = "# LỜI NÓI ĐẦU, QUY ƯỚC VÀ TRA CỨU NHANH\n\n" + "\n\n".join(intro_parts)
intro = flatten_links(strip_nav(intro))

files = sorted(SRC.glob("[0-9][0-9]-*.md")) + sorted((SRC / "phu-luc").glob("PL-*.md"))

# Trang ngan cach giua cac phan lon (neu bo tai lieu co cau hinh)
NGAN_CACH = {pre: (title, note) for pre, title, note in CFG.get("ngan_cach", [])}

chunks = [intro]
for f in files:
    sep = NGAN_CACH.get(f.name[:2]) if f.parent == SRC else None
    if sep:
        chunks.append(f"# {sep[0]}\n\n{sep[1]}\n")
    chunks.append(load(f))

body = ("\n\n" + PAGEBREAK + "\n\n").join(chunks)

OUT.write_text(body, encoding="utf-8")

n_h1 = len(re.findall(r"^# ", body, re.M))
n_h2 = len(re.findall(r"^## ", body, re.M))
n_h3 = len(re.findall(r"^### ", body, re.M))
print(f"combined.md: {len(body.split()):,} từ".replace(",", "."))
print(f"  {n_h1} phần (H1), {n_h2} mục (H2), {n_h3} tiểu mục (H3)")
print(f"  còn liên kết markdown: {len(LINK_ANY.findall(body))}")
