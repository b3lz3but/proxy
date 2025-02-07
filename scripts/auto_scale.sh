#!/bin/bash
echo "Auto-scaling proxies..."
curl -X POST http://localhost:5000/api/v1/autoscale -H "Content-Type: application/json" -d '{"instances": 3}'
