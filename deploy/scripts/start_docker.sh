#!/bin/bash
# Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 116981799876.dkr.ecr.us-east-1.amazonaws.com

# Pull the latest image
docker pull 116981799876.dkr.ecr.us-east-1.amazonaws.com/yamlguru/repo:v1.0

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

# Run the new container
docker run -d -p 80:5000 -e DAGSHUB_PAT=a9ccae4d03c5174b543a4167dd282c25cc28c31e --name campusx-app 116981799876.dkr.ecr.us-east-1.amazonaws.com/yamlguru/repo:v1.0
