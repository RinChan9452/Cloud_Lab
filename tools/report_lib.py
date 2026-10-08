"""Helpers for writing Thai lab-report sections into the unpacked รายงานปฏิบัติการ.docx.

A part script (e.g. build_part1.py) builds a list of XML snippets with these helpers,
then calls splice_part() to replace that Part's body in word/document.xml.
Formatting matches the existing document: Angsana New 15pt, text colour 1f1f1f.
"""
import os, re, struct, shutil
from xml.sax.saxutils import escape

FONT = '<w:rFonts w:ascii="Angsana New" w:cs="Angsana New" w:eastAsia="Angsana New" w:hAnsi="Angsana New"/>'
ARROW_FONT = '<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
IMG_W_EMU = int(6.0 * 914400)   # screenshots are 6 inches wide (page text width is ~6.27")


# ---------- photos ----------
def load_photos(part_dir):
    """Map the leading number of each photo filename ("4.2", "11") to its paths, from all section subfolders."""
    photos = {}
    for d in os.listdir(part_dir):
        full = os.path.join(part_dir, d)
        if os.path.isdir(full):
            for f in os.listdir(full):
                if f.lower().endswith('.png'):
                    key = re.match(r'^([\d.]+)', f).group(1).rstrip('.')
                    photos.setdefault(key, []).append(os.path.join(full, f))
    for k in photos:
        photos[k].sort()
    return photos


def png_size(path):
    with open(path, 'rb') as fh:
        head = fh.read(24)
    return struct.unpack('>II', head[16:24])


# ---------- runs / paragraphs ----------
def rpr(bold=False, size=30, color='1f1f1f', font=FONT):
    b = '<w:b w:val="1"/><w:bCs w:val="1"/>' if bold else ''
    return f'<w:rPr>{font}{b}<w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'


