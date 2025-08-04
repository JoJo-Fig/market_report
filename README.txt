**Market Report** is a Python-based data collection and reporting tool that scrapes 
financial data for selected stocks and generates human-friendly reports.  
It combines company fundamentals with news headlines to give a concise view of a 
company’s recent performance and sentiment.

This project is designed to:
- Demonstrate web scraping, logging, and structured data handling
- Store data in a machine- and human-readable format
- Generate reports that summarize scraped data

---

## Features

    Scrapes company info from Yahoo Finance
    Pulls recent news headlines per ticker
    Uses a custom logger for clean logging and debugging
    Stores cleaned data in JSON and CSV formats
    (Planned) PDF report generation
    (Planned) SQL integration for structured data storage

---

## Folder Structure

market_report/
├── data/
├── logger.py
├── report_generator/
├── scrapers/
├── utils/
├── requirements.txt
├── README.md