import { Skeleton } from "@/components/ui/Skeleton";

export default function ComponentsHubLoading() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center space-y-4">
        <Skeleton className="mx-auto h-8 w-64" variant="text" />
        <Skeleton className="mx-auto h-4 w-96" variant="text" />
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
            <Skeleton className="h-12 w-12 rounded-lg mb-4" />
            <Skeleton className="h-5 w-24 mb-2" variant="text" />
            <Skeleton className="h-3 w-32" variant="text" />
          </div>
        ))}
      </div>
    </div>
  );
}
