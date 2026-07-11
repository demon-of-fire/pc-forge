import { getCPUs, getGPUs, getMotherboards, getRAM, getStorage, getPSUs, getCases, getCoolers } from "@/lib/data";
import { CategoryBrowser } from "@/components/hardware/pages/CategoryBrowser";
import { Component } from "@/lib/data/types";

const categoryMap: Record<string, { 
  label: string; 
  loader: () => Promise<Component[]> 
}> = {
  cpus: { label: "CPUs", loader: getCPUs },
  gpus: { label: "GPUs", loader: getGPUs },
  motherboards: { label: "Motherboards", loader: getMotherboards },
  ram: { label: "RAM", loader: getRAM },
  storage: { label: "Storage", loader: getStorage },
  psus: { label: "PSUs", loader: getPSUs },
  cases: { label: "Cases", loader: getCases },
  cooling: { label: "Cooling", loader: getCoolers },
};

export async function generateStaticParams() {
  return Object.keys(categoryMap).map((cat) => ({
    category: cat,
  }));
}

export default async function CategoryPage({ params }: { params: Promise<{ category: string }> }) {
  const { category } = await params;
  const config = categoryMap[category];

  if (!config) {
    return <div className="p-12 text-center">Category not found</div>;
  }

  const components = await config.loader();

  return (
    <CategoryBrowser 
      category={category} 
      initialComponents={components} 
      label={config.label} 
    />
  );
}
