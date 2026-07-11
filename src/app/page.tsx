import Link from "next/link";

const componentCategories = [
  {
    name: "CPUs",
    href: "/components/cpus/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    name: "GPUs",
    href: "/components/gpus/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="2" y="6" width="20" height="12" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="7" cy="12" r="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="2" stroke="currentColor" strokeWidth="1.5" />
      </svg>
    ),
  },
  {
    name: "Motherboards",
    href: "/components/motherboards/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <rect x="7" y="7" width="4" height="4" stroke="currentColor" strokeWidth="1.5" />
        <rect x="13" y="7" width="4" height="4" stroke="currentColor" strokeWidth="1.5" />
        <rect x="7" y="13" width="4" height="4" stroke="currentColor" strokeWidth="1.5" />
      </svg>
    ),
  },
  {
    name: "RAM",
    href: "/components/ram/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M8 8v2M12 8v2M16 8v2M8 14v2M12 14v2M16 14v2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    name: "Storage",
    href: "/components/storage/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="1" fill="currentColor" />
      </svg>
    ),
  },
  {
    name: "PSUs",
    href: "/components/psus/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="3" y="6" width="18" height="12" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M7 10l2 2 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    name: "Cases",
    href: "/components/cases/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <rect x="4" y="2" width="16" height="20" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="17" r="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M8 6h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    name: "Cooling",
    href: "/components/cooling/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6" aria-hidden="true">
        <path d="M12 3v4M12 17v4M3 12h4M17 12h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth="1.5" />
        <path d="M12 8a4 4 0 014 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
];

const featuredBuilds = [
  {
    name: "Budget Gaming Build",
    description: "Solid 1080p gaming performance without breaking the bank.",
    price: "From ~£600",
    tag: "Budget",
  },
  {
    name: "Mid-Range Powerhouse",
    description: "Excellent 1440p gaming and productivity performance.",
    price: "From ~£1,200",
    tag: "Mid-Range",
  },
  {
    name: "Ultimate Workstation",
    description: "Top-tier performance for gaming, streaming, and content creation.",
    price: "From ~£2,500",
    tag: "High-End",
  },
];

const beginnerGuides = [
  {
    title: "How to Choose a CPU",
    description: "Understand cores, threads, and what matters for your use case.",
    href: "/learn/",
  },
  {
    title: "What is VRAM?",
    description: "Why GPU memory matters and how much you actually need.",
    href: "/learn/",
  },
  {
    title: "Understanding PSU Ratings",
    description: "80+ Bronze, Gold, Platinum — what do they actually mean?",
    href: "/learn/",
  },
  {
    title: "DDR4 vs DDR5",
    description: "Is the upgrade worth it? A beginner-friendly comparison.",
    href: "/learn/",
  },
];

export default function HomePage() {
  return (
    <>
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-zinc-50 dark:from-blue-950/20 dark:via-zinc-950 dark:to-zinc-950" />
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-4xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-6xl">
              Build your{" "}
              <span className="bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent">
                perfect PC
              </span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-zinc-600 dark:text-zinc-400">
              The open-source PC building platform. Browse thousands of components, check compatibility,
              compare prices, and build your dream machine — all without creating an account.
            </p>
            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                href="/build/"
                className="inline-flex h-12 items-center justify-center rounded-xl bg-blue-600 px-6 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
              >
                Start Building
              </Link>
              <Link
                href="/components/"
                className="inline-flex h-12 items-center justify-center rounded-xl border border-zinc-300 bg-white px-6 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
              >
                Browse Components
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
          Browse by Category
        </h2>
        <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {componentCategories.map((cat) => (
            <Link
              key={cat.name}
              href={cat.href}
              className="group flex items-center gap-3 rounded-xl border border-zinc-200 bg-white p-4 transition-all hover:shadow-lg hover:shadow-zinc-200/50 hover:border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700 dark:hover:shadow-zinc-900/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-zinc-100 text-zinc-600 transition-colors group-hover:bg-blue-50 group-hover:text-blue-600 dark:bg-zinc-800 dark:text-zinc-400 dark:group-hover:bg-blue-900/30 dark:group-hover:text-blue-400">
                {cat.icon}
              </div>
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {cat.name}
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
          Featured Builds
        </h2>
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featuredBuilds.map((build) => (
            <div
              key={build.name}
              className="rounded-xl border border-zinc-200 bg-white p-6 transition-all hover:shadow-lg hover:shadow-zinc-200/50 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:shadow-zinc-900/50"
            >
              <div className="flex items-center gap-2">
                <span className="inline-flex rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                  {build.tag}
                </span>
              </div>
              <h3 className="mt-3 text-lg font-semibold text-zinc-900 dark:text-zinc-100">
                {build.name}
              </h3>
              <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
                {build.description}
              </p>
              <p className="mt-4 text-sm font-medium text-zinc-700 dark:text-zinc-300">
                {build.price}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
          Beginner Guides
        </h2>
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          {beginnerGuides.map((guide) => (
            <Link
              key={guide.title}
              href={guide.href}
              className="group rounded-xl border border-zinc-200 bg-white p-5 transition-all hover:shadow-lg hover:shadow-zinc-200/50 hover:border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700 dark:hover:shadow-zinc-900/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
            >
              <h3 className="font-semibold text-zinc-900 group-hover:text-blue-600 dark:text-zinc-100 dark:group-hover:text-blue-400">
                {guide.title}
              </h3>
              <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
                {guide.description}
              </p>
              <span className="mt-3 inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400">
                Learn more
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
                  <path d="M5 3l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="rounded-2xl bg-zinc-900 p-8 sm:p-12 dark:bg-zinc-100">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-2xl font-bold text-white sm:text-3xl dark:text-zinc-900">
              Open Source and Free
            </h2>
            <p className="mt-4 text-zinc-400 dark:text-zinc-600">
              PCForge is built by the community, for the community. No accounts, no paywalls, no tracking.
              Your data stays on your device. Everything is transparent.
            </p>
            <div className="mt-8 flex justify-center gap-4">
              <Link
                href="/build/"
                className="inline-flex h-12 items-center justify-center rounded-xl bg-white px-6 text-sm font-medium text-zinc-900 transition-colors hover:bg-zinc-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 dark:bg-zinc-900 dark:text-zinc-100 dark:hover:bg-zinc-800 dark:focus-visible:ring-zinc-900"
              >
                Start Building Now
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
