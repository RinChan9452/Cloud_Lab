"""Rebuild the สารบัญ (with page numbers) and the page-number header, then pack the docx.

Usage: python update_toc.py <unpacked_docx_dir> <out.docx>

Run it after every build_partN.py (it replaces pack_docx.py as the last step). It:
  1. bookmarks every body heading: "Part N: ...", the numbered section headings ("1. ...", "16.AI ...")
     and "สรุป Part N" (bookmark names start with _TocCL, so Word hides them);
  2. regenerates everything between the " สารบัญ" title and the body "Part 1:" heading:
     one line per heading with a dot leader and a PAGEREF field (clickable, F9 in Word refreshes it),
     followed by a section break so the cover + สารบัญ have no page number;
  3. gives the body section a header with a right-aligned PAGE field, starting at 1;
  4. packs the docx, asks Word (toc_pages.ps1) which page each bookmark is on, writes those numbers
     into the PAGEREF results and packs again.
Body page numbers don't depend on the length of the สารบัญ (the body always starts on a new page),
so one Word pass is enough.
"""
import html, json, os, re, subprocess, sys, zipfile, xml.dom.minidom
from xml.sax.saxutils import escape

UN, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(UN, 'word', 'document.xml')
FONT = '<w:rFonts w:ascii="Angsana New" w:cs="Angsana New" w:eastAsia="Angsana New" w:hAnsi="Angsana New"/>'
BM_PREFIX, BM_BASE = '_TocCL', 90000
HDR_FILE, HDR_RID = 'header2.xml', 'rIdPageNumHdr'
PAGE_SECT = ('<w:pgSz w:h="16834" w:w="11909" w:orient="portrait"/>'
             '<w:pgMar w:bottom="1440" w:top="1440" w:left="1440" w:right="1440" w:header="720" w:footer="720"/>')
TAB_POS = 9020   # right edge of the text area (page 11909 - margins 2880)

P_RE = re.compile(r'<w:p[ >].*?</w:p>', re.S)


def ptext(p):
    return html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))


def rpr(bold=False, size=30):
    b = '<w:b w:val="1"/><w:bCs w:val="1"/>' if bold else ''
    return f'<w:rPr>{FONT}{b}<w:color w:val="1f1f1f"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'


def run(text, bold=False):
    return f'<w:r>{rpr(bold)}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


# ---------------------------------------------------------------- 1. bookmarks
doc = open(DOC, encoding='utf8').read()
doc = re.sub(rf'<w:bookmarkStart w:id="\d+" w:name="{BM_PREFIX}[^"]*"/>', '', doc)
doc = re.sub(rf'<w:bookmarkEnd w:id="9\d{{4}}"/>', '', doc)

# blank out tables so numbers inside table cells (e.g. "10.0.1.0/24") are never taken as headings
masked = re.sub(r'<w:tbl>.*?</w:tbl>', lambda m: ' ' * len(m.group()), doc, flags=re.S)
paras = list(P_RE.finditer(masked))
part_idx = [i for i, m in enumerate(paras) if ptext(m.group()).startswith('Part ')
            and re.match(r'Part \d+:', ptext(m.group()))]
# the first "Part 1:" is the สารบัญ line, the second is the body heading
body_start = [i for i in part_idx if ptext(paras[i].group()).startswith('Part 1:')][1]

entries = []     # (level, text, bookmark name, paragraph index)
next_sec = 1
for i in range(body_start, len(paras)):
    t = ptext(paras[i].group()).strip()
    m = re.match(r'Part (\d+):', t)
    if m:
        entries.append((0, t, f'{BM_PREFIX}P{m.group(1)}', i))
        continue
    if re.match(rf'{next_sec}\.\D', t):
        entries.append((1, t, f'{BM_PREFIX}S{next_sec}', i))
        next_sec += 1
        continue
    m = re.match(r'สรุป Part (\d+)$', t)
    if m:
        entries.append((1, t, f'{BM_PREFIX}Sum{m.group(1)}', i))

# insert bookmarks from the end so earlier offsets stay valid
for n, (lvl, t, name, i) in sorted(enumerate(entries), key=lambda e: -e[1][3]):
    m = paras[i]
    p = doc[m.start():m.end()]
    start = f'<w:bookmarkStart w:id="{BM_BASE + n}" w:name="{name}"/>'
    end = f'<w:bookmarkEnd w:id="{BM_BASE + n}"/>'
    if '</w:pPr>' in p:
        p = p.replace('</w:pPr>', '</w:pPr>' + start, 1)
    else:
        p = re.sub(r'^(<w:p[^>]*>)', r'\1' + start, p)
    p = p[:-len('</w:p>')] + end + '</w:p>'
    doc = doc[:m.start()] + p + doc[m.end():]


# ---------------------------------------------------------------- 2. สารบัญ block
def toc_line(lvl, text, name, page):
    ind = '<w:ind w:left="0" w:right="400"/>' if lvl == 0 else '<w:ind w:left="360" w:right="400"/>'
    before = 100 if lvl == 0 else 0
    ppr = (f'<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TAB_POS}"/></w:tabs>'
           f'<w:spacing w:before="{before}" w:after="0" w:line="240" w:lineRule="auto"/>{ind}<w:rPr>{FONT}<w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:pPr>')
    fld = (f'<w:r>{rpr(lvl == 0)}<w:fldChar w:fldCharType="begin"/></w:r>'
           f'<w:r>{rpr(lvl == 0)}<w:instrText xml:space="preserve"> PAGEREF {name} \\h </w:instrText></w:r>'
           f'<w:r>{rpr(lvl == 0)}<w:fldChar w:fldCharType="separate"/></w:r>'
           f'<w:r>{rpr(lvl == 0)}<w:t>{page}</w:t></w:r>'
           f'<w:r>{rpr(lvl == 0)}<w:fldChar w:fldCharType="end"/></w:r>')
    body = run(text, lvl == 0) + f'<w:r>{rpr(lvl == 0)}<w:tab/></w:r>' + fld
    return f'<w:p>{ppr}<w:hyperlink w:anchor="{name}" w:history="1">{body}</w:hyperlink></w:p>'


