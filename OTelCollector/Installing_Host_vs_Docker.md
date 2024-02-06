# Installing Host vs. Docker

Here are a few considerations when deciding to deploy the otel collector in a docker container instead of on the host. For the collector to be fully effective it needs access to the host network, filesystem, etc.

NOTE: This is not relevant for kubernetes, which has a different deployment pattern.

- If using a container...
  - Do you have tools to monitor the service?
    - Systemd or Windows Services generally handles this on the host and can handle crashes
    - With docker you will likely need to use the `restart` option
  - How do you do log management?
    - Docker = container logs
    - Host = journald/event logs
  - To monitor the host, you need to mount host FS
    - Is there a concern trusting the docker base image?
  - Some receivers, like the SmartAgent forwarder, need to listen on the host network
    - Is there a concern running containers with host networking?
  - Resources are limited to what the docker engine is configured to use
    - Shouldn't be an issue but something to consider