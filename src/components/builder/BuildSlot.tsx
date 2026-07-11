import { ComponentType, Component } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface BuildSlotProps {
  type: ComponentType;
  component: Component | null;
  onSelect: () => void;
  onRemove: () => void;
}

export function BuildSlot({ type, component, onSelect, onRemove }: BuildSlotProps) {
  const label = {
    cpu: "Processor",
    gpu: "Graphics Card",
    motherboard: "Motherboard",
    ram: "Memory",
    storage: "Storage",
    psu: "Power Supply",
    case: "Case",
    cooler: "CPU Cooler",
  }[type];

  return (
    <Card className="p-4 flex items-center justify-between gap-4 border-zinc-200 dark:border-zinc-800">
      <div className="flex items-center gap-4">
        <div className="h-12 w-12 rounded-lg bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-zinc-400">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M3 9h18M9 21V9" />
          </svg>
        </div>
        <div>
          <h4 className="text-sm font-medium text-zinc-500 dark:text-zinc-400">{label}</h4>
          <div className="text-base font-semibold text-zinc-900 dark:text-zinc-100 truncate max-w-[200px]">
            {component ? component.name : "Not Selected"}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {component && (
          <Button variant="ghost" size="sm" onClick={onRemove} aria-label={`Remove ${component.name}`}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
            </svg>
          </Button>
        )}
        <Button variant={component ? "secondary" : "primary"} size="sm" onClick={onSelect}>
          {component ? "Change" : "Select"}
        </Button>
      </div>
    </Card>
  );
}
