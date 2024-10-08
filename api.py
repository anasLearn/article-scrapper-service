import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

from yle import yle_scrap_one_article, yle_scrap_all_feeds

load_dotenv()

HOST = os.environ.get("HOST", default="localhost")
PORT = int(os.environ.get("PORT", default=5020))

app = FastAPI()
YLE_SOURCE = "yle"


class ArticleURL(BaseModel):
    url: str


@app.get("/ping")
async def ping():
    """
    GET /ping

    Health check endpoint to verify that the article scraper service is alive.

    Returns:
        str: A confirmation message indicating the service is alive.
    """
    return "Hello, Article Scraper Service is alive"


@app.get("/get_new_articles", response_model=Dict[str, Dict[str, List[Dict[str, str]]]])
def get_new_articles(
    source: Optional[str] = Query(None, description="Source to filter articles by")
):
    articles = {}
    if source:
        if source.lower() == YLE_SOURCE:
            articles = {"yle": yle_scrap_all_feeds()}

    return articles


@app.post("/scrap_article", response_model=dict)
def scrap_article(
    article: ArticleURL,
    source: Optional[str] = Query(None, description="Source to filter articles by"),
):
    # TODO: Improve this process of waiting before scraping to avoid overwhelming the scrapped website
    time.sleep(0.5)

    try:
        scraped_data = {}
        if source:
            if source.lower() == YLE_SOURCE:
                scraped_data = yle_scrap_one_article(article.url)

        return scraped_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api:app", host=HOST, port=PORT, reload=True)
