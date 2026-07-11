import { 
  getCPUs, getGPUs, getMotherboards, getRAM, 
  getStorage, getPSUs, getCases, getCoolers 
} from "@/lib/data";
import { ComponentDetail } from "@/components/hardware/ComponentDetail";
import { PriceComparison } from "@/components/hardware/PriceComparison";
import { notFound } from "next/navigation";
import Link from "next/link";
import { Component } from "@/lib/data/types";

const categoryMap: Record<string, { 
  loader: () => Promise<Component[]> 
}> = {
  cpus: { loader: getCPUs },
  gpus: { loader: getGPUs },
  motherboards: { loader: getMotherboards },
  ram: { loader: getRAM },
  storage: { loader: getStorage },
  psus: { loader: getPSUs },
  cases: { loader: getCases },
  cooling: { loader: getCoolers },
};

export async function generateStaticParams() {
  const paths: { category: string; slug: string }[] = [];
  for (const [category, config] of Object.entries(categoryMap)) {
    const components = await config.loader();
    components.forEach((comp) => {
      paths.push({
        category: category,
        slug: comp.slug,
      });
    });
  }
  return paths;
}

export default async function ComponentDetailPage({ params }: { params: Promise<{ category: string; slug: string }> }) {
  const { category, slug } = await params;
  const config = categoryMap[category];

  if (!config) notFound();

  const components = await config.loader();
  const component = components.find((c) => c.slug === slug);

  if (!component) notFound();

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-8">
        <nav className="flex items-center gap-2 text-sm text-zinc-500 dark:text-zinc-400 mb-4">
          <Link href="/components/" className="hover:text-blue-600 dark:hover:text-blue-400">Components</Link>
          <span>/</span>
          <Link href={`/components/${category}/`} className="hover:text-blue-600 dark:hover:text-blue-400 capitalize">{category}</Link>
          <span>/</span>
          <span className="text-zinc-900 dark:text-zinc-100 truncate">{component.name}</span>
        </nav>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2">
          <ComponentDetail component={component} />
        </div>
        <div className="lg:col-span-1">
          <PriceComparison component={component} />
        </div>
      </div>
    </div>
  );
}
