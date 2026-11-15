# Pull latest brain from GitHub and copy it into ~/.claude on this machine.
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot
$claude = Join-Path $env:USERPROFILE '.claude'
$encHome = $env:USERPROFILE -replace '[^A-Za-z0-9]', '-'

Set-Location $repo
git pull
if ($LASTEXITCODE -ne 0) { throw 'git pull failed' }

# Copy only adds/overwrites; files that exist only on this machine are kept.
# brain-local.txt (one file name per line, not synced): files this machine keeps to itself
$localFile = Join-Path $claude 'brain-local.txt'
$xf = @(if (Test-Path $localFile) { Get-Content $localFile | Where-Object { $_.Trim() } | ForEach-Object { $_.Trim() } })
if ($xf) { $xf = @('/XF') + $xf }

function Merge($src, $dst) {
    robocopy $src $dst /E @xf /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed: $src" }
}

Merge (Join-Path $repo 'skills') (Join-Path $claude 'skills')
Merge (Join-Path $repo 'hooks')  (Join-Path $claude 'hooks')
Copy-Item (Join-Path $repo 'settings.json') (Join-Path $claude 'settings.json') -Force

Get-ChildItem (Join-Path $repo 'memory') -Directory | ForEach-Object {
    Merge $_.FullName (Join-Path $claude "projects\$encHome-$($_.Name)\memory")
}
Write-Host 'Brain updated. Restart Claude to load it.'
exit 0
