#neww_scraper
import os
import json
from typing import List, Dict
from datetime import datetime, timezone
from utils.logger import Logger
import requests
from bs4 import BeautifulSoup

logger = Logger("logs")

SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(SAVE_PATH, exist_ok=True)

def fetch_yahoo_news(ticker: str, limit: int = 5) -> List[Dict[str, str]]:
    """Primary source of news for a ticker."""
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch"
    news_list = []

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("li.js-stream-content")[:limit]

        for item in items:
            headline_tag = item.select_one("h3")
            headline = headline_tag.get_text(strip=True) if headline_tag else "N/A"

            link_tag = item.select_one("a")
            link = f"https://finance.yahoo.com{link_tag['href']}" if link_tag else ""

            source_tag = item.select_one("span")
            source = source_tag.get_text(strip=True) if source_tag else ""

            news_list.append({
                "headline": headline,
                "source": source,
                "url": link,
                "published_at": datetime.now(timezone.utc).isoformat()
            })
        return news_list

    except Exception as e:
        logger.warning(f"Failed to fetch news for {ticker}: {e}")
        return []

def save_news_to_json(ticker: str, news: List[Dict[str, str]]) -> str:
    filename = os.path.join(SAVE_PATH, f"{ticker}_news.json")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(news, f, indent=2)
        logger.info(f"Saved news for {ticker} -> {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to save news for {ticker}: {e}")
        return ""
