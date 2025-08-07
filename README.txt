A Python-based tool that scrapes financial data for user-selected stock tickers and generates human-readable summaries. It combines fundamental information and recent news sentiment to provide a concise overview of a company's performance.

This project is designed to:

    Demonstrate web scraping, logging, and structured data handling
    Validate ticker inputs against the official Nasdaq listed symbols file
    Store data in both machine- and human-readable formats
    Lay the foundation for future report generation

Features
    Validates stock symbols against a locally cached Nasdaq listing
    Scrapes company details and recent headlines from Yahoo Finance
    Custom logger supports multiple severity levels and daily log rotation
    Stores data in JSON and CSV formats
    Modular project layout for future scalability

Planned Additions
    Report generation in one or more exportable formats
    SQL support for structured data storage
    Company name-based search for more flexible input
    Interactive command-line prompts for better user experience

Folder Structure
    market_report/
    ├── data/                  # JSON and CSV outputs
    ├── logs/                  # Daily log files
    ├── scrapers/             # Web scraping modules
    ├── report_generator/     # Report formatting and export (future)
    ├── utils/                # Supporting modules (e.g., logger)
    ├── requirements.txt      # Dependencies
    ├── README.md             # Project documentation

Tech Stack
    Python 3.13.6
    requests
    logging
    os, sys, json, csv, datetime
