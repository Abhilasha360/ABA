import os
import aiohttp

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
BASE_URL = "https://newsapi.org/v2"

class NewsClient:
    async def top_headlines(self):
        return await self._fetch("top-headlines", {"country": "us"})

    async def by_category(self, category):
        return await self._fetch("top-headlines", {"country": "us", "category": category})

    async def search(self, q):
        return await self._fetch("everything", {"q": q})

    async def _fetch(self, endpoint, params):
        headers = {"Authorization": NEWSAPI_KEY}
        url = f"{BASE_URL}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                return await resp.json()
