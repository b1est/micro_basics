docker build -f docker/FacadeServiceDockerfile -t facade-service:1.0 .
docker build -f docker/LoggingServiceDockerfile -t logging-service:1.0 .
docker build -f docker/MessagesServiceDockerfile -t messages-service:1.0 .
docker compose -f docker/docker-compose.yaml -p micro_hazelcast up -d
docker compose -p micro_hazelcast ps
pause