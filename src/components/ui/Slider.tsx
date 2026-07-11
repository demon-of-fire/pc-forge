import { forwardRef, type InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils/cn";

export interface SliderProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
  showValue?: boolean;
  min?: number;
  max?: number;
}

const Slider = forwardRef<HTMLInputElement, SliderProps>(
  ({ className, label, showValue = true, min = 0, max = 100, value, id, ...props }, ref) => {
    const sliderId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);
    return (
      <div className="flex flex-col gap-1.5">
        {(label || showValue) && (
          <div className="flex items-center justify-between">
            {label && (
              <label
                htmlFor={sliderId}
                className="text-sm font-medium text-zinc-700 dark:text-zinc-300"
              >
                {label}
              </label>
            )}
            {showValue && (
              <span className="text-sm text-zinc-500 dark:text-zinc-400" aria-hidden="true">
                {value ?? min}
              </span>
            )}
          </div>
        )}
        <input
          ref={ref}
          id={sliderId}
          type="range"
          min={min}
          max={max}
          value={value}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={Number(value ?? min)}
          aria-label={label || undefined}
          className={cn(
            "h-2 w-full appearance-none rounded-full bg-zinc-200 dark:bg-zinc-700",
            "[&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none",
            "[&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-blue-600",
            "[&::-webkit-slider-thumb]:focus-visible:ring-2 [&::-webkit-slider-thumb]:focus-visible:ring-blue-500",
            className
          )}
          {...props}
        />
      </div>
    );
  }
);

Slider.displayName = "Slider";

export { Slider };
