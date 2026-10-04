# Install Usage agent on windows machine to report Memory, Cpu, and Storage Usage
# It creates a ScheduledTask called "OverwatchAgent" that runs the FastAPI + uvicorn app.
$baseDir = "C:\overwatch-agent"
$taskName = "OverwatchAgent"
cd $baseDir


# install python packges
if (!(Test-Path "$baseDir\env")) {
    Write-Host "Creating Virtual Environment..."
    python -m venv env
    
}
./env/Scripts/pip.exe install -r requirements.txt


# clear any existing rules or tasks from previous runs
$taskExists = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($taskExists) {
    Write-Host "Stopping and removing Scheduled Task..."
    # Stopping a task in Windows can sometimes throw an error if it's already idle, so we catch it softly
    Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
} else {
    Write-Host "Scheduled task $taskName not found. Skipping."
}

# 3. Clean up the Windows Defender Firewall Rule
$ruleExists = Get-NetFirewallRule -DisplayName "OverwatchAgentRule" -ErrorAction SilentlyContinue
if ($ruleExists) {
    Write-Host "Removing Firewall Rules..."
    Remove-NetFirewallRule -DisplayName "OverwatchAgentRule"
}

# FIXME:maybe adjust this logic?
# if (Test-Path $baseDir) {
#     Write-Host "Wiping project folder and logs at $baseDir..."
#     # Force allows deleting read-only files, Recurse steps into all subfolders
#     Remove-Item -Path $baseDir -Force -Recurse
# }



# Recreate firewall rules, only accessible through tailscale
New-NetFirewallRule -DisplayName "OverwatchAgentRule" `
    -Direction Inbound `
    -LocalPort 8001 `
    -Protocol TCP `
    -Action Allow `
    -RemoteAddress "100.64.0.0/10"

# Run the agent using uvicorn
$tailscale_addr = tailscale ip -4
$binary = "$baseDir\env\Scripts\python.exe"
$fullArg = "/c cd /d `"$baseDir`" && `"$binary`" -m uvicorn agent:app --host $tailscale_addr --port 8001 > `"$baseDir\startup_log.txt`" 2>&1"

# Create ScheduledTask to have the app run indefinitely
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument $fullArg
$trigger = New-ScheduledTaskTrigger -AtStartup
# Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName $taskName -User $env:USERNAME -RunLevel Highest -Force
Start-ScheduledTask -TaskName $taskName

# Check that Task is running
Start-Sleep -Seconds 2
Get-ScheduledTask -TaskName $taskName