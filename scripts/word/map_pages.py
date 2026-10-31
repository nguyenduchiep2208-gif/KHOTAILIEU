#!/usr/bin/env python3
"""Doc PDF luot 1, lap bang tieu de -> so trang (doi chieu theo dong)."""
import json, re, subprocess, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bo_tai_lieu  # noqa: E402

PDF = bo_tai_lieu.lay()["ten_tep"] + ".pdf"
n = int(re.search(r"Pages:\s+(\d+)",
        subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout).group(1))

norm = lambda s: re.sub(r"\s+", " ", s).strip()

def candidates(i):
    """Cac dong cua trang i, da ghep doi dong lien tiep, bo dong co dau cham noi."""
    txt = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", PDF, "-"],
                         capture_output=True, text=True).stdout
    lines = [norm(l) for l in txt.split("\n")]
    lines = [l for l in lines if l and "...." not in l]
    out = set(lines)
    for a, b in zip(lines, lines[1:]):
        out.add(norm(a + " " + b))
    return out

print("Đang đọc", n, "trang ...")
PAGES = [candidates(i) for i in range(1, n + 1)]

entries = []
for line in Path("combined.md").read_text(encoding="utf-8").split("\n"):
    m = re.match(r"^(#{1,2})\s+(.+?)\s*$", line)
    if m:
        entries.append((len(m.group(1)), norm(re.sub(r"[*`]", "", m.group(2)))))

def find(text, lo, hi):
    for i in range(lo, hi + 1):
        for c in PAGES[i - 1]:
            if text in c:
                return i
    return None

# Muc luc la day trang lien tuc tu trang 2 co dau cham noi
def has_dots(i):
    txt = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", PDF, "-"],
                         capture_output=True, text=True).stdout
    return "...." in txt

body_start = 2
while body_start <= n and has_dots(body_start):
    body_start += 1
print(f"Mục lục: trang 2..{body_start - 1} | thân bài từ trang {body_start}")

# H1 theo dung thu tu tai lieu, khong lui ve truoc
h1, cursor = {}, body_start
for lvl, t in entries:
    if lvl == 1:
        p = find(t, cursor, n)
        if p:
            h1[t] = p
            cursor = p
tot1 = sum(1 for l, _ in entries if l == 1)
print(f"H1: khớp {len(h1)}/{tot1}")

h1_seq = [(t, h1[t]) for l, t in entries if l == 1 and t in h1]
rng = {t: (p, h1_seq[i + 1][1] - 1 if i + 1 < len(h1_seq) else n)
       for i, (t, p) in enumerate(h1_seq)}

pages, cur, miss = [], None, []
last = body_start
for lvl, t in entries:
    if lvl == 1:
        cur = t
        last = h1.get(t, last)
        pages.append(last)
        continue
    lo, hi = rng.get(cur, (2, n))
    lo = max(lo, last)
    p = find(t, lo, hi)
    if p is None:                       # tieu de dai, xuong nhieu dong: doi chieu phan dau
        p = find(t[:28], lo, hi)
    if p is None:                       # van khong thay: lay trang cua muc lien truoc
        p = last
        miss.append((cur, t))
    pages.append(p)
    last = p

tot2 = sum(1 for l, _ in entries if l == 2)
print(f"H2: khớp {tot2 - len(miss)}/{tot2}")
assert len(pages) == len(entries), (len(pages), len(entries))
assert all(a <= b for a, b in zip(pages, pages[1:])), "số trang không tăng dần"
if miss:
    print(f"  thiếu {len(miss)}:", [f"{c[:18]} > {t[:40]}" for c, t in miss[:6]])

Path("pagemap.json").write_text(json.dumps(pages, ensure_ascii=False), encoding="utf-8")
print(f"pagemap.json: {len(pages)} mục")
