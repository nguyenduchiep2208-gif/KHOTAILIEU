#!/usr/bin/env python3
"""Tao search-index.json va index.html tu cac trang HTML da dung.

Bo tai lieu chon bang bien moi truong BO (mac dinh: SO-TAY-DIEU-TRA-VIEN).
"""
import html as H
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bo_tai_lieu  # noqa: E402

CFG = bo_tai_lieu.lay()["html"]
OUT = bo_tai_lieu.thu_muc() / "html"

MAIN = sorted(p.name for p in OUT.glob("[0-9][0-9]-*.html"))
PL = sorted(p.name for p in (OUT / "phu-luc").glob("PL-*.html"))
FILES = MAIN + [f"phu-luc/{n}" for n in PL]

SEC = re.compile(
    r'<section id="([^"]+)" class="level([1-3])">\s*<h([1-3])[^>]*>(.*?)</h\3>',
    re.S,
)
TAGSTRIP = re.compile(r"<[^>]+>")


def clean(s: str) -> str:
    s = TAGSTRIP.sub("", s)
    s = H.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


KIND = {"PHẦN": "Phần", "PHỤ LỤC": "Phụ lục", "CHƯƠNG": "Chương"}


def short(full: str) -> str:
    m = re.match(r"(PHẦN|PHỤ LỤC|CHƯƠNG)\s+([0-9A-Z]+\b|MỞ ĐẦU)\.?\s*(.*)", full)
    if m:
        num = "mở đầu" if m.group(2) == "MỞ ĐẦU" else m.group(2)
        return f"{KIND[m.group(1)]} {num}", m.group(3).strip()
    return full, ""


pages = []
for f in FILES:
    src = (OUT / f).read_text(encoding="utf-8")
    body = src.split('<main>', 1)[1] if '<main>' in src else src
    secs = SEC.findall(body)
    title = ""
    items = []
    for sid, lvl, h, raw in secs:
        txt = clean(raw)
        if h == "1" and not title:
            title = txt
            continue
        if h in ("2", "3"):
            items.append({"t": txt, "a": sid, "l": int(h)})
    if not title:
        m = re.search(r"<title>(.*?)</title>", src, re.S)
        title = clean(m.group(1)) if m else f
    label, rest = short(title)
    pages.append({"f": f, "title": title, "label": label, "name": rest, "s": items})

