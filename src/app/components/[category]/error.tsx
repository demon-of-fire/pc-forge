"use client";

import { useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function CategoryError({
  error,
  unstable_retry,
}: {
  error: Error & { digest?: string };
  unstable_retry: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <h1 className="mb-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
        Failed to Load Components
      </h1>
      <p className="mb-8 max-w-md text-zinc-500 dark:text-zinc-400">
        There was an issue loading the hardware data. Please try again.
      </p>
      <div className="flex gap-3">
        <Button variant="primary" onClick={() => unstable_retry()}>
          Try Again
        </Button>
        <Link href="/components/">
          <Button variant="outline">All Components</Button>
        </Link>
      </div>
    </div>
  );
}
