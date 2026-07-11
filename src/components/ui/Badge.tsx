import { cn } from "@/lib/utils/cn";

export interface BadgeProps {
  variant?: "default" | "secondary" | "success" | "warning" | "danger" | "info";
  size?: "sm" | "md";
  children: React.ReactNode;
  className?: string;
}

export function Badge({
  variant = "default",
  size = "sm",
  children,
  className,
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full font-medium",
        {
          "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300": variant === "default",
          "bg-zinc-200 text-zinc-600 dark:bg-zinc-700 dark:text-zinc-400": variant === "secondary",
          "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400": variant === "success",
          "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400": variant === "warning",
          "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400": variant === "danger",
          "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400": variant === "info",
        },
        {
          "px-2 py-0.5 text-xs": size === "sm",
          "px-2.5 py-1 text-sm": size === "md",
        },
        className
      )}
    >
      {children}
    </span>
  );
}
