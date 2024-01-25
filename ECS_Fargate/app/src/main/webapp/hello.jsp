<!DOCTYPE html>
<%@ page import="org.apache.log4j.Logger" %>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello World</title>
</head>
<body>
<h1>Hello World</h1>
<%
Logger log = Logger.getLogger("simple_jsp.class");
log.debug("Show DEBUG message");
log.info("Show INFO message");
log.warn("Show WARN message");
log.error("Show ERROR message");
log.fatal("Show FATAL message");
%>
</body>
</html>