from fastapi import FastAPI
import redis
import time
import logging
import os
from kubernetes import client, config

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Redis connection for storing active proxies
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
redis_client = redis.StrictRedis(connection_pool=pool)


# Store active proxy in Redis
def store_proxy(port, ip):
    redis_client.set(f"proxy:{port}", ip)
    logging.info(f"Stored proxy {ip} on port {port}")


# Retrieve active proxies
def list_proxies():
    proxies = {key: redis_client.get(key) for key in redis_client.keys("proxy:*")}
    logging.info(f"Retrieved proxies: {proxies}")
    return proxies


# API to get active proxies
@app.get("/api/v1/proxies")
async def get_proxies():
    return {"active_proxies": list_proxies()}


# AI-Based Proxy Auto-Scaling
@app.post("/api/v1/autoscale")
async def auto_scale(instances: int):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    pod_manifests = []
    for _ in range(instances):
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": f"proxy-pod-{time.time()}"},
            "spec": {"containers": [{"name": "proxy", "image": "squid"}]},
        }
        pod_manifests.append(pod_manifest)

    for pod_manifest in pod_manifests:
        try:
            v1.create_namespaced_pod(namespace="default", body=pod_manifest)
            logging.info(f"Deployed pod: {pod_manifest['metadata']['name']}")
        except client.rest.ApiException as e:
            logging.error(f"Failed to create pod: {e.reason}")
            return {"error": f"Failed to create pod: {e.reason}"}, 500

    return {"message": f"Deployed {instances} proxy instances."}


if __name__ == "__main__":
    logging.info("Starting Enterprise Proxy API...")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
