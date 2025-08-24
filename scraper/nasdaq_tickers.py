#nasdaq_tickers
import sys
import os
import io
import time
import pandas as pd
from scraper.yfinance_scraper import scrape_symbol
from scraper.news_scraper import fetch_yahoo_news  # <- added
from urllib.request import urlopen
from utils.logger import Logger

logger = Logger("logs")

SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")
FILENAME = "nasdaq_listed.csv"
FILEPATH = os.path.join(SAVE_PATH, FILENAME)
MAX_FILE_AGE_DAYS = 3

def scrape_ticker(symbol: str, company_name: str = "") -> dict:
    """Scrape ticker data and attach Yahoo news as primary source."""
    data = scrape_symbol(symbol)
    if not data:
        logger.error(f"No data returned for {symbol}")
        return {}

    # Ensure company info exists
    if "company_info" not in data or not data["company_info"].get("name"):
        data["company_info"] = data.get("company_info", {})
        data["company_info"]["name"] = company_name or symbol

    data["symbol"] = symbol
    data["company_name"] = data["company_info"]["name"]

    # Attach news from news_scraper as primary source
    data["news"] = fetch_yahoo_news(symbol)

    return data


def is_file_old(filepath, max_age_days=MAX_FILE_AGE_DAYS):
    if not os.path.exists(filepath):
        logger.warning(f"Ticker file {filepath} does not exist. Will attempt to fetch.")
        return True

    file_age = time.time() - os.path.getmtime(filepath)
    return file_age > max_age_days * 86400  # seconds in a day


def fetch_nasdaq_listed():
    url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"

    try:
        with urlopen(url) as response:
            lines = response.read().decode('utf-8').splitlines()

        # Skip last line (record count), parse rest
        df = pd.read_csv(io.StringIO('\n'.join(lines[:-1])), sep='|')

        # Filter out test entries
        df = df[df['Test Issue'] == 'N']

        logger.info(f"Fetched {len(df)} NASDAQ-listed tickers.")
        return df

    except Exception as e:
        logger.error(f"Error fetching NASDAQ data: {e}")
        return pd.DataFrame()


def save_to_csv(df, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    logger.info(f"Saved: {filepath}")


def get_nasdaq_listed():
    if is_file_old(FILEPATH):
        logger.warning(f"Ticker list is missing or stale, refreshing...")
        df = fetch_nasdaq_listed()
        if not df.empty:
            save_to_csv(df, FILEPATH)
        else:
            logger.warning(f"Failed to fetch fresh data, trying to load cached file if available.")
            if os.path.exists(FILEPATH):
                df = pd.read_csv(FILEPATH)
                logger.info(f"Loaded cached data from file.")
            else:
                logger.error(f"No data available - file missing and fetch failed.")
                df = pd.DataFrame()
    else:
        logger.info("Using cached ticker list.")
        df = pd.read_csv(FILEPATH)

    return df
