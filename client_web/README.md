# Web client application
Using Python Flask to build a simple web application as clients of the SOA basaed system

## search engine
The users are unaware of where to locate the service provider and thus don't directly access the services. Therefore, we offer a search engine allowing users to search for a service bu name or key word. The backend of the search engine is the service registry which maintains a list of available services and processes search request.

1. The Web client and the registry server are developed at the same time, thus, we need to use postman as a test tool to test Web client.
2. When the registry server finished develop and deploy, we should be able to do integrate test.
Subject line (try to keep under 50 characters)
