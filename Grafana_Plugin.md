# Grafana Plugin

These are the instructions to get Grafana running with the Signalfx plugin.

This example uses Docker is meant to be for demonstration purposes.

## Preparation

```
cd ~
mkdir grafana
cd grafana
git clone https://github.com/signalfx/grafana-signalfx-datasource.git
mkdir plugins
cp -r grafana-signalfx-datasource/dist ./plugins
mv ./plugins/dist ./plugins/signalfx-datasource
echo "[plugins]" > custom.ini
echo "enable_alpha = true" >> custom.ini
echo "app_tls_skip_verify_insecure = true" >> custom.ini
echo "allow_loading_unsigned_plugins = signalfx-datasource" >> custom.ini
echo "plugin_admin_enabled = true" >> custom.ini
echo "plugin_admin_external_manage_enabled = true" >> custom.ini
echo "docker run -d -p 3000:3000 \\" > start_grafana.sh
echo "-v ${PWD}/plugins:/var/lib/grafana/plugins \\" >> start_grafana.sh
echo "--mount type=bind,source=${PWD}/custom.ini,target=/etc/grafana/grafana.ini \\" >> start_grafana.sh
echo "grafana/grafana-oss" >> start_grafana.sh
chmod +x start_grafana.sh
```

## Running it

```
./start_grafana.sh
```

## Configuring

* Navigate to http://localhost:3000
* Login as **admin**/**admin**
* Skip changing the password
* Go to **Settings** / **Data sources**
* Click **Add data source**
* Search for **SignalFx** and click **Select**
* Give it
  * A name
  * Endpoint (i.e. https://stream.us1.signalfx.com)
  * Access (Only browser worked for me)
  * Token
* And save and test

## Using

* Create a new dashboard
* Add a new panel
* Select SignalFx as the datasource
* Enter your signalflow
  * Example: ```data('cpu.utilization').publish(label='A')```
* Click **Apply**