# Change Hostname of OTel Collector

## Add the following processor

```
processors:
  resource/change_name:
    attributes:
      - action: upsert
        value: test_log
        key: host.name
```

## Add the processor to all the pipelines

Example for metrics:

```
service:
  pipelines:
    metrics:
      receivers: [hostmetrics, otlp, signalfx, smartagent/signalfx-forwarder, smartagent/tail]
      processors: [memory_limiter, batch, resourcedetection, resource/change_name]
      exporters: [signalfx]
      # Use instead when sending to gateway
      #exporters: [otlp]