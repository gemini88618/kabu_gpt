from fastapi import APIRouter

from app.config import STOCK_UNIVERSE, TARGET_RETURNS
from app.models import BacktestResponse, ScreenRequest, ScreenResponse
from app.services.backtest import run_backtest
from app.services.data_fetcher import fetch_universe
from app.services.prediction import rank_stocks

router = APIRouter()


@router.get("/stocks/{market}")
def stocks(market: str) -> dict:
    return {"market": market, "items": STOCK_UNIVERSE.get(market, {})}


@router.post("/screen", response_model=ScreenResponse)
async def screen(request: ScreenRequest) -> ScreenResponse:
    stocks_data = await fetch_universe(request.market, request.period_type)
    items = rank_stocks(stocks_data, request.period_type, request.period_slot, request.coefficients)
    return ScreenResponse(
        market=request.market,
        period_type=request.period_type,
        period_slot=request.period_slot,
        target_return=TARGET_RETURNS[request.period_type],
        items=items,
    )


@router.post("/backtest", response_model=BacktestResponse)
async def backtest(request: ScreenRequest) -> BacktestResponse:
    stocks_data = await fetch_universe(request.market, request.period_type)
    result = run_backtest(stocks_data, request.period_type, request.period_slot, request.coefficients)
    return BacktestResponse(
        market=request.market,
        period_type=request.period_type,
        period_slot=request.period_slot,
        target_return=TARGET_RETURNS[request.period_type],
        **result,
    )
