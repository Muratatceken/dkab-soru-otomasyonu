"""
Windows PowerShell pipeline'daki build_sb_docx2.ps1 / build_u2_docx.ps1'in Python portu.

Word/DOCX dosyasini python-docx gibi bir kutuphane olmadan, doğrudan OOXML XML
parçalarını elle üretip bir zip (docx) paketi olarak yazar. Orijinal PowerShell
scriptiyle birebir aynı stil tanımlarını (Arial 10pt, Band/H1a/H2a/Kbox/Cevap/...)
kullanır, böylece üretilen belgeler görsel olarak öncekilerle tutarlı kalır.
"""
from __future__ import annotations

import zipfile
from dataclasses import dataclass, field

ARIAL_RPR = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>'

STYLES_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    f'<w:docDefaults><w:rPrDefault><w:rPr>{ARIAL_RPR}<w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:rPrDefault></w:docDefaults>'
    f'<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="80" w:line="252" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr><w:rPr>{ARIAL_RPR}<w:sz w:val="20"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="16305A"/><w:sz w:val="30"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="21426E"/><w:sz w:val="24"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Band"><w:name w:val="Band"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="120"/><w:jc w:val="center"/><w:shd w:val="clear" w:fill="21426E"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="FFFFFF"/><w:sz w:val="24"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="H1a"><w:name w:val="H1a"/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="80"/><w:pBdr><w:bottom w:val="single" w:sz="8" w:space="2" w:color="21426E"/></w:pBdr></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="16305A"/><w:sz w:val="24"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="H2a"><w:name w:val="H2a"/><w:pPr><w:keepNext/><w:spacing w:before="140" w:after="60"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="0F7B78"/><w:sz w:val="22"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Kapsam"><w:name w:val="Kapsam"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="100"/><w:jc w:val="left"/></w:pPr><w:rPr>{ARIAL_RPR}<w:i/><w:color w:val="59637A"/><w:sz w:val="18"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Kazanim"><w:name w:val="Kazanim"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="120" w:after="20"/><w:jc w:val="left"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="0F7B78"/><w:sz w:val="16"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Soru"><w:name w:val="Soru"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Kok"><w:name w:val="Kok"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="60" w:after="60"/><w:jc w:val="left"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Secenek"><w:name w:val="Secenek"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="10"/><w:ind w:left="284" w:hanging="284"/><w:jc w:val="left"/></w:pPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Cevap"><w:name w:val="Cevap"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="140"/><w:jc w:val="left"/></w:pPr><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="9A6B13"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Cozum"><w:name w:val="Cozum"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="140"/><w:ind w:left="170"/><w:jc w:val="left"/><w:shd w:val="clear" w:fill="EAF6F4"/><w:pBdr><w:left w:val="single" w:sz="18" w:space="4" w:color="0F7B78"/></w:pBdr></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Item"><w:name w:val="Item"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="40"/><w:jc w:val="left"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Kbox"><w:name w:val="Kbox"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="60" w:after="100"/><w:jc w:val="left"/><w:shd w:val="clear" w:fill="FBF5E9"/><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="E0C892"/><w:left w:val="single" w:sz="4" w:space="4" w:color="E0C892"/><w:bottom w:val="single" w:sz="4" w:space="4" w:color="E0C892"/><w:right w:val="single" w:sz="4" w:space="4" w:color="E0C892"/></w:pBdr></w:pPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Ayet"><w:name w:val="Ayet"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="40" w:after="20"/><w:ind w:left="284" w:right="284"/></w:pPr><w:rPr>{ARIAL_RPR}<w:i/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="AyetC"><w:name w:val="AyetC"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="80"/><w:jc w:val="right"/></w:pPr><w:rPr>{ARIAL_RPR}<w:color w:val="59637A"/><w:sz w:val="16"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Note"><w:name w:val="Note"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="80"/><w:jc w:val="left"/></w:pPr><w:rPr>{ARIAL_RPR}<w:i/><w:color w:val="59637A"/><w:sz w:val="18"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="Cell"><w:name w:val="Cell"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="20"/><w:jc w:val="left"/></w:pPr><w:rPr>{ARIAL_RPR}<w:sz w:val="18"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="CellH"><w:name w:val="CellH"/><w:basedOn w:val="Cell"/><w:rPr>{ARIAL_RPR}<w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="CellBad"><w:name w:val="CellBad"/><w:basedOn w:val="Cell"/><w:rPr>{ARIAL_RPR}<w:color w:val="B0405E"/><w:sz w:val="18"/></w:rPr></w:style>'
    f'<w:style w:type="paragraph" w:styleId="CellGood"><w:name w:val="CellGood"/><w:basedOn w:val="Cell"/><w:rPr>{ARIAL_RPR}<w:color w:val="1F7A4D"/><w:sz w:val="18"/></w:rPr></w:style>'
    '</w:styles>'
)

LETTERS = ["A", "B", "C", "D", "E"]

STEM_MARKERS = [
    "Bu parça", "Bu ayet", "Bu ayetler", "Aşağıdaki ayet", "Aşağıdakilerden",
    "Buna göre", "Bu söz", "Bu öğüt", "Bu bilgiler",
]


def esc(s: str | None) -> str:
    if s is None:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def split_stem(stem: str) -> tuple[str, str]:
    """Soru paragrafi ile kisa soru kokunu ayirir (paragraf + ayri kalin kok)."""
    best = -1
    for marker in STEM_MARKERS:
        ix = stem.rfind(marker)
        if ix > best:
            best = ix
    if best >= 1 and stem.rstrip().endswith("?"):
        return stem[:best].strip(), stem[best:].strip()
    return stem, ""


