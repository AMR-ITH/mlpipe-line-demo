#!/bin/bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 116981799876.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest image
docker pull 116981799876.dkr.ecr.us-east-1.amazonaws.com/yamlguru/repo:latest

# Check if the container 'campusx-app' is running
if [ "$(docker ps -q -f name=campusx-app)" ]; then
    # Stop the running container
    docker stop campusx-app
fi

# Check if the container 'campusx-app' exists (stopped or running)
if [ "$(docker ps -aq -f name=campusx-app)" ]; then
    # Remove the container if it exists
    docker rm campusx-app
fi

# Run a new container
docker run -p 80:5000 -e DAGSHUB_PAT=e691c7193ab61dc9678e31c6b92ded8a65f80697 --name campusx-app 116981799876.dkr.ecr.us-east-1.amazonaws.com/yamlguru/repo:latest