(OUT / "search-index.json").write_text(
    json.dumps(pages, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
)

# Doi chieu
tot = sum(len(p["s"]) for p in pages)
ok = 0
for p in pages:
    src = (OUT / p["f"]).read_text(encoding="utf-8")
    ids = set(re.findall(r'<section id="([^"]+)"', src))
    ok += sum(1 for s in p["s"] if s["a"] in ids)
print(f"Khop {ok}/{tot} lien ket muc")

# ---------- index.html ----------
GROUPS = CFG["groups"]
QUICK = CFG["quick"]

by_key = {}
for p in pages:
    key = "PL" if p["f"].startswith("phu-luc/") else p["f"][:2]
    by_key.setdefault(key, []).append(p)

cards = []
for gname, keys in GROUPS:
    rows = []
    for k in keys:
        for p in by_key.get(k, []):
            n = len(p["s"])
            rows.append(
                f'<li><a href="{p["f"]}"><span class="pl">{H.escape(p["label"])}</span>'
                f'<span class="pn">{H.escape(p["name"] or p["title"])}</span>'
                f'<span class="pc">{n} mục</span></a></li>'
            )
    cards.append(
        f'<section class="grp"><h2>{H.escape(gname)}</h2><ul class="plist">'
        + "".join(rows)
        + "</ul></section>"
    )

quick_html = "".join(
    f'<li><a href="{href}">{H.escape(t)}</a></li>' for t, href in QUICK
)

n_sec = tot
n_pages = len(pages)
badges_html = "\n".join(
    f"    <span>{b.format(n_sec=n_sec, n_pages=n_pages)}</span>" for b in CFG["badges"]
)

doc = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{CFG["title"]}</title>
<meta name="description" content="{CFG["description"].format(n_pages=n_pages, n_sec=n_sec)}">
<link rel="stylesheet" href="assets/style.css">
<style>
body{{font-size:17px}}
.home{{max-width:1080px;margin:0 auto;padding:32px 24px 100px}}
.hd{{border-bottom:3px solid var(--accent);padding-bottom:18px;margin-bottom:8px}}
.hd h1{{margin:0 0 6px;font-size:2.1em}}
.hd p.sub{{margin:0;color:var(--ink-soft);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px}}
.meta{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 26px;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:12.5px}}
.meta span{{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:4px 12px;color:var(--ink-soft)}}
.warnbox{{background:var(--must-bg);border:1px solid var(--must-line);border-left-width:5px;border-radius:0 8px 8px 0;padding:14px 18px;margin:0 0 28px;font-size:15.5px}}
.warnbox b{{color:var(--must-line)}}
.searchbox{{position:relative;margin:0 0 30px}}
#q{{width:100%;font:inherit;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:16px;padding:14px 16px;border:2px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink)}}
#q:focus{{outline:none;border-color:var(--accent)}}
#res{{margin-top:10px;background:var(--panel);border:1px solid var(--line);border-radius:10px;max-height:460px;overflow-y:auto;display:none}}
#res.on{{display:block}}
#res a{{display:block;padding:10px 16px;border-bottom:1px solid var(--line-soft);text-decoration:none;color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px}}
#res a:last-child{{border-bottom:0}}
#res a:hover,#res a.sel{{background:var(--accent-soft)}}
#res .rp{{display:block;font-size:11.5px;color:var(--accent);font-weight:700;letter-spacing:.03em}}
#res .rn{{color:var(--ink-soft);font-size:12px;padding:10px 16px;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
.cols{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:36px;align-items:start}}
.grp{{margin:0 0 26px}}
.grp h2{{font-size:1.05em;margin:0 0 10px;padding-bottom:7px;border-bottom:2px solid var(--line);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.01em}}
ul.plist{{list-style:none;margin:0;padding:0}}
ul.plist li{{margin:0 0 5px}}
ul.plist a{{display:grid;grid-template-columns:86px minmax(0,1fr) auto;gap:10px;align-items:baseline;text-decoration:none;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:9px 13px;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px}}
ul.plist a:hover{{border-color:var(--accent);background:var(--accent-soft)}}
.pl{{font-weight:700;color:var(--accent);font-size:12.5px;letter-spacing:.02em}}
.pn{{line-height:1.35}}
.pc{{font-size:11.5px;color:var(--ink-soft);white-space:nowrap}}
.side{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px 20px;position:sticky;top:20px}}
.side h2{{font-size:1.02em;margin:0 0 12px;font-family:system-ui,-apple-system,"Segoe UI",sans-serif}}
ul.quick{{list-style:none;margin:0;padding:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:13.5px}}
ul.quick li{{margin:0;border-bottom:1px solid var(--line-soft)}}
ul.quick li:last-child{{border-bottom:0}}
ul.quick a{{display:block;padding:8px 2px;text-decoration:none;color:var(--ink-soft);line-height:1.4}}
ul.quick a:hover{{color:var(--accent)}}
.ft{{margin-top:36px;padding-top:18px;border-top:1px solid var(--line);color:var(--ink-soft);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:12.5px}}
.tools{{display:flex;gap:12px;align-items:center;margin-top:14px}}
@media (max-width:900px){{
  .cols{{grid-template-columns:minmax(0,1fr);gap:24px}}
  .side{{position:static}}
  .home{{padding:22px 16px 80px}}
  ul.plist a{{grid-template-columns:76px minmax(0,1fr);row-gap:2px}}
  .pc{{grid-column:1 / -1}}
}}
</style>
</head>
<body>
<div class="home">
  <div class="hd">
    <h1>{CFG["h1"]}</h1>
    <p class="sub">{CFG["sub"]}</p>
  </div>
  <div class="meta">
{badges_html}
  </div>
  <div class="warnbox">
{CFG["warn"]}
  </div>

  <div class="searchbox">
    <input id="q" type="search" autocomplete="off" placeholder="{CFG["placeholder"]}">
    <div id="res" role="listbox"></div>
  </div>

  <div class="cols">
    <div>{"".join(cards)}</div>
    <aside class="side">
      <h2>Tra cứu nhanh theo tình huống</h2>
      <ul class="quick">{quick_html}</ul>
      <div class="tools">
        <button class="theme" id="themeBtn" type="button">Sáng / tối</button>
      </div>
    </aside>
  </div>

  <div class="ft">
{CFG["footer"]}
  </div>
