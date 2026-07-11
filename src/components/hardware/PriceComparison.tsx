import { Component } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/lib/utils/cn";

interface PriceComparisonProps {
  component: Component;
}

export function PriceComparison({ component }: PriceComparisonProps) {
  const prices = component.prices;
  const averagePrice = prices.reduce((acc, p) => acc + p.price, 0) / prices.length;

  return (
    <Card className="p-6">
      <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase mb-4">
        Price Comparison
      </h3>
      <div className="space-y-3">
        {prices.map((price, i) => (
          <div
            key={i}
            className={cn(
              "flex items-center justify-between p-3 rounded-lg border",
              i === 0 ? "border-green-500 bg-green-50 dark:bg-green-900/20" : "border-zinc-200 dark:border-zinc-800"
            )}
          >
            <div className="flex items-center gap-3">
              {i === 0 && (
                <Badge variant="success">Cheapest</Badge>
              )}
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {price.retailer}
              </span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
                £{price.price.toFixed(2)}
              </span>
              <a
                href={price.url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-1.5 rounded-md bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-400 dark:hover:bg-zinc-700"
                aria-label={`View ${price.retailer} offer`}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
                  <polyline points="15 3 21 3 21 9" />
                  <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
              </a>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6 pt-4 border-t border-zinc-200 dark:border-zinc-800 flex justify-between items-center">
        <span className="text-sm text-zinc-500 dark:text-zinc-400">Average Market Price:</span>
        <span className="text-sm font-bold text-zinc-900 dark:text-zinc-100">
          £{averagePrice.toFixed(2)}
        </span>
      </div>
    </Card>
  );
}
