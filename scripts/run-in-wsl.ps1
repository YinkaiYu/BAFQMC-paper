[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Command
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$commandBase64 = [Convert]::ToBase64String(
    [Text.Encoding]::UTF8.GetBytes($Command)
)
$runner = "if [ -f ~/.profile ]; then . ~/.profile; fi; printf '%s' '$commandBase64' | base64 --decode | bash -l -s"

& wsl.exe --cd $repoRoot -- bash -lc $runner
exit $LASTEXITCODE
