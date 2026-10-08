# Print a JSON object {bookmarkName: displayedPageNumber} for every bookmark whose name starts with -Prefix.
# Used by update_toc.py. Opens the docx read-only in hidden Word; nothing is saved.
param([string]$Docx, [string]$Prefix)
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($Docx, $false, $true)
    $d.Repaginate()
    $d.Bookmarks.ShowHidden = $true    # names starting with "_" are hidden bookmarks
    $pages = @{}
    foreach ($b in $d.Bookmarks) {
        if ($b.Name.StartsWith($Prefix)) {
            # 1 = wdActiveEndAdjustedPageNumber (respects "start at 1" of the body section)
            $pages[$b.Name] = $b.Range.Information(1)
        }
    }
    $d.Close(0)
} finally {
    $w.Quit()
}
$pages | ConvertTo-Json -Compress
