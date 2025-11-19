from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

REQUEST_COUNT = Counter("request_count", "API Request Count", ["path", "method"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency", ["path", "method"])
ERROR_COUNT = Counter("error_count", "API Errors")

metrics_router = APIRouter()

@metrics_router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
