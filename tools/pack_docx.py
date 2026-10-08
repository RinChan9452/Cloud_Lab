"""Zip an unpacked docx folder back into a .docx (this machine has no `zip` command).

Usage: python pack_docx.py <unpacked_dir> <out.docx>
Also checks that word/document.xml is well-formed before writing.
"""
import os, sys, zipfile, xml.dom.minidom

src, out = sys.argv[1], sys.argv[2]
xml.dom.minidom.parse(os.path.join(src, 'word', 'document.xml'))   # raises if the XML is broken

files = []
for root, _, fs in os.walk(src):
    for f in fs:
        files.append(os.path.relpath(os.path.join(root, f), src).replace(os.sep, '/'))
# [Content_Types].xml first, then _rels, then the rest
files.sort(key=lambda n: (n != '[Content_Types].xml', not n.startswith('_rels'), n))
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in files:
        z.write(os.path.join(src, n), n)
print(f'packed {len(files)} files -> {out} ({os.path.getsize(out) // 1024} KB)')
