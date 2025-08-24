#yfinance_scraper
import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from typing import List, Dict, Any
from utils.logger import Logger

logger = Logger("logs")

def calculate_support_resistance(prices: pd.Series) -> Dict[str, List[float]]:
    if prices.empty:
        return {"support": [], "resistance": []}
    support = [float(prices.min()), float(prices.mean())]
    resistance = [float(prices.mean()), float(prices.max())]
    return {"support": support, "resistance": resistance}

def calculate_rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff().fillna(0)
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not rsi.empty and not pd.isna(rsi.iloc[-1]) else 50.0

def scrape_symbol(symbol: str) -> Dict[str, Any]:
    """Scrape price, indicators, and fundamentals; news is handled separately."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo", interval="1d")
        if hist.empty:
            logger.warning(f"No historical data for {symbol}")
            return {}

        latest_close = float(hist["Close"].iloc[-1])
        ema = float(hist["Close"].ewm(span=20).mean().iloc[-1])
        rsi = calculate_rsi(hist["Close"])
        atr = float(hist["High"].subtract(hist["Low"]).rolling(14).mean().iloc[-1])
        sr = calculate_support_resistance(hist["Close"])

        try:
            info = ticker.info
            company_info = {
                "name": info.get("shortName", symbol),
                "industry": info.get("industry", "N/A"),
                "website": info.get("website", ""),
                "exchange": info.get("exchange", "N/A"),
                "description": info.get("longBusinessSummary", ""),
            }
            fundamentals = {
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "eps": info.get("trailingEps"),
                "52w_high": info.get("fiftyTwoWeekHigh"),
                "52w_low": info.get("fiftyTwoWeekLow"),
            }
        except Exception as e:
            logger.warning(f"Failed to fetch info/fundamentals for {symbol}: {e}")
            company_info, fundamentals = {}, {}

        return {
            "symbol": symbol,
            "latest_close": latest_close,
            "ema": ema,
            "rsi": rsi,
            "atr": atr,
            "price_history": hist["Close"].tolist(),
            "support_resistance": sr,
            "company_info": company_info,
            "fundamentals": fundamentals,
            "timestamp": pd.Timestamp.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to scrape symbol {symbol}: {e}")
        return {}

def scrape_tickers(tickers: List[str]) -> List[Dict[str, Any]]:
    results = []
    for idx, symbol in enumerate(tickers, start=1):
        try:
            logger.info(f"Scraping {idx}/{len(tickers)}: {symbol}")
            data = scrape_symbol(symbol)
            if data:
                results.append(data)
        except Exception as e:
            logger.error(f"Error scraping {symbol}: {e}")
    return results
