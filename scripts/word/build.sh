#!/bin/bash
# Dung ban Word va PDF cua mot bo tai lieu theo the thuc Nghi dinh 30/2020/ND-CP.
# Cach dung: scripts/word/build.sh [TEN-BO]   (mac dinh: SO-TAY-DIEU-TRA-VIEN)
#   vi du:   scripts/word/build.sh TOI-PHAM-DAU-THAU
# Yeu cau: pandoc, python3 + python-docx, libreoffice (soffice), poppler-utils.
set -e
cd "$(dirname "$0")"
export BO="${1:-SO-TAY-DIEU-TRA-VIEN}"
NAME="$(python3 -I ../bo_tai_lieu.py "$BO" ten_tep)"
META="$(python3 -I ../bo_tai_lieu.py "$BO" meta)"
DOCX="$NAME.docx"
PDF="$NAME.pdf"
DEST="$(cd ../.. && pwd)/$BO/ban-in"
echo "Bo tai lieu: $BO -> $DOCX"

topdf() {               # soffice ghi de thang vao thu muc hien tai
  rm -f "$PDF"
  soffice --headless --norestore --convert-to pdf --outdir . "$DOCX" >/dev/null 2>&1
}

[ -f ref-base.docx ] || pandoc --print-default-data-file reference.docx > ref-base.docx

echo "1. Tep mau dinh dang";  python3 -I mk_reference.py
echo "2. Ghep ban thao";      python3 -I assemble.py
echo "3. Chuyen sang Word";   LC_ALL=C.UTF-8 pandoc --from=gfm+raw_attribute --to=docx \
  --reference-doc=reference.docx --toc --toc-depth=2 --metadata-file="$META" \
  -o raw.docx combined.md 2>/dev/null
echo "4. Luot 1: muc luc voi so trang tam"; rm -f pagemap.json; python3 -I postprocess.py
topdf
# Lap den khi so trang trong muc luc khop voi ban PDF (diem bat dong)
for lan in 1 2 3 4; do
  echo "5.$lan Do so trang";  python3 -I map_pages.py
  cp pagemap.json pagemap.prev.json
  echo "6.$lan Dung muc luc co so trang"; python3 -I postprocess.py
  echo "7.$lan Chuan hoa OOXML cho Microsoft Word"; python3 -I fix_ooxml.py "$DOCX"
  topdf
  python3 -I map_pages.py >/dev/null
  if cmp -s pagemap.json pagemap.prev.json; then
    echo "   So trang muc luc da khop ban PDF sau $lan luot"; break
  fi
  echo "   So trang con lech, dung lai"
done
cmp -s pagemap.json pagemap.prev.json || { echo "LOI: muc luc chua on dinh"; exit 1; }
pdfinfo "$PDF" | grep -E "^Pages|^Page size"

mkdir -p "$DEST"
cp -f "$DOCX" "$PDF" "$DEST/"
echo "Da chep ban in vao: $DEST"
