import { Market } from "@/lib/types";

const markets: Array<{ value: Market; label: string }> = [
  { value: "jp", label: "日本株" },
  { value: "us", label: "米国株" }
];

export function MarketToggle({ market, onChange }: { market: Market; onChange: (value: Market) => void }) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {markets.map((item) => (
        <button
          key={item.value}
          className={`touch-target rounded-md px-3 py-2 text-sm font-black active:scale-95 ${
            market === item.value ? "bg-accent text-white" : "bg-panel text-ink"
          }`}
          onClick={() => onChange(item.value)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
