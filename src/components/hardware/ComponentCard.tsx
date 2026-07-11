import { Component, ComponentType } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import Link from "next/link";

interface ComponentCardProps {
  component: Component;
  type: ComponentType;
  onSelect?: (component: Component) => void;
}

export function ComponentCard({ component, type, onSelect }: ComponentCardProps) {
  return (
    <Card hover className="flex flex-col h-full">
      <div className="aspect-square relative overflow-hidden rounded-lg bg-zinc-100 dark:bg-zinc-800 mb-4">
        <img
          src={component.image}
          alt={component.name}
          className="h-full w-full object-cover transition-transform group-hover:scale-105"
          onError={(e) => {
            (e.target as HTMLImageElement).src = "/images/placeholder.jpg";
          }}
        />
      </div>
      <div className="flex flex-col flex-1">
        <div className="flex items-start justify-between gap-2 mb-2">
          <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
            {component.manufacturer}
          </span>
          <Badge variant="default">{component.type === "cpu" ? "CPU" : component.type === "gpu" ? "GPU" : "Part"}</Badge>
        </div>
        <h3 className="text-base font-semibold text-zinc-900 dark:text-zinc-100 line-clamp-2 mb-1">
          {component.name}
        </h3>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 line-clamp-2 mb-4 flex-1">
          {component.description}
        </p>
        <div className="flex items-center justify-between mt-auto pt-4 border-t border-zinc-100 dark:border-zinc-800">
          <div className="flex flex-col">
            <span className="text-xs text-zinc-500 dark:text-zinc-400">Est. Price</span>
            <span className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
              £{Math.min(...component.prices.map(p => p.price)).toFixed(2)}
            </span>
          </div>
          {onSelect ? (
            <Button 
              variant="secondary" 
              size="sm" 
              onClick={(e) => {
                e.preventDefault();
                onSelect(component);
              }}
              aria-label={`Select ${component.name}`}
            >
              Select
            </Button>
          ) : (
            <Link
              href={`/components/${type}/${component.slug}`}
              className="p-2 rounded-lg bg-zinc-100 text-zinc-600 hover:bg-blue-600 hover:text-white transition-colors dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-blue-600 dark:hover:text-white"
              aria-label={`View details for ${component.name}`}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </Link>
          )}
        </div>
      </div>
    </Card>
  );
}
