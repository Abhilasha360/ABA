from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="News Aggregator API",
    version="1.0.0",
    description="Fetch trending news using categories & keywords"
)

# ---------- Pydantic Models ----------
class Article(BaseModel):
    title: str
    description: str | None
    url: str
    source: str | None

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: list[Article]

API_KEY = "YOUR_NEWSAPI_KEY"
BASE_URL = "https://newsapi.org/v2"


# ---------- Endpoints ----------

@app.get("/top-headlines", response_model=NewsResponse)
def get_top_headlines():
    url = f"{BASE_URL}/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url).json()

    if response.get("status") != "ok":
        raise HTTPException(400, "API error")

    return response


@app.get("/category", response_model=NewsResponse)
def get_news_by_category(name: str):
    url = f"{BASE_URL}/top-headlines?country=us&category={name}&apiKey={API_KEY}"
    response = requests.get(url).json()

    if response.get("status") != "ok":
        raise HTTPException(400, "Invalid category")

    return response


@app.get("/search", response_model=NewsResponse)
def search_news(query: str):
    url = f"{BASE_URL}/everything?q={query}&apiKey={API_KEY}"
    response = requests.get(url).json()

    if response.get("status") != "ok":
        raise HTTPException(400, "Search failed")

    return response
