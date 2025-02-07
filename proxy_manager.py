import os
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import uuid
from flask_cors import CORS
from threading import Thread
from kubernetes import client, config

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
        df = df.sample(frac=0.1)  # Downsample the data to 10%
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
    try:
        num_instances = int(data.get("instances", 1))
        if num_instances < 1:
            raise ValueError("Number of instances must be a positive integer.")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    config.load_kube_config()
    v1 = client.CoreV1Api()
    for _ in range(num_instances):
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": f"proxy-pod-{time.time()}"},
            "spec": {"containers": [{"name": "proxy", "image": "squid"}]},
        }
        v1.create_namespaced_pod(namespace="default", body=pod_manifest)

    return jsonify({"message": f"Deployed {num_instances} proxy instances."})


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]
    print("🚀 Starting Enterprise Proxy Manager v4.0...")
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
