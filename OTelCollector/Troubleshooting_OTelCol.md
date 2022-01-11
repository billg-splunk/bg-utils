# Troubleshooting OTel Collector

Guidance on troubleshooting that supplements the official guides.

[OTel Collector Troubleshooting](https://github.com/open-telemetry/opentelemetry-collector/blob/main/docs/troubleshooting.md)

[Splunk Distribution Troubleshooting](https://github.com/signalfx/splunk-otel-collector/blob/main/docs/troubleshooting.md)

## Debug mode

Like on Linux you can enable debugging by adding this to the services section:
```
service:
  telemetry:
    logs:
      level: "debug"
```

## Install issues

One potential issue with installation may be how TLS is configured.

On Windows this can be resolved by running the following prior to running the installer:

```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

Note this command will only work in this session, so if you open another you will need to run this again.
## Connection issues

One check to make is if you can send a datapoint. Update the token and realm and use the following commands.

### curl

```
curl -qs -H'X-SF-Token:THE_TOKEN' https://ingest.THE_REALM.signalfx.com/v2/datapoint -X POST -v -d '{}' -H "Content-Type: application/json"
```

### Powershell (Windows)

```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$resp = Invoke-WebRequest -Uri https://ingest.THE_REALM.signalfx.com/v2/event -Method POST -ContentType "application/json" -Headers @{"X-Sf-Token"="THE_TOKEN"} -Body "[]" -UseBasicParsing
echo $resp.StatusCode
```

### Sending actual data

You can replace the previous commands with actual data. For example to send a datapoint (replace the timestamp with a recent one):

First, get an epoch:

```
# On Mac or Linux
date -u +"%s000"
# On Windows
[DateTimeOffset]::Now.ToUnixTimeSeconds() * 1000
```

And the data is:
```
{
  "gauge": [
    {
      "metric": "cpu.utilization",
      "value": 50,
      "dimensions": {
        "host.name": "my-test"
      },
      "timestamp": 1557225030000
    }
  ]
}

## Proxies

It may be that you need to configure the proxy for your environment. This can be done by setting environment variables:

```
# Skip the "NO_PROXY" lines if you don't have any addresses to skip the proxy
# On Linux
sudo sed -i '$ a [Service]' /etc/systemd/system/splunk-otel-collector.service.d/service-proxy.conf
sudo sed -i '$ a Environment="NO_PROXY=localhost,127.0.0.1,169.254.169.254,::1" ' /etc/systemd/system/splunk-otel-collector.service.d/service-proxy.conf
sudo sed -i '$ a HTTP_PROXY="http://<YOUR_PROXY_SERVER_IP:PORT>" ' /etc/systemd/system/splunk-otel-collector.service.d/service-proxy.conf
sudo sed -i '$ a HTTPS_PROXY="http://<YOUR_PROXY_SERVER_IP:PORT>" ' /etc/systemd/system/splunk-otel-collector.service.d/service-proxy.conf# On Windows
sudo systemctl daemon-reload
sudo systemctl restart splunk-otel-collector
# On Windows
[Environment]::SetEnvironmentVariable("http_proxy","http://<YOUR_PROXY_SERVER_IP:PORT>","Machine")
[Environment]::SetEnvironmentVariable("https_proxy","http://<YOUR_PROXY_SERVER_IP:PORT>","Machine")
[Environment]::SetEnvironmentVariable("no_proxy","169.254.169.254","Machine")
Stop-Service -Name "splunk-otel-collector"
Start-Service -Name "splunk-otel-collector"
```
 