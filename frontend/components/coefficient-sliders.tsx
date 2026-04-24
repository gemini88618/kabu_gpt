import { COEFFICIENT_LABELS } from "@/lib/constants";
import { Coefficients } from "@/lib/types";

export function CoefficientSliders({
  values,
  onChange
}: {
  values: Coefficients;
  onChange: (key: keyof Coefficients, value: number) => void;
}) {
  return (
    <div className="space-y-3">
      {(Object.keys(COEFFICIENT_LABELS) as Array<keyof Coefficients>).map((key) => (
        <label key={key} className="block">
          <div className="mb-1 flex items-center justify-between text-sm">
            <span className="font-bold text-ink">{COEFFICIENT_LABELS[key]}</span>
            <span className="rounded bg-panel px-2 py-1 text-xs font-black text-accent">{values[key].toFixed(2)}</span>
          </div>
          <input
            className="range touch-target"
            type="range"
            min="0"
            max="0.5"
            step="0.01"
            value={values[key]}
            onChange={(event) => onChange(key, Number(event.target.value))}
          />
        </label>
      ))}
    </div>
  );
}
