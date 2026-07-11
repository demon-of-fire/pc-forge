import { BuildTotals } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";

interface BuildSummaryProps {
  totals: BuildTotals;
}

export function BuildSummary({ totals }: BuildSummaryProps) {
  return (
    <Card className="p-6 bg-zinc-50 dark:bg-zinc-900 border-blue-200 dark:border-blue-900">
      <h3 className="text-lg font-bold text-zinc-900 dark:text-zinc-100 mb-6">Build Summary</h3>
      
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <span className="text-sm text-zinc-500 dark:text-zinc-400">Total Estimated Price</span>
          <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            £{totals.price.toFixed(2)}
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-zinc-500 dark:text-zinc-400">Estimated Power Draw</span>
          <span className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
            {totals.powerConsumption}W
          </span>
        </div>

        <div className="pt-6 border-t border-zinc-200 dark:border-zinc-800">
          <h4 className="text-xs font-semibold text-zinc-400 uppercase mb-3">Retailer Breakdown</h4>
          <div className="space-y-2">
            {Object.entries(totals.priceByRetailer).map(([retailer, price]) => (
              <div key={retailer} className="flex items-center justify-between text-sm">
                <span className="text-zinc-600 dark:text-zinc-400">{retailer}</span>
                <span className="font-medium text-zinc-900 dark:text-zinc-100">£{price.toFixed(2)}</span>
              </div>
            ))}
            {Object.keys(totals.priceByRetailer).length === 0 && (
              <p className="text-xs text-zinc-400 italic">No retailers available</p>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
}
