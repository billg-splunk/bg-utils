# Standalone fluentd on Windows
These instructions are based on [similar instructions for linux](https://github.com/signalfx/splunk-otel-collector/blob/main/docs/experimental/using-fluentd-only.md).

## Steps

* [Install fluentd](https://www.fluentd.org/download)
  * MSI or other method should work. MSI method tested here.
* Install the Splunk hec plugin
  * On Windows this is done with ```c:\opt\td-agent\bin\td-agent-gem.bat install fluent-plugin-splunk-hec```
* Add the following to ```c:\opt\td-agent\etc\td-agent\td-agent.conf```
  * The source section is a simple example; you can replace it with other sources
  * The label section is what is sending data to Splunk Observability Cloud
  * Replace **REPLACEME_REALM** and **REPLACEME_TOKEN** with your values for Splunk Observability Cloud
```
<source>
  @id log-test
  @type tail
  @label @SPLUNK
  path C:/log-test.log
  pos_file "#{ENV['TD_AGENT_TOPDIR']}/var/log/td-agent/log-test.log.pos"
  tag log-test
  <parse>
    @type csv
    keys host.name,headline
  </parse>
</source>

<label @SPLUNK>
  <match **>
    @type splunk_hec
    hec_host "ingest.REPLACEME_REALM.signalfx.com
    hec_port 443
    hec_token "REPLACEME_TOKEN"
    data_type event
    source ${tag}
    sourcetype _json
    <buffer>
      @type memory
      total_limit_size 600m
      chunk_limit_size 1m
      chunk_limit_records 100000
      flush_interval 5s
      flush_thread_count 1
      overflow_action block
      retry_max_times 3
    </buffer>
  </match>
</label>

<system>
  log_level info
</system>
```
* You can test this config by sending the following
```
echo %COMPUTERNAME%,"Here is sample text, sir...">>c:\log-test.log
```
* If there are any issues you can check fluentd's log at ```C:\opt\td-agent\td-agent.log```