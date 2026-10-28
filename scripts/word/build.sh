#!/bin/bash
# Dung ban Word va PDF cua So tay Dieu tra vien theo the thuc Nghi dinh 30/2020/ND-CP.
# Yeu cau: pandoc, python3 + python-docx, libreoffice (soffice), poppler-utils.
set -e
cd "$(dirname "$0")"
DOCX="SO TAY DIEU TRA VIEN.docx"
PDF="SO TAY DIEU TRA VIEN.pdf"
DEST="$(cd ../.. && pwd)/SO-TAY-DIEU-TRA-VIEN/ban-in"

topdf() {               # soffice ghi de thang vao thu muc hien tai
  rm -f "$PDF"
  soffice --headless --norestore --convert-to pdf --outdir . "$DOCX" >/dev/null 2>&1
}

[ -f ref-base.docx ] || pandoc --print-default-data-file reference.docx > ref-base.docx

echo "1. Tep mau dinh dang";  python3 -I mk_reference.py
echo "2. Ghep ban thao";      python3 -I assemble.py
echo "3. Chuyen sang Word";   LC_ALL=C.UTF-8 pandoc --from=gfm+raw_attribute --to=docx \
  --reference-doc=reference.docx --toc --toc-depth=2 --metadata-file=meta.yaml \
  -o raw.docx combined.md 2>/dev/null
echo "4. Luot 1: muc luc chua co so trang"; rm -f pagemap.json; python3 -I postprocess.py
topdf
echo "5. Do so trang";        python3 -I map_pages.py
echo "6. Luot 2: muc luc day du"; python3 -I postprocess.py
echo "7. Chuan hoa OOXML cho Microsoft Word"; python3 -I fix_ooxml.py "$DOCX"
topdf
pdfinfo "$PDF" | grep -E "^Pages|^Page size"

mkdir -p "$DEST"
cp -f "$DOCX" "$PDF" "$DEST/"
echo "Da chep ban in vao: $DEST"
