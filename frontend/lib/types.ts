export type Market = "jp" | "us";
export type PeriodType = "weekly" | "monthly" | "half_year";
export type PeriodSlot = "p3_to_p2" | "p2_to_p1" | "p1_to_now" | "current_to_next";

export type Coefficients = {
  per: number;
  pbr: number;
  roe: number;
  salesGrowth: number;
  movingAverage: number;
  volume: number;
  momentum: number;
};

export type ScreeningItem = {
  rank: number;
  symbol: string;
  name: string;
  probability: number;
  predictedReturn: number;
  actualReturn: number | null;
  score: number;
};

export type BacktestResult = {
  hitRate: number;
  averageReturn: number;
  maxDrawdown: number;
  sampleSize: number;
};
