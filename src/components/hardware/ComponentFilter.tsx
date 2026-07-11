import { cn } from "@/lib/utils/cn";

interface ComponentFilterProps {
  label: string;
  value: string;
  onChange: (val: string) => void;
  options: string[];
}

export function ComponentFilter({ label, value, onChange, options }: ComponentFilterProps) {
  const filterId = label.toLowerCase().replace(/\s+/g, "-");
  return (
    <div className="flex flex-col gap-2">
      <label
        htmlFor={filterId}
        className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
      >
        {label}
      </label>
      <select
        id={filterId}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={cn(
          "h-10 rounded-lg border border-zinc-300 bg-white px-3 text-sm text-zinc-900",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
          "dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
        )}
      >
        <option value="all">All</option>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}
