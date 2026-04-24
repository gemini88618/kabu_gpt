import math

import numpy as np
import pandas as pd

from app.config import PERIOD_DAYS, TARGET_RETURNS
from app.models import Coefficients, PeriodSlot, PeriodType
from app.services.data_fetcher import StockData


def _clip(value: float, low: float = -1.0, high: float = 1.0) -> float:
    if value is None or math.isnan(value):
        return 0.0
    return max(low, min(high, value))


def _safe_float(value, default: float = 0.0) -> float:
    try:
        if value is None or np.isnan(value):
            return default
        return float(value)
    except Exception:
        return default


def _score_per(per: float) -> float:
    if per <= 0:
        return -0.3
    if 8 <= per <= 20:
        return 1.0
    if 20 < per <= 35:
        return 0.5
    if 35 < per <= 60:
        return 0.0
    if per > 60:
        return -0.5
    return 0.2


def _score_pbr(pbr: float) -> float:
    if pbr <= 0:
        return 0.0
    if pbr < 0.7:
        return -0.2
    if pbr <= 3:
        return 1.0
    if pbr <= 6:
        return 0.5
    if pbr <= 10:
        return 0.0
    return -0.5


def _window(history: pd.DataFrame, period_type: PeriodType, period_slot: PeriodSlot) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    horizon = PERIOD_DAYS[period_type]
    if period_slot == "current_to_next":
        return history.iloc[-max(26, horizon + 26):], None
    if period_slot == "p1_to_now":
        source = history.iloc[:-horizon]
        evaluation = history.iloc[-horizon:]
    elif period_slot == "p2_to_p1":
        source = history.iloc[: -horizon * 2]
        evaluation = history.iloc[-horizon * 2 : -horizon]
    else:
        source = history.iloc[: -horizon * 3]
        evaluation = history.iloc[-horizon * 3 : -horizon * 2]

    return source, evaluation


def score_stock(stock: StockData, period_type: PeriodType, period_slot: PeriodSlot, coefficients: Coefficients) -> dict | None:
    history, evaluation = _window(stock.history, period_type, period_slot)
    if len(history) < 30:
        return None

    close = history["Close"]
    volume = history["Volume"]
    latest = float(close.iloc[-1])
    ma5 = float(close.rolling(5).mean().iloc[-1])
    ma25 = float(close.rolling(25).mean().iloc[-1])
    recent_return = ((latest / float(close.iloc[-6])) - 1) * 100 if len(close) >= 6 else 0.0
    volume_change = ((float(volume.tail(5).mean()) / float(volume.tail(25).mean())) - 1) * 100 if volume.tail(25).mean() else 0.0

    info = stock.info
    per = _safe_float(info.get("trailingPE"))
    pbr = _safe_float(info.get("priceToBook"))
    roe = _safe_float(info.get("returnOnEquity")) * 100
    sales_growth = _safe_float(info.get("revenueGrowth")) * 100

    per_score = _score_per(per)
    pbr_score = _score_pbr(pbr)
    roe_score = _clip((roe - 5) / 20)
    sales_score = _clip(sales_growth / 30)
    ma_score = _clip(((ma5 - ma25) / ma25) / 0.10) if ma25 else 0.0
    volume_score = _clip(volume_change / 100)
    momentum_score = _clip(recent_return / 20)

    total_weight = sum(coefficients.model_dump().values()) or 1
    raw_score = (
        coefficients.per * per_score
        + coefficients.pbr * pbr_score
        + coefficients.roe * roe_score
        + coefficients.sales_growth * sales_score
        + coefficients.moving_average * ma_score
        + coefficients.volume * volume_score
        + coefficients.momentum * momentum_score
    ) / total_weight

    k = {"weekly": 2.2, "monthly": 1.8, "half_year": 1.4}[period_type]
    probability = 100 / (1 + math.exp(-k * raw_score))
    predicted_return = probability / 100 * TARGET_RETURNS[period_type]

    actual_return = None
    if evaluation is not None and len(evaluation) >= 2:
        actual_return = (float(evaluation["Close"].iloc[-1]) / float(evaluation["Close"].iloc[0]) - 1) * 100

    return {
        "symbol": stock.symbol,
        "name": stock.name,
        "score": round(raw_score, 4),
        "probability": round(probability, 2),
        "predicted_return": round(predicted_return, 2),
        "actual_return": None if actual_return is None else round(actual_return, 2),
    }


def rank_stocks(stocks: list[StockData], period_type: PeriodType, period_slot: PeriodSlot, coefficients: Coefficients) -> list[dict]:
    scored = [
        result
        for result in (score_stock(stock, period_type, period_slot, coefficients) for stock in stocks)
        if result is not None
    ]
    scored.sort(key=lambda item: (item["probability"], item["predicted_return"]), reverse=True)
    return [{**item, "rank": index + 1} for index, item in enumerate(scored[:10])]
