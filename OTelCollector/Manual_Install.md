# Manual Install

Here is a supplement to the Splunk documentation on a simple install of the OTel Collector for debian on amd.

This example is provided as-is.

Note this example is using version 0.93.0 and should be updated to your specific version.

## Script

```bash
# Download the debian install
wget https://github.com/signalfx/splunk-otel-collector/releases/download/v0.93.0/splunk-otel-collector_0.93.0_amd64.deb

# Install it
sudo dpkg -i splunk-otel-collector_0.93.0_amd64.deb

# Copy the example config file to create the config file
sudo cp /etc/otel/collector/splunk-otel-collector.conf.example /etc/otel/collector/splunk-otel-collector.conf

# Set the token and realms
export REALM=us1
export ACCESS_TOKEN=XXX

sudo sed -i -e "s/12345/$ACCESS_TOKEN/g" /etc/otel/collector/splunk-otel-collector.conf
sudo sed -i -e "s/us0/$REALM/g" /etc/otel/collector/splunk-otel-collector.conf

# Start the collector
sudo systemctl start splunk-otel-collector.service
```