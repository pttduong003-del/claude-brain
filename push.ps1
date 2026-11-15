# Copy brain files from ~/.claude into this repo, then commit and push.
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot
$claude = Join-Path $env:USERPROFILE '.claude'
# Claude names project folders by the path with every non-alphanumeric char turned into '-'
$encHome = $env:USERPROFILE -replace '[^A-Za-z0-9]', '-'

function Mirror($src, $dst) {
    robocopy $src $dst /MIR /XD .git __pycache__ /XF *KEY*.txt .env /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed: $src" }
}

Mirror (Join-Path $claude 'skills') (Join-Path $repo 'skills')
Mirror (Join-Path $claude 'hooks')  (Join-Path $repo 'hooks')
Copy-Item (Join-Path $claude 'settings.json') (Join-Path $repo 'settings.json') -Force

# Memory: store under the path relative to the home folder so other machines/usernames map back
Get-ChildItem (Join-Path $claude 'projects') -Directory | ForEach-Object {
    $mem = Join-Path $_.FullName 'memory'
    if (-not $_.Name.StartsWith("$encHome-")) { return }
    if ($_.Name -like '*AppData-Local*') { return }  # skip temp scratch workspaces
    if (-not (Test-Path $mem) -or -not (Get-ChildItem $mem -File)) { return }
    Mirror $mem (Join-Path $repo "memory\$($_.Name.Substring($encHome.Length + 1))")
}

Set-Location $repo
git add -A
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { git commit -m "sync from $env:COMPUTERNAME $(Get-Date -Format 'yyyy-MM-dd HH:mm')" }
git pull --rebase
if ($LASTEXITCODE -ne 0) { throw 'git pull --rebase failed: resolve conflict, then run again' }
git push
if ($LASTEXITCODE -ne 0) { throw 'git push failed' }
Write-Host 'Brain pushed.'
exit 0
