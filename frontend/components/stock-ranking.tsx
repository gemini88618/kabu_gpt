import { PeriodSlot, ScreeningItem } from "@/lib/types";

export function StockRanking({ items, periodSlot }: { items: ScreeningItem[]; periodSlot: PeriodSlot }) {
  if (items.length === 0) {
    return (
      <section className="rounded-md border border-dashed border-line bg-white/60 p-6 text-center text-sm font-semibold text-ink/55">
        スクリーニングを実行するとトップ10が表示されます。
      </section>
    );
  }

  const isPast = periodSlot !== "current_to_next";

  return (
    <section className="space-y-2 pb-6">
      <div className="flex items-center justify-between px-1">
        <h2 className="text-lg font-black">Top 10</h2>
        <p className="text-xs font-bold text-ink/50">{isPast ? "実績あり" : "予測"}</p>
      </div>
      {items.map((item) => (
        <article key={`${item.symbol}-${item.rank}`} className="rounded-md border border-line bg-white p-3 shadow-sm">
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="text-xs font-black text-accent">#{item.rank} {item.symbol}</p>
              <h3 className="truncate text-base font-black text-ink">{item.name}</h3>
            </div>
            <div className="text-right">
              <p className="text-xl font-black text-ink">{item.probability.toFixed(1)}%</p>
              <p className="text-[11px] font-bold text-ink/50">上昇確率</p>
            </div>
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-center">
            <Cell label="予測" value={`${item.predictedReturn.toFixed(1)}%`} />
            <Cell label="実績" value={item.actualReturn == null ? "-" : `${item.actualReturn.toFixed(1)}%`} />
            <Cell label="Score" value={item.score.toFixed(2)} />
          </div>
        </article>
      ))}
    </section>
  );
}

function Cell({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded bg-panel px-2 py-2">
      <p className="text-[10px] font-bold uppercase text-ink/45">{label}</p>
      <p className="text-sm font-black text-ink">{value}</p>
    </div>
  );
}
