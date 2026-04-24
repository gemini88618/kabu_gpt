import { Coefficients, PeriodSlot, PeriodType } from "@/lib/types";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export const PERIOD_TYPES: Array<{ value: PeriodType; label: string }> = [
  { value: "weekly", label: "週" },
  { value: "monthly", label: "月" },
  { value: "half_year", label: "半年" }
];

export const PERIOD_SLOTS: Record<PeriodType, Array<{ value: PeriodSlot; label: string }>> = {
  weekly: [
    { value: "p3_to_p2", label: "3週前→2週前" },
    { value: "p2_to_p1", label: "2週前→1週前" },
    { value: "p1_to_now", label: "1週前→現在" },
    { value: "current_to_next", label: "現在→1週後" }
  ],
  monthly: [
    { value: "p3_to_p2", label: "3か月前→2か月前" },
    { value: "p2_to_p1", label: "2か月前→1か月前" },
    { value: "p1_to_now", label: "1か月前→現在" },
    { value: "current_to_next", label: "現在→1か月後" }
  ],
  half_year: [
    { value: "p3_to_p2", label: "18か月前→12か月前" },
    { value: "p2_to_p1", label: "12か月前→6か月前" },
    { value: "p1_to_now", label: "6か月前→現在" },
    { value: "current_to_next", label: "現在→6か月後" }
  ]
};

export const DEFAULT_COEFFICIENTS: Coefficients = {
  per: 0.08,
  pbr: 0.07,
  roe: 0.15,
  salesGrowth: 0.16,
  movingAverage: 0.18,
  volume: 0.16,
  momentum: 0.20
};

export const COEFFICIENT_LABELS: Record<keyof Coefficients, string> = {
  per: "PER",
  pbr: "PBR",
  roe: "ROE",
  salesGrowth: "売上成長率",
  movingAverage: "移動平均",
  volume: "出来高",
  momentum: "モメンタム"
};
