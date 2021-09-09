# Azure App Services Example

## Introduction

This example walks through setting up an example app deployed in Azure App Service and using the Splunk SignalFx extension.

These steps are based on the instructions found in the following resources:
* MS Azure app walkthrough to host a web app with App Service: https://docs.microsoft.com/en-us/learn/modules/host-a-web-app-with-azure-app-service/
* Splunk Documentation on instrumenting an Azure App Service: https://docs.signalfx.com/en/latest/apm/apm-instrument/apm-azure-app.html

## Steps to create the app

* Create an App Service in Azure
  * In Azure, click **Create a Resource**, select **Web** and click **Create** next to **Web App**. (Search for **Web app** if you don't find it.)
  *  Select a subscription
  *  Select a resource group (or create a new one)
  *  Publish as code
  *  Select **.Net Core 3.1 (LTS)** as the runtime stack
  *  Select a region (or keep default)
  *  Click **Next**
  *  Keep default linux plan
  *  Select F1 (Free tier) for the Sku and Size
     *  NOTE: It is free for an hour/day as of this writing. Be aware of any costs incurred following these instructions
  * Click **Review + Create**
  * Once the app is up, click on the URL to confirm it is working
* Create the Bike App
  * Open up a cloud shell. This may take some time and require you to allocate storage for the shell.
  * Run the following commands in the shell
  ```
  wget -q -O - https://dot.net/v1/dotnet-install.sh | bash -s -- --version 3.1.102
  export PATH="~/.dotnet:$PATH"
  echo "export PATH=~/.dotnet:\$PATH" >> ~/.bashrc
  ```
  ```
  dotnet new mvc --name BestBikeApp
  ```
  ```
  cd BestBikeApp
  dotnet run
  ```
  * This should confirm your app is running. Control-C to stop it.
* Deploy the app
  * Run the following commands to package up your app and deploy it.
  ```
  cd ~/BestBikeApp
  dotnet publish -o pub
  cd pub
  zip -r site.zip *
  ```
  ```
  az webapp deployment source config-zip \
  --src site.zip \
  --resource-group <your-resource-group> \
  --name <your-app-name>
  ```
  * Test that your app has been updated. You should see **BestBikeApp** a the top

## Steps to add Splunk APM
* In Splunk Observability Cloud, note down your
  * Realm (typically **us1** in the US)
  * Access Token
* In Azure, go to your App Service
* On the left side, under **Development Tools**, click **Extensions**
* Click **Add** and select **SignalFx .NET Tracing [PreRelease]** and
* Confirm from the extensions page that the extension was deployed successfully
* On the left side, under **Settings**, click **Configuration**
* Add the following application settings
  * SIGNALFX_SERVICE_NAME: **BikeApp**
  * SIGNALFX_ACCESS_TOKEN: **(Access Token)**
  * SIGNALFX_ENDPOINT_URL: **http://ingest.(Realm).signalfx.com/v2/trace**
    * NOTE: You can also set this to an OTel Collector if you have one deployed
* Click **SAVE**, which should restart the application.
  
## View in Splunk APM
* Click around in the app to ensure traces are created
* In Splunk APM you will see this under the "unknown" or "All Environments" environment
  * We can set the SIGNALFX_ENV setting to change this, or set this in an OTel Collector 