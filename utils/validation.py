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

"""     TEST CODE FOR TICKER VALIDATION
if __name__ == "__main__":
    from utils.logger import Logger
    from utils.validation import validate_tickers

    logger = Logger(print_to_console=True)
    
    tickers_input = ["aapl", "msft", "xyz", "GOOGL "]
    reference_data = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOGL": "Alphabet Inc."
    }
    validate_tickers(tickers_input, reference_data, logger=logger)
"""