@dataclass
class MediaItem:
    name: str
    data: bytes
    rid: str


@dataclass
class DocxBuilder:
    body: list[str] = field(default_factory=list)
    media: list[MediaItem] = field(default_factory=list)
    _rid_counter: int = 2

    # ---- low level paragraph helpers ----
    def raw(self, xml: str) -> None:
        self.body.append(xml)

    def paragraph(self, text: str, style: str | None = None) -> None:
        style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        self.body.append(
            f'<w:p>{style_xml}<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
        )

    def bold_paragraph(self, bold_text: str, rest_text: str, style: str | None = None) -> None:
        style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
        self.body.append(
            f'<w:p>{style_xml}'
            f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{esc(bold_text)}</w:t></w:r>'
            f'<w:r><w:t xml:space="preserve">{esc(rest_text)}</w:t></w:r></w:p>'
        )

    def heading(self, text: str, style: str) -> None:
        self.body.append(
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
        )

    def page_break_heading(self, text: str, style: str) -> None:
        self.body.append(
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/><w:pageBreakBefore/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'
        )

    # ---- images ----
    def image_paragraph(self, png_bytes: bytes, width_emu: int = 5486400, height_emu: int | None = None,
                         aspect_h_over_w: float | None = None) -> None:
        n = len(self.media) + 1
        rid = f"rId{self._rid_counter}"
        self._rid_counter += 1
        cx = width_emu
        if height_emu is not None:
            cy = height_emu
        elif aspect_h_over_w is not None:
            cy = int(round(cx * aspect_h_over_w))
        else:
            cy = cx
        name = f"image{n}.png"
        self.media.append(MediaItem(name=name, data=png_bytes, rid=rid))
        self.body.append(
            '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="140"/></w:pPr>'
            '<w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{n}" name="Gorsel{n}"/>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:nvPicPr><pic:cNvPr id="{n}" name="Gorsel{n}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"
        )

    # ---- tables ----
    def table(self, rows: list[list[str]], col_widths: list[int] | None = None) -> None:
        widths = col_widths or [2400, 3300, 3300][: len(rows[0])]
        grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        borders = (
            '<w:tblBorders>'
            '<w:top w:val="single" w:sz="4" w:color="9AA6BF"/>'
            '<w:left w:val="single" w:sz="4" w:color="9AA6BF"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="9AA6BF"/>'
            '<w:right w:val="single" w:sz="4" w:color="9AA6BF"/>'
            '<w:insideH w:val="single" w:sz="4" w:color="C7CEDD"/>'
            '<w:insideV w:val="single" w:sz="4" w:color="C7CEDD"/>'
            '</w:tblBorders>'
        )
        tr_xml = []
        for i, row in enumerate(rows):
            head = i == 0
            tcs = []
            for j, cell in enumerate(row):
                shade = '<w:shd w:val="clear" w:fill="21426E"/>' if head else ""
                style = "CellH" if head else ("CellBad" if j == 1 else "CellGood" if j == 2 else "Cell")
                tcs.append(
                    f'<w:tc><w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{shade}</w:tcPr>'
                    f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
                    f'<w:r><w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p></w:tc>'
                )
            tr_xml.append(f"<w:tr>{''.join(tcs)}</w:tr>")
        self.body.append(
            f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>{borders}'
            f'<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>'
            f"{''.join(tr_xml)}</w:tbl><w:p/>"
        )

    # ---- composite: question block (KAZANIM + kok/paragraf ayrimi + secenekler + cevap) ----
    def question_block(self, number: str, kazanim_line: str, stem: str, secenekler: list[str],
                        dogru: str, kok_override: str = "", cozum: str = "") -> None:
        body_t, kok_t = (stem, kok_override) if kok_override else split_stem(stem)
        if kazanim_line:
            self.paragraph(kazanim_line, "Kazanim")
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="Soru"/></w:pPr>'
            f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{number}. </w:t></w:r>'
            f'<w:r><w:t xml:space="preserve">{esc(body_t)}</w:t></w:r></w:p>'
        )
        if kok_t:
            self.heading(kok_t, "Kok")
        for i, secenek in enumerate(secenekler):
            self.paragraph(f"{LETTERS[i]}) {secenek}", "Secenek")
        self.paragraph(f"CEVAP: {dogru}", "Cevap")
        if cozum:
            self.bold_paragraph("Çözüm: ", cozum, "Cozum")

    # ---- packaging ----
    def save(self, path: str, page_size_w: int = 11906, page_size_h: int = 16838, margin: int = 1134) -> None:
        sect = (
            f'<w:sectPr><w:pgSz w:w="{page_size_w}" w:h="{page_size_h}"/>'
            f'<w:pgMar w:top="{margin}" w:right="{margin}" w:bottom="{margin}" w:left="{margin}"/></w:sectPr>'
        )
        doc = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
            f"<w:body>{''.join(self.body)}{sect}</w:body></w:document>"
        )
        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '</Types>'
        )
        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>'
        )
        doc_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        )
        for m in self.media:
            doc_rels += (
                f'<Relationship Id="{m.rid}" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                f'Target="media/{m.name}"/>'
            )
        doc_rels += "</Relationships>"

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", root_rels)
            zf.writestr("word/document.xml", doc)
            zf.writestr("word/styles.xml", STYLES_XML)
            zf.writestr("word/_rels/document.xml.rels", doc_rels)
            for m in self.media:
                zf.writestr(f"word/media/{m.name}", m.data)
