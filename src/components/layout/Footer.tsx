import Link from "next/link";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900/50" role="contentinfo">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <Link href="/" className="flex items-center gap-2 font-bold text-lg text-zinc-900 dark:text-zinc-100">
              <svg width="24" height="24" viewBox="0 0 28 28" fill="none" aria-hidden="true" className="text-blue-600">
                <rect x="2" y="2" width="24" height="24" rx="6" fill="currentColor" />
                <path d="M8 10h12M8 14h8M8 18h10" stroke="white" strokeWidth="2" strokeLinecap="round" />
              </svg>
              PCForge
            </Link>
            <p className="mt-3 text-sm text-zinc-500 dark:text-zinc-400">
              The open-source PC building platform. Build, compare, and discover hardware.
            </p>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Build</h3>
            <ul className="mt-3 space-y-2">
              <li><Link href="/build/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">PC Builder</Link></li>
              <li><Link href="/components/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">Browse Components</Link></li>
              <li><Link href="/compare/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">Compare</Link></li>
              <li><Link href="/saved/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">Saved Builds</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Hardware</h3>
            <ul className="mt-3 space-y-2">
              <li><Link href="/components/cpus/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">CPUs</Link></li>
              <li><Link href="/components/gpus/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">GPUs</Link></li>
              <li><Link href="/components/motherboards/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">Motherboards</Link></li>
              <li><Link href="/components/ram/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">RAM</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Learn</h3>
            <ul className="mt-3 space-y-2">
              <li><Link href="/learn/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">Hardware Guides</Link></li>
              <li><Link href="/settings/" className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200">Settings</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-10 border-t border-zinc-200 pt-6 dark:border-zinc-800">
          <p className="text-center text-sm text-zinc-400 dark:text-zinc-500">
            Open source. Built by the community. Not affiliated with any hardware manufacturer.
          </p>
        </div>
      </div>
    </footer>
  );
}
