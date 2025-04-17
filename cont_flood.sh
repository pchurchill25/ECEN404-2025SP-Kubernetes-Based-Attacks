#!/bin/bash

trap "echo 'Stopping script...'; exit" SIGINT SIGTERM

# Step 1: Build a lightweight image with a sparse file (100GB)
docker build -t spam_container_image - <<< "FROM alpine:latest
RUN fallocate -l 100G /largefile"
echo "Built custom image: spam_container_image (100GB sparse file)"

count=0
while true; do
    # Step 2: Create containers fast from the prebuilt image
    docker run -d --name spam_container_$count spam_container_image sleep infinity
    echo "Created spam_container_$count (100GB sparse file)"

    # Step 3: Consume CPU power in the background
    (while true; do echo "$((13**99))" > /dev/null; done) &

    count=$((count + 1))
done
