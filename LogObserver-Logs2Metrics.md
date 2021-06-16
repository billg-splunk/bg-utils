# Log Observer - Logs to Metrics

In this example we will walk through installing the Splunk OTel Connector (OTel Collector distro) with fluentd to send logs. We will then convert log entries to metrics.

Note thet this example is not meant to reflect best practices. For example we may want to do the field extraction at the fluentd level; that would make the process simpler when creating the rule. Instead the example shows configuring an extraction both in fluentd and then further in Splunk Observability Cloud to show how multiple scenarios can be haneld.

## Objective

We will simulate logs (at location ```/home/ubuntu/logstometrics.txt``` in the format:
```
Tue Jun 15 19:36:53 EDT 2021 : 95 inserts, 14 updates, and 100 deletes
```
We will then
* Configure **Splunk Observability Connector (specifically fluentD)** to parse out the timestamp and the log details
* Configure **Splunk Observability Cloud** to parse out inserts, updates, and deletes as individual metrics

## Configuration

### Installing the agent

* Go to the menu and click  **Data Setup**
* Choose **Linux**
* Click **Add Connection**
* Choose your access token, Mode = **Agent**, and Log Collection = **Yes**
*  Copy and run the installer

### Configuring a logging script

For this example we will run a script that generates log events each second.

Edit a file, ```/home/ubuntu/createlogs.sh```, and add the following:
```
echo "Press [CTRL+C] to stop..."
while :
do
  x=$(( ($RANDOM % 100) + 1))
  y=$(( ($RANDOM % 100) + 1))
  z=$(( ($RANDOM % 100) + 1))
  echo "$(date) : $x inserts, $y updates, and $z deletes" >> logstometrics.txt
  sleep 1
done
```
Later we will run this script

### Configure Splunk Observability Connector (fluentD)

Create a new file, ```/etc/otel/collector/fluentd/conf.d/logstometrics.conf```, and add the following (adjust the path as necessary):
```
<source>
  @label @SPLUNK
  @type tail
  tag logstometrics.example
  path /home/ubuntu/logstometrics.txt
  pos_file /var/log/td-agent/logstometrics.txt.pos
  <parse>
    @type regexp
    expression ^(?<timestamp>.*)\s:\s(?<details>.*)$
  </parse>
</source>
```

To make it consistent with the other fluentd files:
```
sudo chown td-agent:td-agent /etc/otel/collector/fluentd/conf.d/logstometrics.conf
sudo chmod 755 /etc/otel/collector/fluentd/conf.d/logstometrics.conf
```

It's importand that the td-agent user can access where the log file exists, so change the permissions if needed. You can test with:
```
sudo -u td-agent test -r /home/ubuntu/logstometrics.txt || echo "fail"
```
and confirm this doesn't return "fail".

To restart the fluentd agent: ```sudo systemctl restart td-agent```

## Running the script

Run the script by running:
```
/home/ubuntu/createlogs.sh
```

You should see logs coming from Log Observer. If you see a lot of logs you can:
* Add a filter on ```fluent.tag=logstometrics.example```
* Click **settings** and add the **details** field

You now should only see log entries with ```# inserts, # updates, and # deletes```

## Configuring Log Observer
In the next two sections we will:
* **Extract Fields**: Take the **details** field and split it into separate **inserts**, **updates**, and **deletes** fields
* **Save as Metric**: Convert these new fields into metrics

In both sections it is important we filter the logs on ```fluent.tag=logstometrics.example``` (per above) or these steps would be analyzed on every single log.

### Extracting fields
* Click on one of the log entries, and then on the **details** fields on the right side
* Select **Extract field**
* Choose **Regex Extraction**
* Highlight the first number and click **Extract field**. Set the field name to **inserts**.
* Repeat this for the 2nd number (**updates**) and 3rd number (**deletes**)
* ***Optional***: You can edit the regex if you wish to improve upon the auto-generated one
* Preview the table at the bottom to verify your extraction looks correct, and click **Next**
* Give it a name, like ```Extract Inserts/Updates/Deletes for logstometrics.example``` and click **Save**.
* Go back to **Log Observer** and filter on ```fluent.tag=logstometrics.example```
* Click **seetings** and add the **inserts**, **updates**, and **deletes** fields and verify you can see each value

### Saving log entries as metrics

Now we will convert these logs to metrics:
* Click the three dots at the top-right and select **Save as Metric**
* Set the search to **Sum inserts**. (You will need to unselect the group by severity.)
* Notice each time series represents 30 seconds. You can change the time filter to see what it looks like at different rollups. Click **Next**.
* Pick a token and click **Next**
* Call your metric ```counter.logstometrics.example.inserts```. You can name the rule the same thing. Click **Save**.

To confirm it is coming in:
* Expand **Metricization Rules**
* Click on the rule you just made
* Click **open metric in chart builder**
