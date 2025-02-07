import os
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import logging
from flask_cors import CORS
from threading import Thread
from kubernetes import client, config
import uuid

app = Flask(__name__)
CORS(app)

LOG_FILE = "logs/proxy_usage.log"


@app.route("/analytics", methods=["GET"])
def view_analytics():
    try:
        df = pd.read_csv(
            LOG_FILE,
            names=["CPU (%)", "Memory (%)", "Data Sent (MB)", "Data Received (MB)"],
        )
        downsample_frac = float(request.args.get("downsample", 0.1))
        if downsample_frac < 1.0:
            df = df.sample(frac=downsample_frac)  # Downsample the data
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
def auto_scale():
    data = request.get_json()
    instances = data.get("instances", "1")
    if not instances.isdigit() or int(instances) < 1:
        return jsonify(
            {"error": "Number of instances must be a positive integer."}
        ), 400
    num_instances = int(instances)

    config.load_kube_config()
    v1 = client.CoreV1Api()
    pod_manifests = []
    for _ in range(num_instances):
        pod_manifest = {
            "apiVersion": "v1",
            "metadata": {
                "name": f"proxy-pod-{uuid.uuid4().hex[:8]}-{int(time.time())}"
            },
            "spec": {"containers": [{"name": "proxy", "image": "squid"}]},
        }
        pod_manifests.append(pod_manifest)

    for pod_manifest in pod_manifests:
        v1.create_namespaced_pod(namespace="default", body=pod_manifest)

    return jsonify({"message": f"Deployed {num_instances} proxy instances."})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Starting Enterprise Proxy Manager v4.0...")
    print("🚀 Starting Enterprise Proxy Manager v4.0...")
    debug_mode = True  # Set the debug mode to True or False as needed
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