</div>
<script src="assets/app.js"></script>
<script>
var IDX = {json.dumps(pages, ensure_ascii=False, separators=(",", ":"))};
(function(){{
  var q = document.getElementById('q'), res = document.getElementById('res');
  var flat = [];
  for (var i=0;i<IDX.length;i++) {{
    var p = IDX[i];
    flat.push({{t:p.title, h:p.f, p:p.label, k:norm(p.title+' '+p.label)}});
    for (var j=0;j<p.s.length;j++) {{
      var s = p.s[j];
      flat.push({{t:s.t, h:p.f+'#'+s.a, p:p.label, k:norm(s.t)}});
    }}
  }}
  function norm(s){{
    return s.toLowerCase()
      .normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')
      .replace(/đ/g,'d').replace(/[^a-z0-9\\s]/g,' ')
      .replace(/\\s+/g,' ').trim();
  }}
  var sel = -1, cur = [];
  function render(list){{
    cur = list; sel = -1;
    if (!list.length) {{ res.innerHTML = '<div class="rn">Không tìm thấy mục nào khớp.</div>'; res.className='on'; return; }}
    var h = '';
    for (var i=0;i<list.length;i++) {{
      h += '<a href="'+list[i].h+'"><span class="rp">'+list[i].p+'</span>'+esc(list[i].t)+'</a>';
    }}
    res.innerHTML = h; res.className = 'on';
  }}
  function esc(s){{ var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }}
  q.addEventListener('input', function(){{
    var v = norm(q.value);
    if (v.length < 2) {{ res.className=''; res.innerHTML=''; return; }}
    var words = v.split(' ');
    var hits = [];
    for (var i=0;i<flat.length;i++) {{
      var k = flat[i].k, all = true, score = 0;
      for (var w=0;w<words.length;w++) {{
        var at = k.indexOf(words[w]);
        if (at < 0) {{ all = false; break; }}
        score += at === 0 ? 0 : 1;
      }}
      if (all) {{ hits.push([score, k.length, flat[i]]); }}
    }}
    hits.sort(function(a,b){{ return a[0]-b[0] || a[1]-b[1]; }});
    render(hits.slice(0,40).map(function(x){{ return x[2]; }}));
  }});
  q.addEventListener('keydown', function(e){{
    var items = res.querySelectorAll('a');
    if (!items.length) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {{
      e.preventDefault();
      if (sel >= 0) items[sel].className = '';
      sel = e.key === 'ArrowDown' ? Math.min(sel+1, items.length-1) : Math.max(sel-1, 0);
      items[sel].className = 'sel'; items[sel].scrollIntoView({{block:'nearest'}});
    }} else if (e.key === 'Enter' && sel >= 0) {{
      e.preventDefault(); window.location.href = items[sel].getAttribute('href');
    }} else if (e.key === 'Escape') {{
      res.className=''; q.blur();
    }}
  }});
  document.addEventListener('click', function(e){{
    if (!res.contains(e.target) && e.target !== q) res.className='';
  }});
}})();
</script>
</body>
</html>
"""

(OUT / "index.html").write_text(doc, encoding="utf-8")
print(f"index.html: {len(doc)} bytes, {n_pages} trang, {n_sec} muc")
