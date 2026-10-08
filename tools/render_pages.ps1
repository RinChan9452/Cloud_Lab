# Render PDF pages to PNG with the built-in Windows.Data.Pdf API (no poppler/LibreOffice on this machine).
# Usage: powershell -File render_pages.ps1 -Pdf <file.pdf> -OutDir <folder> -Pages 3,4,5
# Page numbers are 1-based and must be <= the PageCount it prints. Do not pipe the output into Select-Object -First.
param([string]$Pdf, [string]$OutDir, [int[]]$Pages)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.InMemoryRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$t) {
    $task = $asTaskGeneric.MakeGenericMethod($t).Invoke($null, @($op))
    $task.Wait() | Out-Null
    $task.Result
}
function AwaitAction($op) {
    $m = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' } | Select-Object -First 1
    $m.Invoke($null, @($op)).Wait() | Out-Null
}

$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Pdf)) ([Windows.Storage.StorageFile])
$doc = Await ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)) ([Windows.Data.Pdf.PdfDocument])
"PageCount: $($doc.PageCount)"
foreach ($p in $Pages) {
    $page = $doc.GetPage($p - 1)
    $stream = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
    $opts = New-Object Windows.Data.Pdf.PdfPageRenderOptions
    $opts.DestinationWidth = 900
    AwaitAction ($page.RenderToStreamAsync($stream, $opts))
    $net = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($stream.GetInputStreamAt(0))
    $out = Join-Path $OutDir ("page-{0:D2}.png" -f $p)
    $fs = [System.IO.File]::Create($out)
    $net.CopyTo($fs); $fs.Close()
    $page.Dispose()
    $out
}
