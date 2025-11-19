from fastapi import FastAPI, HTTPException, Request, Query
import time
from .news_client import NewsClient
from .metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT

app = FastAPI(title="News Aggregator API")
news = NewsClient()

@app.middleware("http")
async def monitor(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        return response
    except:
        ERROR_COUNT.inc()
        raise
    finally:
        duration = time.time() - start
        REQUEST_COUNT.labels(path=request.url.path, method=request.method).inc()
        REQUEST_LATENCY.labels(path=request.url.path, method=request.method).observe(duration)

@app.get("/top-headlines")
async def top_headlines():
    return await news.top_headlines()

@app.get("/category")
async def cat(name: str):
    return await news.by_category(name)

@app.get("/search")
async def search(query: str):
    return await news.search(query)

from .metrics import metrics_router
app.include_router(metrics_router)
