# Basic microservices architecture

This microservices architecture consists of three services:

* facade-service: receives HTTP POST/GET requests from clients
* logging-service: stores all messages received in memory and can return them
* messages-service: currently serves as a placeholder and returns a static message

## System Functionality
Clients interact with the facade-service through HTTP POST and GET requests. Clients can be tools such as curl, Postman, a browser in Dev mode, and others.

### HTTP POST Request Flow
* The client sends a POST request to the facade-service with a text message - msg.
* Upon receiving the message, the facade-service generates a unique identifier UUID for it.
* The pair {UUID, msg} is sent to the logging-service as a POST message using a programmatic REST/HTTP-client.
* The logging-service receives the message, stores it along with the identifier in a local hash table (identifier as the key), and outputs the received message to its console.

### HTTP GET Request Flow

* The client sends a GET request to the facade-service.
* Upon receiving the request, the facade-service generates GET requests to both the logging-service and messages-service using a programmatic REST/HTTP-client.
* The logging-service returns all messages (without keys) stored in the hash table as a string.
* The messages-service returns a static message, such as "not implemented yet."
* The facade-service concatenates the text of both responses and returns it to the client.