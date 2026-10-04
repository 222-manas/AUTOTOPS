import os
import time
import logging

from flask import Flask, Response, g, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("demo-api")

app = Flask(__name__)

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds", "Request latency in seconds", ["path"]
)

leaked = []


def route_name():
    return request.url_rule.rule if request.url_rule else "unmatched"


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def record_metrics(resp):
    if request.path != "/metrics":
        REQUESTS.labels(request.method, route_name(), resp.status_code).inc()
        LATENCY.labels(route_name()).observe(time.time() - g.start)
    return resp


@app.route("/")
def home():
    log.info("home page visited")
    return {"service": "demo-api", "message": "ok"}


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/error")
def error():
    log.error("simulated HTTP 500 error")
    return {"error": "simulated failure"}, 500


@app.route("/crash")
def crash():
    log.critical("crash requested, killing the process now")
    os._exit(1)


@app.route("/leak")
def leak():
    leaked.append(b"x" * (30 * 1024 * 1024))
    log.warning("leaked 30MB, total = %d MB", len(leaked) * 30)
    return {"leaked_mb": len(leaked) * 30}


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)