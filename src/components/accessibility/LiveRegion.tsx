"use client";

import { useRef, type ReactNode } from "react";

export function LiveRegion({
  children,
  level = "polite",
}: {
  children: ReactNode;
  level?: "polite" | "assertive";
}) {
  return (
    <div
      aria-live={level}
      aria-atomic="true"
      className="sr-only"
    >
      {children}
    </div>
  );
}

export function AnnounceToScreenReader({
  message,
  level = "polite",
}: {
  message: string;
  level?: "polite" | "assertive";
}) {
  const ref = useRef<HTMLDivElement>(null);
  return (
    <div
      ref={ref}
      aria-live={level}
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );
}
