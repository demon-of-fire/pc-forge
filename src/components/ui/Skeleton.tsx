"use client";

import { cn } from "@/lib/utils/cn";

export interface SkeletonProps {
  className?: string;
  variant?: "text" | "circular" | "rectangular";
}

export function Skeleton({ className, variant = "rectangular" }: SkeletonProps) {
  return (
    <div
      className={cn(
        "animate-pulse bg-zinc-200 dark:bg-zinc-700",
        {
          "h-4 w-full rounded": variant === "text",
          "rounded-full": variant === "circular",
          "rounded-xl": variant === "rectangular",
        },
        className
      )}
      aria-hidden="true"
    />
  );
}
