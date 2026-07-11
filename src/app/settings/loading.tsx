import { Skeleton } from "@/components/ui/Skeleton";

export default function SettingsLoading() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center space-y-4">
        <Skeleton className="mx-auto h-8 w-40" variant="text" />
        <Skeleton className="mx-auto h-4 w-64" variant="text" />
      </div>

      <div className="space-y-8">
        <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
          <div className="flex items-center justify-between mb-6">
            <div className="space-y-2">
              <Skeleton className="h-5 w-32" variant="text" />
              <Skeleton className="h-3 w-48" variant="text" />
            </div>
            <Skeleton className="h-5 w-24 rounded-full" />
          </div>
          <div className="flex gap-3">
            <Skeleton className="h-10 flex-1 rounded-xl" />
            <Skeleton className="h-10 flex-1 rounded-xl" />
            <Skeleton className="h-10 flex-1 rounded-xl" />
          </div>
        </div>

        <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
          <div className="space-y-2 mb-6">
            <Skeleton className="h-5 w-32" variant="text" />
            <Skeleton className="h-3 w-64" variant="text" />
          </div>
          <div className="space-y-3">
            <Skeleton className="h-14 w-full rounded-lg" />
            <Skeleton className="h-14 w-full rounded-lg" />
          </div>
        </div>
      </div>
    </div>
  );
}
