# Cloud lab report

Lab report for the Kasetsart University course แนวคิดและบริการการคำนวณแบบคลาวด์ (term 1/2569), written in
`รายงานปฏิบัติการ.docx`. Each `Part N` folder holds the user's AWS screenshots for that Part of the report.

The report is the user's own step-by-step guide. They will come back to it later to rebuild the labs, so every step
must be clear enough to follow without remembering the lab.

## Later goal (not part of the report)

After the report is done, the user will build a cloud-native system with a 3-tier architecture using what these labs
teach. **Do not put 3-tier content in the report.** Keep it to what was done in each lab.

## Report structure

- **สารบัญ:** the table of contents lists Parts 1–6 and their numbered lab sections (1–16). The body repeats each
  `Part N: ...` heading. Write each Part's content under its body heading.
- **Section titles:** keep the English titles exactly as in the สารบัญ (e.g. `2. Create a Security Group.`).
- **Language:** everything else is in **Thai**. Keep AWS console names in English as they appear on screen
  (button, menu and field names such as **Create key pair** and **Network & Security > Key Pairs**).
- **Each section contains:**
  1. **วัตถุประสงค์:** what the service is and why it is needed.
  2. **ขั้นตอนการทำ:** numbered steps `ขั้นตอนที่ N.M`. Each step says where to click and the exact values typed or
     chosen (names, ports, instance type and so on), followed by its screenshot and the caption `รูปที่ N.M ...`.
     Split long sections into `ส่วน A / ส่วน B` sub-headings.
  3. **Orange call-out boxes** for warnings, errors seen in the screenshots, troubleshooting, and wait times.
- **End of each Part:** a `สรุป Part N` with a table of every value used (names, IDs, IPs, sizes) and a short list of
  `สิ่งที่ควรจำ`.
- **Sections without photos yet:** keep just the heading, in its place before the summary. When the photos arrive, add that section to the existing `build_partN.py`, update the summary, and rebuild
  the whole Part.
- **Page break:** the Part ends with a page break, so the next Part starts on a new page.

## Workflow for a Part

1. **Read the Part** in the docx to get its section list (the body text may hold short notes from the user; keep their
   meaning and translate them into Thai).
2. **Sort photos** in the `Part N` folder into one subfolder per section, named `<section no> <short English title>`
   (e.g. `Part 1/3 Provision an EC2 Instance/`). Use the number at the start of each filename to match photos to
   sections, and **move, don't copy**. The filenames describe the step (e.g. `16 Choose RDP then click download RDP
   shortcut.png`). Tell the user about any judgement calls on where a photo belongs.
3. **View every screenshot** before writing. Read the real values from them (resource names, settings, IPs, errors)
   instead of guessing. If something can't be seen (e.g. which version was downloaded), say so in the text rather than
   inventing it.
4. **Write the content** as `tools/build_partN.py`, modelled on `tools/build_part1.py`:
   - helpers from `tools/report_lib.py`: `H`, `SUB`, `P`, `STEP`, `BUL`, `BOX`, `CODE`, `TABLE`, `PAGEBREAK`,
     `Images`, `load_photos`, `splice_part` (`CODE` takes a string, or a list of lines for a multi-line block);
   - use `Images(UN, 'partN', docpr_base=N*1000)` so image ids never clash between Parts;
   - `splice_part(UN, N, xml, IMG)` replaces everything between the body `Part N:` heading and the body `Part N+1:`
     heading, so re-running the script rebuilds that Part cleanly.
5. **Build:**
   - unpack the current report into a new scratchpad folder;
   - run `python tools/build_partN.py <unpacked> "D:/Cloud lab/Part N"`;
   - run `python tools/pack_docx.py <unpacked> <scratchpad>/out.docx`.
6. **Verify:** run `tools/export_pdf.ps1` (Word COM → PDF), then `tools/render_pages.ps1 -Pages ...` (PDF → PNG), and
   look at the first page, a table page and the summary page of the Part.
7. **Save:** before overwriting `รายงานปฏิบัติการ.docx`, copy the current file to the scratchpad as a backup. Also
   check it wasn't edited by the user since it was last written (compare hashes). If it was, build on the user's
   version instead of overwriting it.
8. **Report back:** say what was written, any assumptions, and anything sensitive visible in the screenshots, such as
   a decrypted Windows password.

## Formatting (match the existing document)

- **Font:** Angsana New, 15pt (`sz 30`), text colour `1f1f1f`. Section headings are bold 17pt; sub-headings are bold
  and dark blue `1F4E79`.
- **Screenshots:** 6 inches wide, centred, with a thin grey border. The caption goes below in 13pt grey.
- **Bullets:** use the existing bullet list `numId 1`. Never type a literal `•`.
- **Arrows:** Angsana New has no `→` glyph. `runs()` already puts arrows in an Arial run, so write `→` normally in the
  content.
- **Breaks:** the original document spaces pages with empty paragraphs and has no real page breaks. Use `PAGEBREAK()`.

## Machine notes

- **No `zip`, LibreOffice, poppler or PIL.** Use `tools/pack_docx.py`, Microsoft Word through COM (installed) and the
  Windows.Data.Pdf renderer in `render_pages.ps1`.
- **Removals:** `rm -rf` on relative or variable paths is blocked by a safety check. Unpack into a fresh, new folder
  instead of deleting old ones.
- **Python:** run it with `PYTHONIOENCODING=utf-8` because the Thai filenames break the default cp1252 console. Don't
  use `python -I` for the tools scripts; it stops `report_lib` from being imported.
- **File size:** screenshots are kept at full resolution, so the docx grows fast (~90 MB with Parts 1–4 and sections 13–14).
- **Long photo filenames:** some of the user's filenames are so long that moving them into a section folder exceeds
  the Windows 260-character path limit. Shorten just that filename (keep its number and meaning) and copy the full
  original wording into the notes file.
- **Viewing many screenshots:** image reads in a long session can come back empty. View 2–3 at a time and append
  the exact values (names, IDs, IPs, settings, errors) to a notes file in the scratchpad after each batch, then write
  the Part from the notes.
