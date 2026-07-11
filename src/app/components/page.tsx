import Link from "next/link";
import { Card } from "@/components/ui/Card";

const categories = [
  {
    id: "cpus",
    name: "Processors",
    description: "The brain of your computer. Compare performance and cores.",
    href: "/components/cpus/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    id: "gpus",
    name: "Graphics Cards",
    description: "Power your visuals and AI workloads with the latest GPUs.",
    href: "/components/gpus/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="2" y="6" width="20" height="12" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="7" cy="12" r="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="2" stroke="currentColor" strokeWidth="1.5" />
      </svg>
    ),
  },
  {
    id: "motherboards",
    name: "Motherboards",
    description: "The backbone of your PC. Check sockets and chipsets.",
    href: "/components/motherboards/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <rect x="7" y="7" width="4" height="4" stroke="currentColor" strokeWidth="1.5" />
        <rect x="13" y="7" width="4" height="4" stroke="currentColor" strokeWidth="1.5" />
        <rect x="7" y="13" width="4" height="4" stroke="currentColor" strokeWidth="1.5" />
      </svg>
    ),
  },
  {
    id: "ram",
    name: "Memory (RAM)",
    description: "Speed up your multitasking with high-speed DDR5 memory.",
    href: "/components/ram/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M8 8v2M12 8v2M16 8v2M8 14v2M12 14v2M16 14v2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    id: "storage",
    name: "Storage",
    description: "Fast NVMe SSDs and high-capacity HDDs for your data.",
    href: "/components/storage/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="1" fill="currentColor" />
      </svg>
    ),
  },
  {
    id: "psus",
    name: "Power Supplies",
    description: "Ensure stable power with high-efficiency PSU units.",
    href: "/components/psus/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="3" y="6" width="18" height="12" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M7 10l2 2 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    id: "cases",
    name: "Cases",
    description: "Protect your hardware with a stylish and airy chassis.",
    href: "/components/cases/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <rect x="4" y="2" width="16" height="20" rx="2" stroke="currentColor" strokeWidth="1.5" />
        <circle cx="12" cy="17" r="2" stroke="currentColor" strokeWidth="1.5" />
        <path d="M8 6h8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    id: "cooling",
    name: "Cooling",
    description: "Keep your components cool with Air or AIO liquid coolers.",
    href: "/components/cooling/",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-8 w-8" aria-hidden="true">
        <path d="M12 3v4M12 17v4M3 12h4M17 12h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth="1.5" />
        <path d="M12 8a4 4 0 014 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
  },
];

export default function ComponentsHub() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-4xl">
          Hardware Browser
        </h1>
        <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400">
          Select a category to explore the latest components and compare specs.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {categories.map((cat) => (
          <Link
            key={cat.id}
            href={cat.href}
            className="group"
          >
            <Card
              hover
              className="h-full flex flex-col p-6 transition-all group-hover:border-blue-500 group-hover:ring-1 group-hover:ring-blue-500"
            >
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-zinc-100 text-zinc-600 transition-colors group-hover:bg-blue-600 group-hover:text-white dark:bg-zinc-800 dark:text-zinc-400 dark:group-hover:bg-blue-600 dark:group-hover:text-white">
                {cat.icon}
              </div>
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100 mb-2">
                {cat.name}
              </h3>
              <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
                {cat.description}
              </p>
              <div className="mt-auto flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400">
                Browse components
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="transition-transform group-hover:translate-x-1">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
