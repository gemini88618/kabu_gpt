import asyncio
from dataclasses import dataclass

import pandas as pd
import yfinance as yf

from app.config import STOCK_UNIVERSE, YFINANCE_PERIODS
from app.models import Market, PeriodType


@dataclass
class StockData:
    symbol: str
    name: str
    history: pd.DataFrame
    info: dict


def _download_symbol(symbol: str, name: str, yfinance_period: str) -> StockData:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period=yfinance_period, interval="1d", auto_adjust=True)
    info = {}
    try:
        info = ticker.info or {}
    except Exception:
        info = {}
    return StockData(symbol=symbol, name=name, history=history, info=info)


async def fetch_universe(market: Market, period_type: PeriodType) -> list[StockData]:
    yfinance_period = YFINANCE_PERIODS[period_type]
    tasks = [
        asyncio.to_thread(_download_symbol, symbol, name, yfinance_period)
        for symbol, name in STOCK_UNIVERSE[market].items()
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [item for item in results if isinstance(item, StockData) and not item.history.empty]
