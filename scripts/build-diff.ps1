[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidatePattern('^[A-Za-z0-9._/-]+$')]
    [string]$Baseline
)

$ErrorActionPreference = 'Stop'
$launcher = Join-Path $PSScriptRoot 'run-in-wsl.ps1'

& $launcher "bash ./scripts/build-diff.sh $Baseline"
exit $LASTEXITCODE
