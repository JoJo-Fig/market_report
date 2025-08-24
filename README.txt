Market Report Generator

A Python-based financial data aggregation and reporting tool, designed to showcase web scraping, structured data handling, and automated report generation. This project consolidates stock data, technical indicators, and news headlines into both human- and machine-readable formats.

Portfolio Context

This project was developed as part of a portfolio to demonstrate:

Full-stack data workflow: from data ingestion (scraping) > processing > storage > reporting.

Robust input validation: NASDAQ ticker validation prevents invalid requests.

Modular architecture: Easily extendable to new data sources, indicators, or reporting formats.

Error-handling & logging: All scraping and reporting operations are logged with severity levels for traceability.

Real-world constraints: Handles rate limits, missing data, and inconsistent ticker listings, mirroring challenges faced in production systems.

Key Features

Validated ticker input: Uses a locally cached NASDAQ listing to ensure accurate symbol selection.

Data scraping:

Historical stock prices (3 months, daily interval)

Technical indicators: EMA, RSI, ATR

Support and resistance levels calculated dynamically

News integration: Fetches recent headlines from Yahoo Finance, enhancing fundamental analysis.

Data persistence:

Machine-readable: JSON & CSV

Human-readable: PDF reports with charts and tables

Custom logging system: Daily log rotation, console + file output, multiple severity levels.

Modular design: Separate modules for scraping, validation, logging, and report generation for easy reuse.

Design Decisions

Interactive CLI: Allows users to enter multiple tickers, validates them, and handles invalid inputs gracefully.

Caching of NASDAQ symbols: Reduces unnecessary network calls and ensures offline validation.

Separated news scraping: Avoids coupling stock data and news, making each component independently testable.

PDF reports: Integrates charts and tables dynamically, showcasing real-time data visualization.

Error resilience: Warnings for rate limits or missing data, with logging for debugging and audit purposes.

Folder Structure
market_report/
    data/                  # JSON and CSV outputs
    logs/                  # Daily log files for scraping and reporting
    scrapers/              # Modules for stock data & news scraping
    report_generator/      # PDF generation modules
    utils/                 # Supporting modules (logger, validation)
    requirements.txt       # Python dependencies
    main.py                # Entry point for executing the workflow
    README.md              # Documentation and portfolio showcase

Tech Stack

    Python 3.13.6

    Data: pandas

    Web scraping: requests, BeautifulSoup4, yfinance

    Reporting: reportlab, matplotlib

    Logging: Custom Logger class with daily rotation

    File handling: os, sys, json, csv, datetime, time

Installation & Setup

Clone the repository:

git clone https://github.com/<your-username>/market_report.git
cd market_report


(Optional) Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

How It Works

Ticker input & validation:
Users enter NASDAQ tickers; invalid entries are flagged.

Data scraping:

Historical prices & indicators are calculated.

News headlines are fetched from Yahoo Finance.

Data storage:

JSON for programmatic access

CSV for spreadsheet-style review

PDF report generation:

Summaries include price tables, charts, and news headlines

Automatically saves to reports/

Example Outputs

CSV & JSON: Cleanly structured datasets including latest prices, indicators, and news links.

PDF report: Visual, per-ticker summary with charts, support/resistance levels, and headlines.

Logs: Detailed record of workflow events, warnings, and errors.

Future Enhancements

Advanced report analytics: Auto-generated insights and trends.

Support for multiple exchanges: Include NYSE, AMEX, etc.

SQL database storage: For historical data tracking and query efficiency.

Company search by name: Allow flexible input beyond ticker symbols.

Why This Project Matters

This repository demonstrates practical skills highly valued in data engineering and financial analytics portfolios:

Building scalable workflows with modular design

Handling real-world data limitations like rate-limits and missing values

Generating readable outputs suitable for both technical review and presentation