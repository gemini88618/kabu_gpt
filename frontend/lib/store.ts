import { create } from "zustand";
import { DEFAULT_COEFFICIENTS } from "@/lib/constants";
import { fetchBacktest, fetchScreening } from "@/lib/api";
import { BacktestResult, Coefficients, Market, PeriodSlot, PeriodType, ScreeningItem } from "@/lib/types";

type ScannerState = {
  market: Market;
  periodType: PeriodType;
  periodSlot: PeriodSlot;
  coefficients: Coefficients;
  items: ScreeningItem[];
  backtest: BacktestResult | null;
  loading: boolean;
  error: string | null;
  setMarket: (value: Market) => void;
  setPeriodType: (value: PeriodType) => void;
  setPeriodSlot: (value: PeriodSlot) => void;
  setCoefficient: (key: keyof Coefficients, value: number) => void;
  screen: () => Promise<void>;
  runBacktest: () => Promise<void>;
  reset: () => void;
};

export const useScannerStore = create<ScannerState>((set, get) => ({
  market: "jp",
  periodType: "weekly",
  periodSlot: "current_to_next",
  coefficients: DEFAULT_COEFFICIENTS,
  items: [],
  backtest: null,
  loading: false,
  error: null,
  setMarket: (market) => set({ market, items: [], backtest: null, error: null }),
  setPeriodType: (periodType) => set({ periodType, periodSlot: "current_to_next", items: [], backtest: null, error: null }),
  setPeriodSlot: (periodSlot) => set({ periodSlot, items: [], backtest: null, error: null }),
  setCoefficient: (key, value) =>
    set((state) => ({
      coefficients: { ...state.coefficients, [key]: value },
      items: [],
      backtest: null,
      error: null
    })),
  screen: async () => {
    const state = get();
    set({ loading: true, error: null });
    try {
      const items = await fetchScreening(state);
      set({ items, loading: false });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "エラーが発生しました", loading: false });
    }
  },
  runBacktest: async () => {
    const state = get();
    set({ loading: true, error: null });
    try {
      const backtest = await fetchBacktest(state);
      set({ backtest, loading: false });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "エラーが発生しました", loading: false });
    }
  },
  reset: () =>
    set({
      market: "jp",
      periodType: "weekly",
      periodSlot: "current_to_next",
      coefficients: DEFAULT_COEFFICIENTS,
      items: [],
      backtest: null,
      error: null
    })
}));
