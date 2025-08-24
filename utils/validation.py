#validation.py
import sys
from scraper.nasdaq_tickers import get_nasdaq_listed
from utils.logger import Logger

logger = Logger("logs")

def get_user_tickers():
    user_tickers = input("Enter ticker symbols, separated by commas: ")
    tickers = user_tickers.split(",")
    return tickers

def validate_tickers(tickers: list[str], reference: dict[str, str], logger=None):
    clean = [t.strip().upper() for t in tickers]
    ref_symbols = set(reference.keys())
    valid_tickers = {}
    invalid_tickers = []

    for t in clean:
        if t in ref_symbols:
            valid_tickers[t] = reference[t]
        else:
            invalid_tickers.append(t)

    if logger:
        logger.info(f"Validated {len(valid_tickers)} tickers")
        if invalid_tickers:
            logger.warning(f"Invalid tickers: {invalid_tickers}")

    return valid_tickers, invalid_tickers

def interactive_ticker_input():
    df = get_nasdaq_listed()
    if df.empty:
        if logger:
            logger.critical("No NASDAQ data available. Exiting.")
        sys.exit(1)
    reference_data = dict(zip(df["Symbol"], df["Security Name"]))

    while True:
        tickers = get_user_tickers()
        valid, invalid = validate_tickers(tickers, reference_data, logger)
        print("Valid ticker(s): ", valid)
        if invalid:
            print("Invalid ticker(s): ", invalid)
        print("\nOptions:")
        print("1. Retry input")
        print("2. Continue with valid ticker(s)")
        print("3. Exit menu")
        choice = input("Choose an option - (1/2/3)" ).strip()

        if choice == "1":
            continue
        elif choice == "2":
            return valid
        elif choice == "3":
            return None
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
