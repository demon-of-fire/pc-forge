"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useSyncExternalStore,
  type ReactNode,
} from "react";

type Theme = "light" | "dark" | "system";

interface ThemeContextType {
  theme: Theme;
  resolved: "light" | "dark";
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "dark";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function applyThemeClass(t: Theme): "light" | "dark" {
  const resolvedTheme = t === "system" ? getSystemTheme() : t;
  if (typeof document !== "undefined") {
    const root = document.documentElement;
    root.classList.remove("light", "dark");
    root.classList.add(resolvedTheme);
  }
  return resolvedTheme as "light" | "dark";
}

function getThemeSnapshot(): string {
  return localStorage.getItem("pcforge-theme") || "system";
}

function getThemeServerSnapshot(): string {
  return "system";
}

function subscribeTheme(callback: () => void): () => void {
  window.addEventListener("storage", callback);
  return () => window.removeEventListener("storage", callback);
}

function useResolvedTheme(storedTheme: Theme): "light" | "dark" {
  return useSyncExternalStore(
    subscribeTheme,
    () => applyThemeClass(storedTheme),
    () => "dark" as const
  );
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const storedTheme = useSyncExternalStore(
    subscribeTheme,
    getThemeSnapshot,
    getThemeServerSnapshot
  ) as Theme;

  const resolved = useResolvedTheme(storedTheme);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = () => {
      if (storedTheme === "system") {
        applyThemeClass("system");
      }
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [storedTheme]);

  const setTheme = useCallback((t: Theme) => {
    applyThemeClass(t);
    try {
      localStorage.setItem("pcforge-theme", t);
    } catch {}
    window.dispatchEvent(new Event("storage"));
  }, []);

  return (
    <ThemeContext.Provider value={{ theme: storedTheme, resolved, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within a ThemeProvider");
  return ctx;
}
