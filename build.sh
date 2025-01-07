#!/bin/bash

# Step 1: Navigate to the frontend directory
cd frontend

# Step 2: Create a Docker network
# Create network only if it doesn't exist
docker network inspect micro_network >/dev/null 2>&1 || docker network create micro_network

# Step 3: Build all the images
docker-compose -f docker-compose.yml build

# Step 4: Launch the microservices environment
docker-compose -f docker-compose.yml up -d

# Step 5: Prepare each microservice MySQL database
for service in corder-service cproduct-service cuser-service
do
  docker exec -it "$service" flask db init
  docker exec -it "$service" flask db migrate
  docker exec -it "$service" flask db upgrade
done

# Step 6: Populate product-db
curl -i -d "name=prod1&slug=prod1&image=product1.jpg&price=100" -X POST localhost:5002/api/product/create
curl -i -d "name=prod2&slug=prod2&image=product2.jpg&price=200" -X POST localhost:5002/api/product/create

echo "Environment set up successfully. You can now register and log in at http://localhost:5000."