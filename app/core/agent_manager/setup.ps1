# Install Usage agent on windows machine to report Memory, Cpu, and Storage Usage
# It creates a ScheduledTask called "OverwatchAgent" that runs the FastAPI + uvicorn app.
$baseDir = "C:\overwatch-agent"

cd $baseDir

# install python packges
if (!(Test-Path "$baseDir\env")) {
    Write-Host "Creating Virtual Environment..."
    python -m venv env
    
}
./env/Scripts/pip.exe install -r requirements.txt

# Recreate firewall rules, only accessible through tailscale
Remove-NetFirewallRule -DisplayName "OverwatchAgentRule"
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
Unregister-ScheduledTask -TaskName "OverwatchAgent" -Confirm:$false
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "OverwatchAgent" -User $env:USERNAME -RunLevel Highest -Force
Start-ScheduledTask -TaskName "OverwatchAgent"

# Check that Task is running
Start-Sleep -Seconds 2
Get-ScheduledTask -TaskName "OverwatchAgent"