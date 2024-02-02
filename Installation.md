# Installation Notes

## Windows OTel installation
```
& {Set-ExecutionPolicy Bypass -Scope Process -Force; $script = ((New-Object System.Net.WebClient).DownloadString('https://dl.signalfx.com/splunk-otel-collector.ps1')); $params = @{access_token = "TOKEN"; realm = "us1"; mode = "agent"; with_fluentd = 0; with_dotnet_instrumentation = 0}; Invoke-Command -ScriptBlock ([scriptblock]::Create(". {$script} $(&{$args} @params)"))}
```


## Windows Smart Agent Install
```
& {Set-ExecutionPolicy Bypass -Scope Process -Force; 
$script = ((New-Object System.Net.WebClient).DownloadString('https://dl.signalfx.com/signalfx-agent.ps1'));
$params = @{access_token = '<access token>'; ingest_url = 'https://ingest.<realm>.signalfx.com'; api_url = 'https://api.<realm>.signalfx.com'}; Invoke-Command -ScriptBlock ([scriptblock]::Create(”. {$script} $(&{$args} @params)”))}
```