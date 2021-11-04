# Lambda Concepts
NOTE: This is a draft. Feedback welcome.

## Overview
Lambda has 3 constructs (wrappers, layers, and extensions). Below is an explanation of each.

NOTE: In terms of using with Splunk Observability Cloud, start with layers. This explanation leads with wrappers as the concepts build on each other. And some wrappers aren't available as layers

## Lambda Wrapper
Lamda wrappers provide standard functionality so developers are focused on writing business logic rather than dealing with events, telemetry, etc. that can be abstracted.

In the context of Splunk Observability, Lambda wrappers instrument your AWS Lambda functions to send metrics and traces to Splunk Observability Cloud.

Resources:
* [Documentation and Instrumenting](https://docs.splunk.com/Observability/gdi/get-data-in/serverless/aws/signalfx-lambda-wrappers.html)
* [Github](https://github.com/signalfx/lambda-layer-versions)
  * SignalFx wrappers: Java, NodeJS, Python, Ruby, and C#
  * For OTel (currently Java, NodeJS, and Python) the layer is preferred

## Lambda Layer
Lambda layers are archives that contain additional code (e.g. libraries, dependencies, runtimes, etc.).

Splunk provides Lambda layers to automatically instrument AWS Lambda functions to send metrics and traces to Splunk Observability Cloud. It also includes a metrics extension (described below).

Resources:
* [Documentation](https://docs.splunk.com/Observability/gdi/get-data-in/serverless/aws/splunk-otel-lambda-layer.html)
* [Instrumenting](https://docs.splunk.com/Observability/gdi/get-data-in/serverless/aws/otel-lambda-layer/instrument-lambda-functions.html)
* [Github](https://github.com/signalfx/lambda-layer-versions/blob/master/splunk-apm/README.md)
  * OTel Layer supports Java, NodeJS and Python
  * If you are using these languages you should be using the layer if possible

## Lambda Extension
Lambda extensions are shared libraries that run side-by-side with functions inside the same execution environment. Since extensions are running outside the function they are language-agnostic (which is different from wrappers).

Splunk's extension:
* Is written in Golang, which is highly performant
* Offers transparent data collection (since it's outside of the function itself)
* Can influence instrumantation (i.e. by setting language-specific environment variables)

Resources:
* No separate documentation, provided as part of the Lambda Layer
  * Though it can be deployed separately (see Github below)
* [Github](https://github.com/signalfx/splunk-extension-wrapper/tree/main/docs)
* [Blog Post](https://www.splunk.com/en_us/blog/platform/splunk-extensions-for-aws-lambda.html)

