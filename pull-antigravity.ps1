# Pull latest brain and install it for Google Antigravity (for machines without Claude Code).
# Memory -> block inside ~/.gemini/GEMINI.md (global rules). Skills -> Antigravity global skills folders.
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot
$gemini = Join-Path $env:USERPROFILE '.gemini'

Set-Location $repo
git pull
if ($LASTEXITCODE -ne 0) { throw 'git pull failed' }

# Same per-machine list as pull.ps1: these memory files stay out (this machine writes its own rule)
$localFile = Join-Path $env:USERPROFILE '.claude\brain-local.txt'
$localOnly = @(if (Test-Path $localFile) { Get-Content $localFile | Where-Object { $_.Trim() } | ForEach-Object { $_.Trim() } })

# Antigravity moved its global skills folder between versions; install to both
foreach ($dst in @("$gemini\config\skills", "$gemini\antigravity\skills")) {
    robocopy (Join-Path $repo 'skills') $dst /E /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed: $dst" }
}

$start = '<!-- claude-brain:start -->'; $end = '<!-- claude-brain:end -->'
$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine($start)
[void]$sb.AppendLine('# Brain synced from Claude Code (do not edit inside this block; pull-antigravity.ps1 rewrites it)')
Get-ChildItem (Join-Path $repo 'memory') -Directory | ForEach-Object {
    [void]$sb.AppendLine("`n## Project: $($_.Name) (apply ONLY in the project folder whose path under the user folder matches this name, '\' written as '-')")
    Get-ChildItem $_.FullName -File -Filter *.md | Where-Object { $_.Name -ne 'MEMORY.md' -and $localOnly -notcontains $_.Name } | ForEach-Object {
        # drop YAML frontmatter, keep the rule body
        $body = (Get-Content $_.FullName -Raw -Encoding UTF8) -replace '(?s)^---.*?\r?\n---\r?\n', ''
        [void]$sb.AppendLine("`n### $($_.BaseName)`n$($body.Trim())")
    }
}
[void]$sb.AppendLine($end)

# Replace only our block; keep anything the user wrote in GEMINI.md
$rules = Join-Path $gemini 'GEMINI.md'
New-Item -ItemType Directory -Force $gemini | Out-Null
$old = if (Test-Path $rules) { Get-Content $rules -Raw -Encoding UTF8 } else { '' }
$pattern = '(?s)' + [regex]::Escape($start) + '.*?' + [regex]::Escape($end)
$new = if ($old -match $pattern) { [regex]::Replace($old, $pattern, { param($m) $sb.ToString().TrimEnd() }) } else { ($old.TrimEnd() + "`n`n" + $sb.ToString()).TrimStart() }
[System.IO.File]::WriteAllText($rules, $new, [System.Text.UTF8Encoding]::new($false))

Write-Host "Brain installed for Antigravity: $rules + skills. Restart Antigravity."
exit 0
