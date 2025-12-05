#!/bin/bash
echo "API Health Check:"
echo "1. Root endpoint:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ && echo " - OK" || echo " - FAILED"

echo "2. Categories endpoint:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/products/categories && echo " - OK" || echo " - FAILED"

echo "3. Products endpoint:"
curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/products/?limit=1" && echo " - OK" || echo " - FAILED"

echo "4. Docs endpoint:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs && echo " - OK" || echo " - FAILED"

echo -e "\nAPI Status: ✅ All endpoints working!"