def runs(text, size=30, color='1f1f1f', bold_all=False):
    """Text with **bold** markup. Angsana New has no "→" glyph, so arrows get their own Arial run."""
    out = []
    for i, seg in enumerate(text.split('**')):
        if not seg:
            continue
        bold = bold_all or (i % 2 == 1)
        for j, part in enumerate(seg.split('→')):
            if j:
                out.append(f'<w:r>{rpr(bold, size - 6, color, ARROW_FONT)}<w:t>→</w:t></w:r>')
            if part:
                out.append(f'<w:r>{rpr(bold, size, color)}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return ''.join(out)


def para(inner, ppr_extra='', jc=None, before=60, after=60, keep_next=False, size=30, ind=None):
    kn = '<w:keepNext/>' if keep_next else ''
    sp = f'<w:spacing w:before="{before}" w:after="{after}"/>'
    jcx = f'<w:jc w:val="{jc}"/>' if jc else ''
    ppr = (f'<w:pPr>{kn}{ppr_extra}{sp}{ind or ""}{jcx}'
           f'<w:rPr>{FONT}<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr></w:pPr>')
    return f'<w:p>{ppr}{inner}</w:p>'


def H(text):
    """Section heading, e.g. "1. Create a key pair ..." (keep the English title from the สารบัญ)."""
    return para(runs(text, size=34, bold_all=True), before=360, after=120, keep_next=True, size=34)


def SUB(text):
    """Sub-heading such as วัตถุประสงค์ / ขั้นตอนการทำ."""
    return para(runs(text, size=30, color='1F4E79', bold_all=True), before=180, after=60, keep_next=True)


def P(text):
    return para(runs(text), jc='thaiDistribute')


def STEP(num, text, keep_next=True):
    """'ขั้นตอนที่ 1.1 ...' — kept with the screenshot that follows it."""
    inner = runs(f'**ขั้นตอนที่ {num}** ') + runs(text)
    return para(inner, before=160, after=60, keep_next=keep_next, jc='thaiDistribute')


def BUL(text):
    numpr = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'   # numId 1 = existing bullet list
    return para(runs(text), ppr_extra=numpr, before=0, after=20, ind='<w:ind w:left="1080" w:hanging="360"/>')


def BOX(text):
    """Orange call-out for warnings, gotchas and troubleshooting."""
    extra = ('<w:pBdr><w:left w:val="single" w:sz="24" w:space="8" w:color="E8A33D"/></w:pBdr>'
             '<w:shd w:val="clear" w:color="auto" w:fill="FFF4E0"/>')
    return para(runs(text), ppr_extra=extra, before=120, after=120, jc='thaiDistribute',
                ind='<w:ind w:left="200" w:right="100"/>')


def CODE(text):
    """One code line, or several when given a list (kept in one shaded block, joined with line breaks)."""
    mono = '<w:rFonts w:ascii="Consolas" w:cs="Consolas" w:eastAsia="Consolas" w:hAnsi="Consolas"/>'
    lines = text if isinstance(text, list) else [text]
    brk = f'<w:r>{rpr(False, 22, "1f1f1f", mono)}<w:br/></w:r>'
    r = brk.join(f'<w:r>{rpr(False, 22, "1f1f1f", mono)}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>'
                 for t in lines)
    return para(r, ppr_extra='<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>',
                before=60, after=60, ind='<w:ind w:left="720"/>', size=22)


def PAGEBREAK():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def TABLE(header, rows, widths):
    """widths in twips (dxa); keep the total around 9000 (text width is 9029)."""
    total = sum(widths)
    border = ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="A6A6A6"/>'
                     for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    tblpr = (f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/><w:jc w:val="center"/>'
             f'<w:tblBorders>{border}</w:tblBorders><w:tblLayout w:type="fixed"/>'
             f'<w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'

    def cell(text, w, head):
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="DCE6F2"/>' if head else ''
        p = (f'<w:p><w:pPr><w:spacing w:before="20" w:after="20"/>'
             f'<w:rPr>{FONT}<w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:pPr>{runs(text, size=26, bold_all=head)}</w:p>')
        return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}</w:tcPr>{p}</w:tc>'

    def row(cells, head=False):
        trpr = '<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' if head else '<w:trPr><w:cantSplit/></w:trPr>'
        return '<w:tr>' + trpr + ''.join(cell(c, w, head) for c, w in zip(cells, widths)) + '</w:tr>'

    body = row(header, True) + ''.join(row(r) for r in rows)
    return f'<w:tbl>{tblpr}{grid}{body}</w:tbl>' + para('', before=0, after=60)


# ---------- images ----------
class Images:
    """Copies screenshots into word/media and builds inline picture paragraphs + captions.

    prefix must be unique per Part (e.g. "part1") so ids and file names never collide.
    """

    def __init__(self, unpacked_dir, prefix, docpr_base):
        self.un, self.prefix, self.docpr_base = unpacked_dir, prefix, docpr_base
        self.n = 0
        self.rels = []

    def __call__(self, path, caption):
        self.n += 1
        n = self.n
        rid = f'rId{self.prefix}img{n}'
        target = f'media/{self.prefix}_{n:02d}.png'
        shutil.copyfile(path, os.path.join(self.un, 'word', target))
        self.rels.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                         f'relationships/image" Target="{target}"/>')
        w, h = png_size(path)
        cx, cy = IMG_W_EMU, int(IMG_W_EMU * h / w)
        did = self.docpr_base + n
        descr = escape(caption, {'"': '&quot;'})
        drawing = (
            f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{did}" name="{self.prefix} Picture {n}" descr="{descr}"/>'
            f'<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{did}" name="{self.prefix}_{n:02d}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:ln w="9525"><a:solidFill><a:srgbClr val="A6A6A6"/></a:solidFill></a:ln></pic:spPr>'
            f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')
        img_p = para(drawing, jc='center', before=120, after=0, keep_next=True)
        cap_p = para(runs(caption, size=26, color='595959'), jc='center', before=40, after=160)
        return img_p + cap_p


# ---------- splice ----------
def _ptext(m):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', m.group()))


def splice_part(unpacked_dir, part_no, new_xml, images):
    """Replace everything between the body heading "Part N:" and the body heading "Part N+1:".

    Each "Part N:" heading appears twice: first in the สารบัญ, second in the body.
    The body heading itself is kept. For the last Part, content runs to the end of the body.
    """
    doc_path = os.path.join(unpacked_dir, 'word', 'document.xml')
    doc = open(doc_path, encoding='utf8').read()
    paras = list(re.finditer(r'<w:p[ >].*?</w:p>', doc, re.S))
    this = [i for i, m in enumerate(paras) if _ptext(m).startswith(f'Part {part_no}:')]
    nxt = [i for i, m in enumerate(paras) if _ptext(m).startswith(f'Part {part_no + 1}:')]
    if len(this) < 2:
        raise SystemExit(f'Body heading "Part {part_no}:" not found')
    start = paras[this[1]].end()
    end = paras[nxt[1]].start() if len(nxt) >= 2 else doc.rindex('<w:sectPr')
    doc = doc[:start] + new_xml + doc[end:]
    open(doc_path, 'w', encoding='utf8').write(doc)

    rels_path = os.path.join(unpacked_dir, 'word', '_rels', 'document.xml.rels')
    rels = open(rels_path, encoding='utf8').read()
    rels = re.sub(rf'<Relationship Id="rId{images.prefix}img\d+"[^>]*/>', '', rels)   # drop stale ones on rebuild
    rels = rels.replace('</Relationships>', ''.join(images.rels) + '</Relationships>')
    open(rels_path, 'w', encoding='utf8').write(rels)
    print(f'Part {part_no}: {images.n} images inserted')
