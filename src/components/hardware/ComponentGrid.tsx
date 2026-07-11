import { Component, ComponentType } from "@/lib/data/types";
import { ComponentCard } from "./ComponentCard";

interface ComponentGridProps {
  components: Component[];
  type: ComponentType;
  onSelect?: (component: Component) => void;
}

export function ComponentGrid({ components, type, onSelect }: ComponentGridProps) {
  if (components.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <div className="h-16 w-16 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-zinc-400 mb-4">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">No components found</h3>
        <p className="text-zinc-500 dark:text-zinc-400 max-w-xs mx-auto">
          Try adjusting your filters or search terms.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {components.map((component) => (
        <ComponentCard 
          key={component.id} 
          component={component} 
          type={type} 
          onSelect={onSelect} 
        />
      ))}
    </div>
  );
}
