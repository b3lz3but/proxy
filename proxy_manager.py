import os
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
from kubernetes import client, config

app = Flask(__name__)
CORS(app)

LOG_FILE = "logs/proxy_usage.log"

@app.route("/analytics", methods=["GET"])
def view_analytics():
    df = pd.read_csv(LOG_FILE, names=["CPU (%)", "Memory (%)", "Data Sent (MB)", "Data Received (MB)"])
    df.plot(kind="line", figsize=(10, 5))
    plt.savefig("logs/proxy_usage.png")
    return jsonify({"message": "Analytics generated: logs/proxy_usage.png"})

@app.route("/autoscale", methods=["POST"])
def auto_scale():
    data = request.get_json()
    num_instances = data.get("instances", 1)

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
    print("🚀 Starting Enterprise Proxy Manager v4.0...")
    app.run(host="0.0.0.0", port=5000, debug=True)
