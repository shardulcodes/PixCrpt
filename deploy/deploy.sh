#!/bin/bash
set -e

APP_NAME="pixcrypt"
IMAGE="${DOCKER_HUB_USERNAME:-yourdockerhubusername}/pixcrypt:latest"

echo "Pulling latest image from Docker Hub..."
docker pull $IMAGE

echo "Stopping old container (if running)..."
docker stop $APP_NAME || true
docker rm $APP_NAME || true

echo "Starting new container..."
docker run -d \
  --name $APP_NAME \
  -p 5000:5000 \
  --restart=always \
  $IMAGE

echo "Deployment complete! Container is running."
docker ps | grep $APP_NAME
