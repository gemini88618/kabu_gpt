from typing import Literal

from pydantic import BaseModel, Field

Market = Literal["jp", "us"]
PeriodType = Literal["weekly", "monthly", "half_year"]
PeriodSlot = Literal["p3_to_p2", "p2_to_p1", "p1_to_now", "current_to_next"]


class Coefficients(BaseModel):
    per: float = Field(default=0.08, ge=0, le=1)
    pbr: float = Field(default=0.07, ge=0, le=1)
    roe: float = Field(default=0.15, ge=0, le=1)
    sales_growth: float = Field(default=0.16, ge=0, le=1)
    moving_average: float = Field(default=0.18, ge=0, le=1)
    volume: float = Field(default=0.16, ge=0, le=1)
    momentum: float = Field(default=0.20, ge=0, le=1)


class ScreenRequest(BaseModel):
    market: Market
    period_type: PeriodType
    period_slot: PeriodSlot
    coefficients: Coefficients = Field(default_factory=Coefficients)


class ScreenItem(BaseModel):
    rank: int
    symbol: str
    name: str
    probability: float
    predicted_return: float
    actual_return: float | None
    score: float


class ScreenResponse(BaseModel):
    market: Market
    period_type: PeriodType
    period_slot: PeriodSlot
    target_return: float
    items: list[ScreenItem]


class BacktestResponse(BaseModel):
    market: Market
    period_type: PeriodType
    period_slot: PeriodSlot
    target_return: float
    hit_rate: float
    average_return: float
    max_drawdown: float
    sample_size: int
