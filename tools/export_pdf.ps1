# Open a .docx in Microsoft Word (read-only, hidden) and export it to PDF.
# Usage: powershell -File export_pdf.ps1 -Docx <in.docx> -Pdf <out.pdf>
param([string]$Docx, [string]$Pdf)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($Docx, $false, $true)
    $d.ExportAsFixedFormat($Pdf, 17)   # 17 = wdExportFormatPDF
    $d.Close(0)
} finally {
    $w.Quit()
}
"Exported $Pdf"
