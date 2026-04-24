TARGET_RETURNS = {
    "weekly": 10.0,
    "monthly": 50.0,
    "half_year": 300.0,
}

PERIOD_DAYS = {
    "weekly": 5,
    "monthly": 21,
    "half_year": 126,
}

LOOKBACK_DAYS = {
    "weekly": 120,
    "monthly": 260,
    "half_year": 520,
}

YFINANCE_PERIODS = {
    "weekly": "6mo",
    "monthly": "1y",
    "half_year": "2y",
}

STOCK_UNIVERSE = {
    "jp": {
        "7203.T": "Toyota Motor",
        "6758.T": "Sony Group",
        "9984.T": "SoftBank Group",
        "8306.T": "Mitsubishi UFJ",
        "6861.T": "Keyence",
        "8035.T": "Tokyo Electron",
        "6098.T": "Recruit Holdings",
        "4063.T": "Shin-Etsu Chemical",
        "9432.T": "NTT",
        "7974.T": "Nintendo",
        "6501.T": "Hitachi",
        "8058.T": "Mitsubishi Corp"
    },
    "us": {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "NVDA": "NVIDIA",
        "AMZN": "Amazon",
        "GOOGL": "Alphabet",
        "META": "Meta Platforms",
        "TSLA": "Tesla",
        "AVGO": "Broadcom",
        "AMD": "Advanced Micro Devices",
        "NFLX": "Netflix",
        "CRM": "Salesforce",
        "COST": "Costco"
    },
}
