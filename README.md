# bg-utils
Tips and tricks

## Windows Smart Agent Install
```
& {Set-ExecutionPolicy Bypass -Scope Process -Force; 
$script = ((New-Object System.Net.WebClient).DownloadString('https://dl.signalfx.com/signalfx-agent.ps1'));
$params = @{access_token = '<access token>'; ingest_url = 'https://ingest.<realm>.signalfx.com'; api_url = 'https://api.<realm>.signalfx.com'}; Invoke-Command -ScriptBlock ([scriptblock]::Create(”. {$script} $(&{$args} @params)”))}
```