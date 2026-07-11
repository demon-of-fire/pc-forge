import { Skeleton } from "@/components/ui/Skeleton";

export default function LearnLoading() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center space-y-4">
        <Skeleton className="mx-auto h-8 w-48" variant="text" />
        <Skeleton className="mx-auto h-4 w-80" variant="text" />
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
            <Skeleton className="h-5 w-16 rounded-full mb-4" />
            <Skeleton className="h-6 w-3/4 mb-2" variant="text" />
            <Skeleton className="h-4 w-full mb-2" variant="text" />
            <Skeleton className="h-4 w-2/3" variant="text" />
          </div>
        ))}
      </div>
    </div>
  );
}
