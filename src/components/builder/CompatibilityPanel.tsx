import { CompatibilityResult } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

interface CompatibilityPanelProps {
  results: CompatibilityResult[];
}

export function CompatibilityPanel({ results }: CompatibilityPanelProps) {
  if (results.length === 0) {
    return (
      <Card className="p-6 text-center">
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Select components to check compatibility.
        </p>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase mb-4">
        Compatibility Check
      </h3>
      {results.map((res, i) => (
        <Card key={i} className="p-4 flex items-start gap-4 border-zinc-200 dark:border-zinc-800">
          <div
            className={
              res.status === "compatible" ? "text-green-500" :
              res.status === "warning" ? "text-yellow-500" : "text-red-500"
            }
            role="img"
            aria-label={res.status === "compatible" ? "Compatible" : res.status === "warning" ? "Warning" : "Incompatible"}
          >
            {res.status === "compatible" && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            )}
            {res.status === "warning" && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                <line x1="12" y1="9" x2="12" y2="13" />
                <line x1="12" y1="17" x2="12.01" y2="17" />
              </svg>
            )}
            {res.status === "incompatible" && (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="10" />
                <line x1="15" y1="//9" x2="//9" y2="15" />
              </svg>
            )}
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm font-bold text-zinc-900 dark:text-zinc-100">{res.check}</span>
              <Badge variant={
                res.status === "compatible" ? "success" : 
                res.status === "warning" ? "warning" : "danger"
              }>
                {res.status}
              </Badge>
            </div>
            <p className="text-sm text-zinc-700 dark:text-zinc-300 font-medium">{res.message}</p>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{res.details}</p>
          </div>
        </Card>
      ))}
    </div>
  );
}
