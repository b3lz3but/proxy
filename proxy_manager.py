import os
import time
import uuid
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from kubernetes import client, config
from functools import wraps

# Import pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)
LOG_FILE = "logs/proxy_usage.log"

# Configuration using environment variables
KUBERNETES_NAMESPACE = os.environ.get("KUBERNETES_NAMESPACE", "default")
PROXY_IMAGE = os.environ.get("PROXY_IMAGE", "squid")
API_USERNAME = os.environ.get("API_USERNAME", "admin")
API_PASSWORD = os.environ.get("API_PASSWORD", "password")


# Authentication decorator
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not (
            auth.username == API_USERNAME and auth.password == API_PASSWORD
        ):
            return jsonify({"error": "Authentication required"}), 401
        return func(*args, **kwargs)

    return wrapper


@app.route("/analytics", methods=["GET"])
def view_analytics():
    try:
        df = pd.read_csv(
            LOG_FILE,
            names=["CPU (%)", "Memory (%)", "Data Sent (MB)", "Data Received (MB)"],
        )
        downsample_frac = float(request.args.get("downsample", 0.1))
        df = df.sample(frac=downsample_frac)
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["CPU (%)"], label="CPU (%)")
        plt.plot(df.index, df["Memory (%)"], label="Memory (%)")
        plt.plot(df.index, df["Data Sent (MB)"], label="Data Sent (MB)")
        plt.plot(df.index, df["Data Received (MB)"], label="Data Received (MB)")
        plt.savefig("logs/proxy_usage.png", format="png")
        return jsonify({"message": "Analytics generated: logs/proxy_usage.png"})
    except FileNotFoundError:
        return jsonify({"error": "Log file not found."}), 404
    except pd.errors.EmptyDataError:
        return jsonify({"error": "Log file is empty."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/autoscale", methods=["POST"])
@authenticate  # Apply authentication to this endpoint
def autoscale():
    data = request.get_json()
    instances = data.get("instances", "1")
    if not instances.isdigit() or int(instances) < 1:
        return jsonify(
            {"error": "Number of instances must be a positive integer."}
        ), 400
    num_instances = int(instances)
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
    except config.ConfigException as e:
        return jsonify({"error": f"Kubernetes configuration error: {str(e)}"}), 500

    pod_manifests = []
    for _ in range(num_instances):
        pod_manifest = {
            "apiVersion": "v1",
            "metadata": {
                "name": f"proxy-pod-{uuid.uuid4().hex[:8]}-{int(time.time())}"
            },
            "spec": {"containers": [{"name": "proxy", "image": PROXY_IMAGE}]},
        }
        pod_manifests.append(pod_manifest)

    for pod_manifest in pod_manifests:
        try:
            v1.create_namespaced_pod(namespace=KUBERNETES_NAMESPACE, body=pod_manifest)
        except client.rest.ApiException as e:
            if e.status == 409:
                return jsonify({"error": f"Pod already exists: {e.reason}"}), 409
            else:
                return jsonify({"error": f"Failed to create pod: {e.reason}"}), 500

    return jsonify({"message": f"Deployed {num_instances} proxy instances."})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Starting Enterprise Proxy Manager v4.0...")
    print("🚀 Starting Enterprise Proxy Manager v4.0...")
    debug_mode = True
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
