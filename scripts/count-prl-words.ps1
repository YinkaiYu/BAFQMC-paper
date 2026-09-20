[CmdletBinding()]
param(
    [switch]$NoBuild,
    [switch]$Check,
    [string[]]$TableLines = @()
)

$ErrorActionPreference = 'Stop'
function Quote-Bash([string]$Value) {
    $sq = [string][char]39
    $dq = [string][char]34
    return $sq + $Value.Replace($sq, $sq + $dq + $sq + $dq + $sq) + $sq
}
$arguments = @('python3', 'scripts/count-prl-words.py')
if ($NoBuild) { $arguments += '--no-build' }
if ($Check) { $arguments += '--check' }
foreach ($item in $TableLines) { $arguments += @('--table-lines', $item) }
$command = ($arguments | ForEach-Object { Quote-Bash $_ }) -join ' '
& (Join-Path $PSScriptRoot 'run-in-wsl.ps1') $command
exit $LASTEXITCODE
