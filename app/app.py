import math
import os
import socket
import time
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

PRODUCTS = [
    {
        "id": 1,
        "name": "DevOps Handbook (2nd Ed)",
        "desc": "How to create world-class agility, reliability, and security in tech.",
        "price": 29.99,
        "icon": "📘"
    },
    {
        "id": 2,
        "name": "Kubernetes in Production",
        "desc": "Master cluster orchestration, Helm charts, and microservices.",
        "price": 44.99,
        "icon": "☸️"
    },
    {
        "id": 3,
        "name": "Docker Deep Dive Edition",
        "desc": "Zero to mastery on containers, networks, and multi-stage builds.",
        "price": 34.99,
        "icon": "🐳"
    },
    {
        "id": 4,
        "name": "Cloud Native Architecture",
        "desc": "Designing high-scale, fault-tolerant distributed cloud systems.",
        "price": 39.99,
        "icon": "☁️"
    },
    {
        "id": 5,
        "name": "Prometheus & Grafana Lab",
        "desc": "Complete observability, alerting, and telemetry dashboards.",
        "price": 27.50,
        "icon": "📊"
    },
    {
        "id": 6,
        "name": "Terraform Infrastructure",
        "desc": "Infrastructure as Code (IaC) with multi-cloud automation.",
        "price": 31.99,
        "icon": "🏗️"
    }
]

@app.route("/")
def home():
    pod_name = os.environ.get("HOSTNAME", socket.gethostname())
    return render_template("index.html", pod_name=pod_name, products=PRODUCTS)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/products")
def products():
    return jsonify({
        "count": len(PRODUCTS),
        "products": PRODUCTS
    })

@app.route("/status")
def status():
    pod_name = os.environ.get("HOSTNAME", socket.gethostname())
    return jsonify({
        "application": "AutoScale",
        "status": "Running",
        "pod_name": pod_name,
        "hostname": socket.gethostname()
    })

@app.route("/heavy")
def heavy():
    iterations = int(request.args.get("iterations", 3000000))
    start_time = time.time()

    val = 0.0
    for i in range(1, iterations):
        val += math.sqrt(i) * math.sin(i)

    elapsed = time.time() - start_time
    pod_name = os.environ.get("HOSTNAME", socket.gethostname())

    return jsonify({
        "message": "CPU intensive calculation complete",
        "pod_name": pod_name,
        "iterations": iterations,
        "elapsed_seconds": round(elapsed, 4)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
