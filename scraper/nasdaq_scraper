import requests
import json
import os
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Referer': 'https://www.nasdaq.com'
}

BASE_URL = "https://api.nasdaq.com/api/screener/stocks"
SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "data")

def fetch_stocks(offset=0, limit=25):
    params = {
        'tableonly': 'false',
        'limit': limit,
        'offset': offset,
        'exchange': 'NASDAQ'
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def save_to_file(data, filename):
    os.makedirs(SAVE_PATH, exist_ok=True)
    full_path = os.path.join(SAVE_PATH, filename)
    with open(full_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {full_path}")

def main():
    all_results = []
    for offset in range(0, 100, 25):  # First 100 stocks
        print(f"Fetching offset: {offset}")
        data = fetch_stocks(offset)
        rows = data.get("data", {}).get("rows", [])
        all_results.extend(rows)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"nasdaq_stocks_{timestamp}.json"
    save_to_file(all_results, filename)

if __name__ == "__main__":
    main()
