# Splunk Metric Concepts

**Work in progress; may be inaccurate!**

This table lays out the different constructs and how they are used inside the product.

**MetricSets** are categories of metrics about traces and spans you can use for real-time monitoring and high-cardinality troubleshooting. MetricSets are specific to Splunk APM, but are similar to metrics and metric time-series for Infrastructure Monitoring the application uses to populate charts and generate alerts.

**Stadard Metric** = Not a Monitoring MetricSet or Troubleshooting MetricSet.

|&nbsp;|Standard Metric|Monitoring Metricset|Troubleshooting Metricset|
|--|--|--|--|
|Available in Dashboards/Charts|Yes|Yes|Yes|
|Can breakdown in Troubleshooting View|No|No|Yes|
|Can be used in Tag Spotlight|No|No|Yes|
|Can be used with detectors|No|Yes|No|
|Maximum Number (Approximately)|Effectively Unlimited|100-150K|Effectively Unlimited|
|Data Retention<br>(1 min roll-up, Std. Lic)|13 months|13 months|13 months|
|Data Retention<br>(1 min roll-up, Ent. Lic)|13 months|13 months|13 months|
|Data Retention<br>(1 sec native, Std. Lic)|8 days|8 days|8 days|
|Data Retention<br>(1 sec native, Ent. Lic)|3 months|8 days|3 months|
