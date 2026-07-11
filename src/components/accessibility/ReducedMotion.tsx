"use client";

import { useSyncExternalStore } from "react";

function getSnapshot(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function getServerSnapshot(): boolean {
  return false;
}

function subscribe(callback: () => void): () => void {
  const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  mq.addEventListener("change", callback);
  return () => mq.removeEventListener("change", callback);
}

export function ReducedMotion({ children }: { children: React.ReactNode }) {
  const prefersReduced = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  return (
    <div data-reduced-motion={prefersReduced ? "true" : undefined}>
      {children}
    </div>
  );
}
