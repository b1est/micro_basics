docker build -f FacadeServiceDockerfile -t facade-service:1.0 .
docker build -f LoggingServiceDockerfile -t logging-service:1.0 .
docker build -f MessagesServiceDockerfile -t messages-service:1.0 .