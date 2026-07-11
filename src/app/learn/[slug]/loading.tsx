import { Skeleton } from "@/components/ui/Skeleton";

export default function ArticleLoading() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <Skeleton className="h-4 w-48 mb-8" variant="text" />

      <div className="mb-8 space-y-4">
        <Skeleton className="h-5 w-20 rounded-full" />
        <Skeleton className="h-10 w-full" variant="text" />
        <Skeleton className="h-5 w-3/4" variant="text" />
      </div>

      <div className="space-y-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-4 w-full" variant="text" />
        ))}
        <Skeleton className="h-4 w-5/6" variant="text" />
        <Skeleton className="h-4 w-2/3" variant="text" />
      </div>
    </div>
  );
}
