#!/bin/bash

echo "=== E-Commerce API Docker Manager ==="
echo ""

# Kill anything on port 8000
echo "Stopping anything on port 8000..."
sudo fuser -k 8000/tcp 2>/dev/null || true
pkill -f uvicorn 2>/dev/null || true

# Stop and remove any existing container
echo "Cleaning old containers..."
docker stop ecommerce-api 2>/dev/null || true
docker rm ecommerce-api 2>/dev/null || true

# Build if needed
if [ "$1" = "build" ]; then
    echo "Building Docker image..."
    docker build -t ecommerce-api .
fi

# Run the container
echo "Starting container..."
docker run -d \
    -p 8000:8000 \
    --name ecommerce-api \
    -v $(pwd)/data:/app/data \
    ecommerce-api

echo ""
echo "Waiting for API to start..."
sleep 5

# Test it
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API is running!"
    echo ""
    echo "📢 Access your API at:"
    echo "   Main URL: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo "   Health:   http://localhost:8000/health"
    echo ""
    echo "📋 Quick test:"
    curl -s http://localhost:8000/api/products | python3 -m json.tool | head -20
else
    echo "❌ API failed to start"
    echo "Checking logs..."
    docker logs ecommerce-api
fi
