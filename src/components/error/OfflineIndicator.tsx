"use client";

import { useSyncExternalStore } from "react";

function getSnapshot(): boolean {
  return !navigator.onLine;
}

function getServerSnapshot(): boolean {
  return false;
}

function subscribe(callback: () => void): () => void {
  window.addEventListener("online", callback);
  window.addEventListener("offline", callback);
  return () => {
    window.removeEventListener("online", callback);
    window.removeEventListener("offline", callback);
  };
}

export function OfflineIndicator() {
  const isOffline = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  if (!isOffline) return null;

  return (
    <div
      role="alert"
      className="fixed bottom-0 left-0 right-0 z-50 border-t border-amber-300 bg-amber-100 px-4 py-3 text-center text-sm font-medium text-amber-800 dark:border-amber-700 dark:bg-amber-900/80 dark:text-amber-200"
    >
      You are currently offline. Some features may be unavailable.
    </div>
  );
}
