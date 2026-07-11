import { forwardRef, type InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils/cn";

export interface CheckboxProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, id, ...props }, ref) => {
    const checkboxId = id || label?.toLowerCase().replace(/\s+/g, "-");
    return (
      <label
        htmlFor={checkboxId}
        className="inline-flex items-center gap-2 cursor-pointer"
      >
        <input
          ref={ref}
          type="checkbox"
          id={checkboxId}
          aria-checked={props.checked ?? props.defaultChecked ?? false}
          className={cn(
            "h-4 w-4 rounded border-zinc-300 bg-white text-blue-600",
            "focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
            "dark:border-zinc-600 dark:bg-zinc-800",
            className
          )}
          {...props}
        />
        {label && (
          <span className="text-sm text-zinc-700 dark:text-zinc-300">{label}</span>
        )}
      </label>
    );
  }
);

Checkbox.displayName = "Checkbox";

export { Checkbox };
