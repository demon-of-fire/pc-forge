import { Skeleton } from "@/components/ui/Skeleton";

export default function CategoryLoading() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-8 flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
        <div className="flex-1 space-y-3">
          <Skeleton className="h-5 w-20 rounded-full" />
          <Skeleton className="h-8 w-48" variant="text" />
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:flex lg:items-center lg:gap-4">
          <Skeleton className="h-10 w-64 rounded-xl" />
          <Skeleton className="h-10 w-40 rounded-xl" />
          <Skeleton className="h-10 w-48 rounded-xl" />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
            <Skeleton className="aspect-[4/3] w-full rounded-lg mb-4" />
            <Skeleton className="h-4 w-3/4 mb-2" variant="text" />
            <Skeleton className="h-3 w-1/2 mb-4" variant="text" />
            <div className="flex gap-2">
              <Skeleton className="h-6 w-16 rounded-full" />
              <Skeleton className="h-6 w-16 rounded-full" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
