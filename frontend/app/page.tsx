"use client";

import { Activity, BarChart3, RotateCcw, SlidersHorizontal } from "lucide-react";
import { CoefficientSliders } from "@/components/coefficient-sliders";
import { MarketToggle } from "@/components/market-toggle";
import { PeriodSelector } from "@/components/period-selector";
import { StockRanking } from "@/components/stock-ranking";
import { useScannerStore } from "@/lib/store";

export default function HomePage() {
  const {
    market,
    periodType,
    periodSlot,
    coefficients,
    items,
    loading,
    error,
    backtest,
    setMarket,
    setPeriodType,
    setPeriodSlot,
    setCoefficient,
    screen,
    runBacktest,
    reset
  } = useScannerStore();

  return (
    <main className="ios-shell mx-auto flex w-full max-w-md flex-col gap-4 px-4">
      <header className="pt-2">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">PWA Scanner</p>
            <h1 className="mt-1 text-3xl font-black tracking-normal text-ink">Stock Scanner</h1>
          </div>
          <button
            className="touch-target rounded-md border border-line bg-white/80 px-3 text-ink shadow-sm active:scale-95"
            onClick={reset}
            aria-label="Reset"
          >
            <RotateCcw size={20} />
          </button>
        </div>
      </header>

      <section className="rounded-md border border-line bg-white/85 p-3 shadow-app backdrop-blur">
        <MarketToggle market={market} onChange={setMarket} />
        <div className="mt-3">
          <PeriodSelector
            periodType={periodType}
            periodSlot={periodSlot}
            onTypeChange={setPeriodType}
            onSlotChange={setPeriodSlot}
          />
        </div>
      </section>

      <section className="rounded-md border border-line bg-white/85 p-3 shadow-app">
        <div className="mb-3 flex items-center gap-2">
          <SlidersHorizontal size={18} className="text-accent" />
          <h2 className="text-base font-bold">係数</h2>
        </div>
        <CoefficientSliders values={coefficients} onChange={setCoefficient} />
      </section>

      {error ? (
        <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm font-semibold text-red-700">{error}</div>
      ) : null}

      <div className="grid grid-cols-2 gap-3">
        <button
          className="touch-target rounded-md bg-ink px-4 py-3 font-bold text-white shadow-app active:scale-[0.98] disabled:opacity-50"
          onClick={screen}
          disabled={loading}
        >
          <span className="inline-flex items-center gap-2">
            <Activity size={18} />
            {loading ? "計算中" : "スクリーニング"}
          </span>
        </button>
        <button
          className="touch-target rounded-md border border-line bg-white px-4 py-3 font-bold text-ink shadow-sm active:scale-[0.98] disabled:opacity-50"
          onClick={runBacktest}
          disabled={loading}
        >
          <span className="inline-flex items-center gap-2">
            <BarChart3 size={18} />
            バックテスト
          </span>
        </button>
      </div>

      {backtest ? (
        <section className="grid grid-cols-3 gap-2 rounded-md border border-line bg-panel p-3 text-center">
          <Metric label="Hit" value={`${backtest.hitRate.toFixed(1)}%`} />
          <Metric label="Avg" value={`${backtest.averageReturn.toFixed(1)}%`} />
          <Metric label="Max DD" value={`${backtest.maxDrawdown.toFixed(1)}%`} />
        </section>
      ) : null}

      <StockRanking items={items} periodSlot={periodSlot} />
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[11px] font-bold uppercase text-ink/50">{label}</p>
      <p className="text-lg font-black text-ink">{value}</p>
    </div>
  );
}
