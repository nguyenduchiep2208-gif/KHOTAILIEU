#!/usr/bin/env python3
"""Chuan hoa thu tu phan tu OOXML cho dung lich ECMA-376.

pandoc va python-docx deu sinh ra mot so phan tu dat sai thu tu trong pPr,
rPr, tcPr, tblPr, trPr va w:style. LibreOffice bo qua, nhung Microsoft Word
kiem tra chat hon. Script nay sap xep lai con cua cac phan tu do, bo sung
thuoc tinh w:gutter con thieu va dem w:nsid cho du 8 ky tu hex.
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

# Thu tu con theo luoc do ECMA-376 (CT_PPr, CT_RPr, CT_TcPr, ...).
ORDER = {
    "pPr": """pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr
        suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap
        overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd
        snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc
        textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr
        sectPr pPrChange""",
    "rPr": """ins del moveFrom moveTo rStyle rFonts b bCs i iCs caps smallCaps strike
        dstrike outline shadow emboss imprint noProof snapToGrid vanish webHidden
        color spacing w kern position sz szCs highlight u effect bdr shd fitText
        vertAlign rtl cs em lang eastAsianLayout specVanish oMath rPrChange""",
    "tcPr": """cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar
        textDirection tcFitText vAlign hideMark headers cellIns cellDel cellMerge
        tcPrChange""",
    "trPr": """cnfStyle divId gridBefore gridAfter wBefore wAfter cantSplit trHeight
        tblHeader tblCellSpacing jc hidden ins del trPrChange""",
    "tblPr": """tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize
        tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd tblLayout
        tblCellMar tblLook tblCaption tblDescription tblPrChange""",
    "style": """name aliases basedOn next link autoRedefine hidden uiPriority
        semiHidden unhideWhenUsed qFormat locked personal personalCompose
        personalReply rsid pPr rPr tblPr trPr tcPr tblStylePr""",
    "sectPr": """footnotePr endnotePr type pgSz pgMar paperSrc pgBorders lnNumType
        pgNumType cols formProt vAlign noEndnote titlePg textDirection bidi
        rtlGutter docGrid printerSettings sectPrChange""",
    "settings": """writeProtection view zoom removePersonalInformation
        removeDateAndTime doNotDisplayPageBoundaries displayBackgroundShape
        printPostScriptOverText printFractionalCharacterWidth printFormsData
        embedTrueTypeFonts embedSystemFonts saveSubsetFonts saveFormsData
        mirrorMargins alignBordersAndEdges bordersDoNotSurroundHeader
        bordersDoNotSurroundFooter gutterAtTop hideSpellingErrors
        hideGrammaticalErrors activeWritingStyle proofState formsDesign
        attachedTemplate linkStyles stylePaneFormatFilter stylePaneSortMethod
        documentType mailMerge revisionView trackChanges doNotTrackMoves
        doNotTrackFormatting documentProtection autoFormatOverride styleLockTheme
        styleLockQFSet defaultTabStop autoHyphenation consecutiveHyphenLimit
        hyphenationZone doNotHyphenateCaps showEnvelope summaryLength
        clickAndTypeStyle defaultTableStyle evenAndOddHeaders bookFoldRevPrinting
        bookFoldPrinting bookFoldPrintingSheets drawingGridHorizontalOrigin
        drawingGridVerticalOrigin drawingGridHorizontalSpacing
        drawingGridVerticalSpacing displayHorizontalDrawingGridEvery
        displayVerticalDrawingGridEvery doNotUseMarginsForDrawingGridOrigin
        doNotShadeFormData noPunctuationKerning characterSpacingControl
        printTwoOnOne strictFirstAndLastChars noLineBreaksAfter noLineBreaksBefore
        savePreviewPicture doNotValidateAgainstSchema saveInvalidXml
        ignoreMixedContent alwaysShowPlaceholderText doNotDemarcateInvalidXml
        saveXmlDataOnly useXSLTWhenSaving saveThroughXslt showXMLTags
        alwaysMergeEmptyNamespace updateFields hdrShapeDefaults footnotePr
        endnotePr compat docVars rsids mathPr uiCompat97To2003 attachedSchema
        themeFontLang clrSchemeMapping doNotIncludeSubdocsInStats
        doNotAutoCompressPictures forceUpgrade captions readModeInkLockDown
        smartTagType schemaLibrary shapeDefaults doNotEmbedSmartTags decimalSymbol
        listSeparator""",
}
ORDER = {k: v.split() for k, v in ORDER.items()}
PARTS = ("word/document.xml", "word/styles.xml", "word/numbering.xml",
         "word/settings.xml",
         "word/header1.xml", "word/header2.xml", "word/header3.xml",
         "word/footer1.xml", "word/footer2.xml", "word/footer3.xml")


def reorder(root):
    """Sap xep lai con cua moi phan tu co trong bang ORDER. Tra ve so lan sua."""
    n = 0
    for tag, seq in ORDER.items():
        rank = {W + name: i for i, name in enumerate(seq)}
        if tag == "settings":  # m:mathPr nam dung cho cua w:mathPr trong luoc do
            rank[M + "mathPr"] = rank[W + "mathPr"]
        for el in root.iter(W + tag):
            kids = list(el)
            # sectPr co the mang nhieu headerReference/footerReference o dau:
            # giu nguyen vi tri tuong doi cua chung.
            if tag == "sectPr":
                head = [k for k in kids if k.tag in
                        (W + "headerReference", W + "footerReference")]
                rest = [k for k in kids if k not in head]
            else:
                head, rest = [], kids
            if tag == "settings":
                # w:settings con mang ca m:mathPr (khong gian ten khac):
                # phan tu la duoc day ve cuoi, giu nguyen thu tu tuong doi.
                def key(k, _n=len(seq)):
                    return rank.get(k.tag, _n + kids.index(k))
            elif any(k.tag not in rank for k in rest):
                continue  # co phan tu la: khong dung den cho an toan
            else:
                def key(k):
                    return rank[k.tag]
            ordered = head + sorted(rest, key=key)
            if ordered != kids:
                for k in ordered:
                    el.append(k)
                n += 1
    return n


def strip_text(root):
    """Xoa van ban lac trong cac phan tu chi chua phan tu con."""
    n = 0
    for tag in ORDER:
        for el in root.iter(W + tag):
            if (el.text or "").strip():
                n += 1
            el.text = None
            for k in el:
                if (k.tail or "").strip():
                    n += 1
                k.tail = None
    return n


def patch(root):
    """Bo sung w:gutter va dem w:nsid cho du 8 ky tu hex."""
    n = 0
    for el in root.iter(W + "pgMar"):
        if el.get(W + "gutter") is None:
            el.set(W + "gutter", "0")
            n += 1
    for el in root.iter(W + "nsid"):
        v = el.get(W + "val") or ""
        if re.fullmatch(r"[0-9A-Fa-f]{1,8}", v) and len(v) != 8:
            el.set(W + "val", v.rjust(8, "0"))
            n += 1
    return n


def main(path):
    src = Path(path)
    tmp = src.with_suffix(".fixed.docx")
    fixed = 0
    with zipfile.ZipFile(src) as zin, \
            zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in PARTS:
                root = etree.fromstring(data)
                fixed += reorder(root) + patch(root) + strip_text(root)
                data = etree.tostring(root, xml_declaration=True,
                                      encoding="UTF-8", standalone=True)
            zout.writestr(item, data)
    shutil.move(tmp, src)
    print(f"{src.name}: chuan hoa {fixed} phan tu OOXML")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "SO TAY DIEU TRA VIEN.docx")
