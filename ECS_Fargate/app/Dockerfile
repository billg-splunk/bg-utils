FROM tomcat:9.0-jre8-alpine

RUN apk add curl

# Create a work directory to copy the agent artifacts
RUN mkdir -p /opt/splunk

# Download and extract agent artifacts to the work directory
RUN curl -L0 https://github.com/signalfx/splunk-otel-java/releases/latest/download/splunk-otel-javaagent.jar \
-o /opt/splunk/splunk-otel-javaagent.jar

WORKDIR /usr/local/tomcat/webapps

EXPOSE 8080

CMD ["/usr/local/tomcat/bin/catalina.sh", "run"]