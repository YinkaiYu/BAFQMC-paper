[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$launcher = Join-Path $PSScriptRoot 'run-in-wsl.ps1'

& $launcher 'bash ./scripts/build-manuscript.sh'
exit $LASTEXITCODE
