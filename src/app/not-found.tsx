import Link from "next/link";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800">
        <span className="text-4xl font-bold text-zinc-400 dark:text-zinc-500">404</span>
      </div>
      <h1 className="mb-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
        Page Not Found
      </h1>
      <p className="mb-8 max-w-md text-zinc-500 dark:text-zinc-400">
        The page you&apos;re looking for doesn&apos;t exist or has been moved. Let&apos;s get you back on track.
      </p>
      <div className="flex gap-3">
        <Link href="/">
          <Button variant="primary">Go Home</Button>
        </Link>
        <Link href="/build/">
          <Button variant="outline">Start Building</Button>
        </Link>
      </div>
    </div>
  );
}
