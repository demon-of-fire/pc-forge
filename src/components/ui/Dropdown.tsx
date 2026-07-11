"use client";

import { useState, useRef, useEffect, useCallback, type ReactNode } from "react";
import { cn } from "@/lib/utils/cn";

export interface DropdownItem {
  label: string;
  value: string;
  icon?: ReactNode;
  disabled?: boolean;
  separator?: boolean;
}

export interface DropdownProps {
  trigger: ReactNode;
  items: DropdownItem[];
  onSelect: (value: string) => void;
  align?: "left" | "right";
  className?: string;
}

export function Dropdown({
  trigger,
  items,
  onSelect,
  align = "left",
  className,
}: DropdownProps) {
  const [open, setOpen] = useState(false);
  const [focusIndex, setFocusIndex] = useState(-1);
  const menuRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const itemRefs = useRef<(HTMLButtonElement | null)[]>([]);

  const close = useCallback(() => {
    setOpen(false);
    setFocusIndex(-1);
    triggerRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!open) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        close();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open, close]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      const focusableItems = items.filter((item) => !item.disabled && !item.separator);
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setFocusIndex((prev) => (prev + 1) % focusableItems.length);
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setFocusIndex((prev) => (prev - 1 + focusableItems.length) % focusableItems.length);
      }
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        if (focusIndex >= 0 && focusIndex < focusableItems.length) {
          onSelect(focusableItems[focusIndex].value);
          close();
        }
      }
    },
    [items, focusIndex, onSelect, close]
  );

  useEffect(() => {
    if (focusIndex >= 0 && itemRefs.current[focusIndex]) {
      itemRefs.current[focusIndex]?.focus();
    }
  }, [focusIndex]);

  return (
    <div className="relative inline-block">
      <button
        ref={triggerRef}
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-haspopup="menu"
        className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
      >
        {trigger}
      </button>
      {open && (
        <div
          ref={menuRef}
          role="menu"
          onKeyDown={handleKeyDown}
          className={cn(
            "absolute z-50 mt-1 min-w-[180px] rounded-xl border border-zinc-200 bg-white py-1 shadow-lg",
            "dark:border-zinc-700 dark:bg-zinc-800",
            {
              "right-0": align === "right",
              "left-0": align === "left",
            },
            className
          )}
        >
          {items.map((item, i) => {
            if (item.separator) {
              return (
                <div
                  key={`sep-${i}`}
                  className="my-1 border-t border-zinc-200 dark:border-zinc-700"
                  role="separator"
                />
              );
            }
            let refIndex = 0;
            const focusableBefore = items.slice(0, i).filter(
              (it) => !it.disabled && !it.separator
            ).length;
            refIndex = focusableBefore;
            return (
              <button
                key={item.value}
                ref={(el) => { itemRefs.current[refIndex] = el; }}
                role="menuitem"
                disabled={item.disabled}
                onClick={() => {
                  onSelect(item.value);
                  close();
                }}
                className={cn(
                  "flex w-full items-center gap-2 px-3 py-2 text-sm text-left",
                  "hover:bg-zinc-100 dark:hover:bg-zinc-700",
                  "focus:bg-zinc-100 focus:outline-none dark:focus:bg-zinc-700",
                  "disabled:cursor-not-allowed disabled:opacity-50"
                )}
              >
                {item.icon && <span className="flex-shrink-0">{item.icon}</span>}
                {item.label}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
