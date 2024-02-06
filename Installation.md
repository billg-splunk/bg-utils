# Installation Notes

For environments like Windows Core you may need an easy way to download the install/uninstall scripts.

To get these from a powershell shell:
```powershell
# You may need to run this first, if the following command doesn't run by itself
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

# Download the file
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/billg-splunk/bg-utils/main/Installation.md" -OutFile "install.txt"

# Here's a shorter version with bit.ly
Invoke-WebRequest -Uri "https://bit.ly/o11y-install" -OutFile "install.txt"
```


## Windows OTel installation
```powershell
& {Set-ExecutionPolicy Bypass -Scope Process -Force; $script = ((New-Object System.Net.WebClient).DownloadString('https://dl.signalfx.com/splunk-otel-collector.ps1')); $params = @{access_token = "TOKEN"; realm = "us1"; mode = "agent"; with_fluentd = 0; with_dotnet_instrumentation = 0}; Invoke-Command -ScriptBlock ([scriptblock]::Create(". {$script} $(&{$args} @params)"))}
```

## Windows OTel Uninstall
```powershell
$MyProgram = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\uninstall\* | Where { $_.DisplayName -eq "Splunk OpenTelemetry Collector" }

cmd /c $MyProgram.UninstallString
```

## Windows Smart Agent Install
```powershell
& {Set-ExecutionPolicy Bypass -Scope Process -Force; 
$script = ((New-Object System.Net.WebClient).DownloadString('https://dl.signalfx.com/signalfx-agent.ps1'));
$params = @{access_token = '<access token>'; ingest_url = 'https://ingest.<realm>.signalfx.com'; api_url = 'https://api.<realm>.signalfx.com'}; Invoke-Command -ScriptBlock ([scriptblock]::Create(". {$script} $(&{$args} @params)"))}
```