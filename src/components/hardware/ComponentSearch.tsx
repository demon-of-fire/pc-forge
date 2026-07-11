import { cn } from "@/lib/utils/cn";

interface ComponentSearchProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
}

export function ComponentSearch({ value, onChange, placeholder = "Search components..." }: ComponentSearchProps) {
  return (
    <div className="relative w-full max-w-md">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-zinc-400">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </div>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
        className={cn(
          "h-10 w-full rounded-xl border border-zinc-300 bg-white pl-10 pr-4 text-sm text-zinc-900",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
          "dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
        )}
      />
    </div>
  );
}
