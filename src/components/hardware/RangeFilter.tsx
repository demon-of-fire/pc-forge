interface RangeFilterProps {
  label: string;
  value: [number, number];
  onChange: (val: [number, number]) => void;
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
}

export function RangeFilter({ label, value, onChange, unit = "" }: RangeFilterProps) {
  const baseId = label.toLowerCase().replace(/\s+/g, "-");
  const minId = `${baseId}-min`;
  const maxId = `${baseId}-max`;

  const handleChange = (index: number, val: string) => {
    const newVal = parseFloat(val);
    const nextValue = [...value] as [number, number];
    nextValue[index] = newVal;
    onChange(nextValue);
  };

  return (
    <div className="flex flex-col gap-2">
      <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
        {label}
      </span>
      <div className="flex items-center gap-2">
        <label htmlFor={minId} className="sr-only">Minimum {label}</label>
        <input
          id={minId}
          type="number"
          value={value[0]}
          onChange={(e) => handleChange(0, e.target.value)}
          aria-label={`Minimum ${label}`}
          className="h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
        />
        <span className="text-zinc-400" aria-hidden="true">-</span>
        <label htmlFor={maxId} className="sr-only">Maximum {label}</label>
        <input
          id={maxId}
          type="number"
          value={value[1]}
          onChange={(e) => handleChange(1, e.target.value)}
          aria-label={`Maximum ${label}`}
          className="h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
        />
        {unit && <span className="text-sm text-zinc-500 dark:text-zinc-400" aria-hidden="true">{unit}</span>}
      </div>
    </div>
  );
}
