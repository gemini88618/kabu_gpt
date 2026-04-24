import numpy as np

from app.config import PERIOD_DAYS, TARGET_RETURNS
from app.models import Coefficients, PeriodSlot, PeriodType
from app.services.data_fetcher import StockData
from app.services.prediction import score_stock


def run_backtest(stocks: list[StockData], period_type: PeriodType, period_slot: PeriodSlot, coefficients: Coefficients) -> dict:
    horizon = PERIOD_DAYS[period_type]
    target = TARGET_RETURNS[period_type]
    returns: list[float] = []

    for stock in stocks:
        history = stock.history
        if len(history) < horizon * 6:
            continue

        max_offset = min(len(history) - horizon - 30, horizon * 8)
        step = max(5, horizon // 2)
        for offset in range(max_offset, 0, -step):
            train = history.iloc[: len(history) - offset]
            forward = history.iloc[len(history) - offset : len(history) - offset + horizon]
            if len(train) < 30 or len(forward) < 2:
                continue
            synthetic = StockData(symbol=stock.symbol, name=stock.name, history=train, info=stock.info)
            result = score_stock(synthetic, period_type, "current_to_next", coefficients)
            if result is None:
                continue
            actual = (float(forward["Close"].iloc[-1]) / float(forward["Close"].iloc[0]) - 1) * 100
            returns.append(actual)

    if not returns:
        return {"hit_rate": 0.0, "average_return": 0.0, "max_drawdown": 0.0, "sample_size": 0}

    arr = np.array(returns)
    equity = np.cumsum(arr)
    peak = np.maximum.accumulate(equity)
    drawdown = equity - peak

    return {
        "hit_rate": round(float((arr >= target).mean() * 100), 2),
        "average_return": round(float(arr.mean()), 2),
        "max_drawdown": round(float(drawdown.min()), 2),
        "sample_size": int(len(arr)),
    }
