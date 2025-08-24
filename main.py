# main.py
import os
import pandas as pd
from utils.logger import Logger
from utils.validation import interactive_ticker_input
from scraper.nasdaq_tickers import scrape_ticker
from report_generator.generate_report import generate_report_from_json
import json

def main():
    logger = Logger("logs")
    logger.info("Starting Market Report Generator...")

    # Step 1: Get valid tickers from user
    tickers_dict = interactive_ticker_input()
    if not tickers_dict:
        logger.warning("No valid tickers selected. Exiting.")
        return

    tickers = list(tickers_dict.keys())
    logger.info(f"User selected tickers ({len(tickers)}): {tickers}")

    # Step 2: Scrape data for each ticker
    scraped_data = []
    for idx, symbol in enumerate(tickers, start=1):
        company_name = tickers_dict[symbol]
        try:
            logger.info(f"Scraping {idx}/{len(tickers)}: {symbol}")
            data = scrape_ticker(symbol, company_name)
            if data:
                scraped_data.append(data)
        except Exception as e:
            logger.error(f"Error scraping {symbol}: {e}")

    if not scraped_data:
        logger.warning("No data was scraped. Exiting.")
        return

    # Step 3: Save scraped data as CSV & JSON
    data_dir = os.path.join("data", "processed")
    os.makedirs(data_dir, exist_ok=True)

    csv_file = os.path.join(data_dir, "batch_scraped_data.csv")
    df = pd.DataFrame(scraped_data)
    df.to_csv(csv_file, index=False)
    logger.info(f"Saved scraped data to CSV: {csv_file}")

    json_file = os.path.join(data_dir, "batch_scraped_data.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2)
    logger.info(f"Saved scraped data to JSON: {json_file}")

    # Step 4: Generate PDF report
    report_path = generate_report_from_json(scraped_data)
    if report_path:
        logger.info(f"PDF report generated successfully: {report_path}")
    else:
        logger.error("Failed to generate PDF report.")

    logger.info("Market Report Generator finished successfully.")

if __name__ == "__main__":
    main()
