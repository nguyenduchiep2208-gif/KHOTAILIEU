#!/usr/bin/env python3
"""Dung ban HTML tra cuu offline cho mot bo tai lieu trong kho.

Bo tai lieu chon bang bien moi truong BO (mac dinh: SO-TAY-DIEU-TRA-VIEN),
vi du: BO=TOI-PHAM-DAU-THAU python3 scripts/build_html.py
"""
import html as htmlmod
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bo_tai_lieu  # noqa: E402

ROOT = bo_tai_lieu.thu_muc()
OUT = ROOT / "html"
TPL = OUT / "assets" / "template.html"

MAIN = sorted(p.name for p in ROOT.glob("[0-9][0-9]-*.md"))
PL = sorted(p.name for p in (ROOT / "phu-luc").glob("PL-*.md"))

PAGES = [(ROOT / n, OUT / (n[:-3] + ".html"), "") for n in MAIN]
PAGES += [(ROOT / "phu-luc" / n, OUT / "phu-luc" / (n[:-3] + ".html"), "../") for n in PL]

TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
TAGS = {
    "BẮT BUỘC": "tag-must",
    "CẢNH BÁO": "tag-warn",
    "CẦN ĐỐI CHIẾU": "tag-check",
    "VKS": "tag-check",
    "MỚI 2021": "tag-new",
    "MỚI 2025": "tag-new",
    "MỚI 2026": "tag-new",
    "TP.HCM": "tag-hcm",
    "KINH NGHIỆM": "tag-tip",
}


KIND = {"PHẦN": "Phần", "PHỤ LỤC": "Phụ lục", "CHƯƠNG": "Chương"}


def short_title(full: str) -> str:
    """'PHẦN 07. BIỆN PHÁP NGĂN CHẶN' -> 'Phần 07'; 'CHƯƠNG MỞ ĐẦU. ...' -> 'Chương mở đầu'."""
    m = re.match(r"(PHẦN|PHỤ LỤC|CHƯƠNG)\s+([0-9A-Z]+\b|MỞ ĐẦU)", full)
    if m:
        num = "mở đầu" if m.group(2) == "MỞ ĐẦU" else m.group(2)
        return f"{KIND[m.group(1)]} {num}"
    return full[:28]


def build_page(src: Path, dst: Path, prefix: str, prev, nxt) -> str:
    text = src.read_text(encoding="utf-8")
    m = TITLE_RE.search(text)
    full_title = m.group(1) if m else src.stem
    cmd = [
        "pandoc", "--from=gfm", "--to=html5", "--standalone",
        "--toc", "--toc-depth=3", "--section-divs",
        f"--template={TPL}",
        "--metadata", f"title={full_title}",
        "--metadata", f"cssprefix={prefix}",
    ]
    if prev:
        cmd += ["--metadata", f"prevlink={prev[0]}", "--metadata", f"prevtitle={prev[1]}"]
    if nxt:
        cmd += ["--metadata", f"nextlink={nxt[0]}", "--metadata", f"nexttitle={nxt[1]}"]
    cmd += [str(src)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"pandoc loi tren {src}: {res.stderr[:600]}")
    out = res.stdout

    # Lien ket .md -> .html
    out = re.sub(r'(href="[^"]*?)\.md(?=["#])', r"\1.html", out)
    out = out.replace('href="../README.html"', 'href="../index.html"')
    out = out.replace('href="README.html"', 'href="index.html"')

    # Nhan canh bao thanh the co dinh dang
    for label, cls in TAGS.items():
        esc = htmlmod.escape(label)
        out = out.replace(
            f"<strong>[{esc}]</strong>", f'<span class="tag {cls}">{esc}</span>'
        )

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    return full_title


def heading_index(src: Path, href_base: str):
    """Thu muc tra cuu: moi heading h2/h3 -> href + anchor."""
    items = []
    for line in src.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if not m:
            continue
        level = len(m.group(1))
        raw = m.group(2)
        plain = re.sub(r"[*`\[\]]", "", raw).strip()
        slug = pandoc_slug(plain)
        items.append({"t": plain, "h": f"{href_base}#{slug}", "l": level})
    return items


def pandoc_slug(text: str) -> str:
    """Xap xi cach pandoc sinh id cho heading."""
    s = text.lower()
    s = re.sub(r"[^\w\s\-àáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳẵặẹẻẽềềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹý]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"^[\d\-\.]+", "", s)
    return s or "section"


def main():
    titles = []
    for i, (src, dst, prefix) in enumerate(PAGES):
        m = TITLE_RE.search(src.read_text(encoding="utf-8"))
        titles.append(m.group(1) if m else src.stem)

    search = []
    built = []
    for i, (src, dst, prefix) in enumerate(PAGES):
        prev = nxt = None
        if i > 0:
            psrc, pdst, _ = PAGES[i - 1]
            prev = (rel(dst, pdst), short_title(titles[i - 1]))
        if i < len(PAGES) - 1:
            nsrc, ndst, _ = PAGES[i + 1]
            nxt = (rel(dst, ndst), short_title(titles[i + 1]))
        full = build_page(src, dst, prefix, prev, nxt)
        built.append((full, dst.relative_to(OUT).as_posix()))
        base = dst.relative_to(OUT).as_posix()
        search.append({"p": full, "f": base, "s": heading_index(src, base)})
        print(f"  {base}")

    (OUT / "search-index.json").write_text(
        json.dumps(search, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nDa dung {len(built)} trang HTML.")


def rel(from_file: Path, to_file: Path) -> str:
    import os
    return os.path.relpath(to_file, from_file.parent).replace("\\", "/")


if __name__ == "__main__":
    main()
