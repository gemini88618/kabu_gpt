import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

SYMBOLS = {
    "jp": [
        ("7203.T", "トヨタ自動車"),
        ("6758.T", "ソニーグループ"),
        ("8035.T", "東京エレクトロン"),
        ("9984.T", "ソフトバンクグループ"),
        ("6861.T", "キーエンス"),
        ("7974.T", "任天堂"),
        ("6098.T", "リクルートホールディングス"),
        ("4063.T", "信越化学工業"),
        ("6501.T", "日立製作所"),
        ("8058.T", "三菱商事"),
        ("8306.T", "三菱UFJフィナンシャル・グループ"),
        ("9432.T", "日本電信電話"),
    ],
    "us": [
        ("NVDA", "NVIDIA"),
        ("MSFT", "Microsoft"),
        ("AAPL", "Apple"),
        ("AMZN", "Amazon"),
        ("GOOGL", "Alphabet"),
        ("META", "Meta Platforms"),
        ("TSLA", "Tesla"),
        ("AVGO", "Broadcom"),
        ("AMD", "Advanced Micro Devices"),
        ("NFLX", "Netflix"),
        ("CRM", "Salesforce"),
        ("COST", "Costco"),
    ],
}


def synthetic_history(symbol: str, index: int, days: int = 560) -> dict:
    start = datetime.now(timezone.utc).date() - timedelta(days=days * 1.45)
    dates: list[str] = []
    close: list[float] = []
    volume: list[int] = []
    price = 80 + index * 11
    day = start

    while len(close) < days:
        if day.weekday() < 5:
            t = len(close)
            drift = 0.0009 + (index % 5) * 0.00018
            wave = math.sin(t / (13 + index % 4)) * 0.014
            pulse = math.cos(t / (37 + index % 5)) * 0.008
            price = max(5, price * (1 + drift + wave + pulse))
            dates.append(day.isoformat())
            close.append(round(price, 2))
            volume.append(int(900_000 + index * 140_000 + abs(math.sin(t / 9)) * 700_000))
        day += timedelta(days=1)

    return {"symbol": symbol, "dates": dates, "close": close, "volume": volume}


def fetch_yfinance_history(symbol: str) -> dict | None:
    try:
        import yfinance as yf

        history = yf.Ticker(symbol).history(period="2y", interval="1d", auto_adjust=True)
        if history.empty or "Close" not in history:
            return None
        history = history.dropna(subset=["Close"])
        return {
            "symbol": symbol,
            "dates": [idx.strftime("%Y-%m-%d") for idx in history.index],
            "close": [round(float(value), 4) for value in history["Close"].tolist()],
            "volume": [int(value) for value in history["Volume"].fillna(0).tolist()],
        }
    except Exception:
        return None


def build_market_data() -> dict:
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "yfinance_with_synthetic_fallback",
        "markets": {},
    }

    global_index = 0
    for market, symbols in SYMBOLS.items():
        output["markets"][market] = []
        for symbol, name in symbols:
            history = fetch_yfinance_history(symbol) or synthetic_history(symbol, global_index)
            output["markets"][market].append({"symbol": symbol, "name": name, **history})
            global_index += 1

    return output


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "market-data.json").write_text(
        json.dumps(build_market_data(), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