def build_block(pages):
    head = (f'<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:before="0" w:after="60"/></w:pPr>{run("หน้า", True)}</w:p>')
    lines = ''.join(toc_line(l, t, n, pages.get(n, '0')) for l, t, n, _ in entries)
    brk = (f'<w:p><w:pPr><w:sectPr><w:headerReference r:id="rId7" w:type="default"/>{PAGE_SECT}</w:sectPr></w:pPr></w:p>')
    return head + lines + brk


def write_block(doc, pages):
    ps = list(P_RE.finditer(doc))
    title = next(m for m in ps if ptext(m.group()).strip() == 'สารบัญ')
    parts = [m for m in ps if re.match(r'Part 1:', ptext(m.group()))]
    body = parts[1]            # first "Part 1:" is in the สารบัญ, second is the body heading
    # title starts a new page (the cover is spaced with empty paragraphs)
    t = title.group()
    if '<w:pageBreakBefore/>' not in t:
        t = t.replace('<w:pPr>', '<w:pPr><w:pageBreakBefore/>', 1) if '<w:pPr>' in t else t
    return doc[:title.start()] + t + build_block(pages) + doc[body.start():]


doc = write_block(doc, {})

# ---------------------------------------------------------------- 3. page-number header on the body section
final_sect = (f'<w:sectPr><w:headerReference r:id="{HDR_RID}" w:type="default"/>{PAGE_SECT}'
              f'<w:pgNumType w:start="1"/></w:sectPr>')
last = doc.rindex('<w:sectPr>')
doc = doc[:last] + final_sect + doc[doc.index('</w:sectPr>', last) + len('</w:sectPr>'):]
open(DOC, 'w', encoding='utf8').write(doc)

hdr_path = os.path.join(UN, 'word', HDR_FILE)
if not os.path.exists(hdr_path):
    ns = open(os.path.join(UN, 'word', 'header1.xml'), encoding='utf8').read()
    root_open = re.search(r'<w:hdr [^>]*>', ns).group()
    fld = (f'<w:r>{rpr()}<w:fldChar w:fldCharType="begin"/></w:r>'
           f'<w:r>{rpr()}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
           f'<w:r>{rpr()}<w:fldChar w:fldCharType="separate"/></w:r>'
           f'<w:r>{rpr()}<w:t>1</w:t></w:r>'
           f'<w:r>{rpr()}<w:fldChar w:fldCharType="end"/></w:r>')
    hdr = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>{root_open}'
           f'<w:p><w:pPr><w:jc w:val="right"/></w:pPr>{fld}</w:p></w:hdr>')
    open(hdr_path, 'w', encoding='utf8').write(hdr)

rels_path = os.path.join(UN, 'word', '_rels', 'document.xml.rels')
rels = open(rels_path, encoding='utf8').read()
if HDR_RID not in rels:
    rels = rels.replace('</Relationships>',
                        f'<Relationship Id="{HDR_RID}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                        f'relationships/header" Target="{HDR_FILE}"/></Relationships>')
    open(rels_path, 'w', encoding='utf8').write(rels)

ct_path = os.path.join(UN, '[Content_Types].xml')
ct = open(ct_path, encoding='utf8').read()
if f'/word/{HDR_FILE}' not in ct:
    ct = ct.replace('</Types>', '<Override ContentType="application/vnd.openxmlformats-officedocument.'
                                f'wordprocessingml.header+xml" PartName="/word/{HDR_FILE}"/></Types>')
    open(ct_path, 'w', encoding='utf8').write(ct)


# ---------------------------------------------------------------- 4. pack, ask Word for page numbers, fill in
def pack():
    xml.dom.minidom.parse(DOC)
    files = []
    for root, _, fs in os.walk(UN):
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), UN).replace(os.sep, '/'))
    files.sort(key=lambda n: (n != '[Content_Types].xml', not n.startswith('_rels'), n))
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in files:
            z.write(os.path.join(UN, n), n)


pack()
res = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                      os.path.join(HERE, 'toc_pages.ps1'), '-Docx', os.path.abspath(OUT), '-Prefix', BM_PREFIX],
                     capture_output=True, text=True, encoding='utf-8')
line = next((l for l in res.stdout.splitlines() if l.startswith('{')), None)
if not line:
    raise SystemExit('Word did not return page numbers:\n' + res.stdout + res.stderr)
pages = {k: str(v) for k, v in json.loads(line).items()}

doc = open(DOC, encoding='utf8').read()
doc = write_block(doc, pages)
open(DOC, 'w', encoding='utf8').write(doc)
pack()
missing = [n for _, _, n, _ in entries if n not in pages]
print(f'สารบัญ: {len(entries)} entries, packed -> {OUT}' + (f' | MISSING pages: {missing}' if missing else ''))
for l, t, n, _ in entries:
    print(('  ' if l else '') + f'{t[:60]} ... {pages.get(n)}')
