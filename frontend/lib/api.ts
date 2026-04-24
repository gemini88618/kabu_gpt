import { API_BASE_URL } from "@/lib/constants";
import { BacktestResult, Coefficients, Market, PeriodSlot, PeriodType, ScreeningItem } from "@/lib/types";

type RequestPayload = {
  market: Market;
  periodType: PeriodType;
  periodSlot: PeriodSlot;
  coefficients: Coefficients;
};

function toApiCoefficients(coefficients: Coefficients) {
  return {
    per: coefficients.per,
    pbr: coefficients.pbr,
    roe: coefficients.roe,
    sales_growth: coefficients.salesGrowth,
    moving_average: coefficients.movingAverage,
    volume: coefficients.volume,
    momentum: coefficients.momentum
  };
}

export async function fetchScreening(payload: RequestPayload): Promise<ScreeningItem[]> {
  const response = await fetch(`${API_BASE_URL}/api/screen`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      market: payload.market,
      period_type: payload.periodType,
      period_slot: payload.periodSlot,
      coefficients: toApiCoefficients(payload.coefficients)
    })
  });

  if (!response.ok) {
    throw new Error("スクリーニングに失敗しました");
  }

  const json = await response.json();
  return json.items.map((item: any) => ({
    rank: item.rank,
    symbol: item.symbol,
    name: item.name,
    probability: item.probability,
    predictedReturn: item.predicted_return,
    actualReturn: item.actual_return,
    score: item.score
  }));
}

export async function fetchBacktest(payload: RequestPayload): Promise<BacktestResult> {
  const response = await fetch(`${API_BASE_URL}/api/backtest`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      market: payload.market,
      period_type: payload.periodType,
      period_slot: payload.periodSlot,
      coefficients: toApiCoefficients(payload.coefficients)
    })
  });

  if (!response.ok) {
    throw new Error("バックテストに失敗しました");
  }

  const json = await response.json();
  return {
    hitRate: json.hit_rate,
    averageReturn: json.average_return,
    maxDrawdown: json.max_drawdown,
    sampleSize: json.sample_size
  };
}
