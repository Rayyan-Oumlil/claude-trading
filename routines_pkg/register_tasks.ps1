# Register Claude Trading routines as Windows Scheduled Tasks.
#
# Usage (from PowerShell, non-admin is fine for user-level tasks):
#   cd "c:\Users\rayya\Desktop\Claude Trading"
#   powershell -ExecutionPolicy Bypass -File routines_pkg\register_tasks.ps1
#
# To remove the tasks later:
#   Unregister-ScheduledTask -TaskName "ClaudeTrading-Premarket" -Confirm:$false
#   Unregister-ScheduledTask -TaskName "ClaudeTrading-EODClose" -Confirm:$false
#
# To run one immediately for testing:
#   Start-ScheduledTask -TaskName "ClaudeTrading-Premarket"

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$premarketScript = Join-Path $repoRoot "routines_pkg\run_premarket.bat"
$eodScript = Join-Path $repoRoot "routines_pkg\run_eod.bat"

if (-not (Test-Path $premarketScript)) { throw "Missing $premarketScript" }
if (-not (Test-Path $eodScript)) { throw "Missing $eodScript" }

# ---- Pre-market: 06:00 Mon-Fri ----
$premarketAction = New-ScheduledTaskAction `
    -Execute $premarketScript `
    -WorkingDirectory $repoRoot

$premarketTrigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At 6:00am

$premarketSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

Register-ScheduledTask `
    -TaskName "ClaudeTrading-Premarket" `
    -Action $premarketAction `
    -Trigger $premarketTrigger `
    -Settings $premarketSettings `
    -Description "Claude Trading pre-market snapshot (watchlist prices -> memory/routine-state.md)" `
    -Force

Write-Host "Registered: ClaudeTrading-Premarket (Mon-Fri 06:00)"

# ---- EOD close: 15:00 Mon-Fri ----
$eodAction = New-ScheduledTaskAction `
    -Execute $eodScript `
    -WorkingDirectory $repoRoot

$eodTrigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At 3:00pm

$eodSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

Register-ScheduledTask `
    -TaskName "ClaudeTrading-EODClose" `
    -Action $eodAction `
    -Trigger $eodTrigger `
    -Settings $eodSettings `
    -Description "Claude Trading EOD close (account + positions -> journal + memory/portfolio-state.md)" `
    -Force

Write-Host "Registered: ClaudeTrading-EODClose (Mon-Fri 15:00)"
Write-Host ""
Write-Host "Done. Verify with: Get-ScheduledTask ClaudeTrading-*"
Write-Host "Test a task now with: Start-ScheduledTask ClaudeTrading-Premarket"
