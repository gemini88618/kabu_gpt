import { PERIOD_SLOTS, PERIOD_TYPES } from "@/lib/constants";
import { PeriodSlot, PeriodType } from "@/lib/types";

type Props = {
  periodType: PeriodType;
  periodSlot: PeriodSlot;
  onTypeChange: (value: PeriodType) => void;
  onSlotChange: (value: PeriodSlot) => void;
};

export function PeriodSelector({ periodType, periodSlot, onTypeChange, onSlotChange }: Props) {
  const slots = PERIOD_SLOTS[periodType];

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-3 gap-2">
        {PERIOD_TYPES.map((item) => (
          <button
            key={item.value}
            className={`touch-target rounded-md px-2 py-2 text-sm font-black active:scale-95 ${
              periodType === item.value ? "bg-ink text-white" : "bg-panel text-ink"
            }`}
            onClick={() => onTypeChange(item.value)}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-2">
        {slots.map((slot) => (
          <button
            key={slot.value}
            className={`touch-target rounded-md border px-2 py-2 text-xs font-bold active:scale-95 ${
              periodSlot === slot.value ? "border-accent bg-accent/10 text-accent" : "border-line bg-white text-ink"
            }`}
            onClick={() => onSlotChange(slot.value)}
          >
            {slot.label}
          </button>
        ))}
      </div>
    </div>
  );
}
