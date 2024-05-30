from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Tuple, Dict
import uvicorn

from yle import yle_scrap_one_article, yle_scrap_all_feeds

app = FastAPI()
YLE_SOURCE = "yle"


class ArticleURL(BaseModel):
    url: str


@app.get("/get_new_articles", response_model=Dict[str, List[Tuple]])
def get_new_articles(source: Optional[str] = Query(None, description="Source to filter articles by")):
    articles = {}
    if source:
        if source.lower() == YLE_SOURCE:
            articles = yle_scrap_all_feeds()

    return articles


@app.post("/scrap_article", response_model=dict)
def scrap_article(
        article: ArticleURL,
        source: Optional[str] = Query(None, description="Source to filter articles by")
):
    try:
        scraped_data = {}
        if source:
            if source.lower() == YLE_SOURCE:
                scraped_data = yle_scrap_one_article(article.url)

        return scraped_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
