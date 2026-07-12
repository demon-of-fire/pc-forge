import cpusData from "../../../public/data/cpus.json";
import { CPU } from "./types";

function normalizeCPU(item: Record<string, unknown>): CPU {
  const manufacturer = (item.manufacturer as string) || "Unknown";
  return {
    id: (item.id as string) || "",
    slug: (item.slug as string) || "",
    name: (item.name as string) || "Unknown",
    manufacturer: manufacturer as CPU["manufacturer"],
    image: (item.image as string) || "",
    officialUrl: (item.officialUrl as string) || "",
    releaseDate: (item.releaseDate as string) || "2023-01-01",
    msrp: (item.msrp as number) || 0,
    description: (item.description as string) || "",
    prices: (item.prices as CPU["prices"]) || [],
    generation: (item.generation as string) || "",
    architecture: (item.architecture as string) || "",
    socket: (item.socket as CPU["socket"]) || "AM5",
    cores: (item.cores as number) || 0,
    threads: (item.threads as number) || 0,
    baseFrequency: (item.baseFrequency as number) || 0,
    boostFrequency: (item.boostFrequency as number) || 0,
    cache: (item.cache as string) || "",
    integratedGraphics: (item.integratedGraphics as string) || null,
    tdp: (item.tdp as number) || 0,
    gamingScore: (item.gamingScore as number) || 0,
    productivityScore: (item.productivityScore as number) || 0,
    aiScore: (item.aiScore as number) || 0,
    advantages: (item.advantages as string[]) || [],
    disadvantages: (item.disadvantages as string[]) || [],
    type: "cpu",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getCPUs(): Promise<CPU[]> {
  return (cpusData as Record<string, unknown>[]).map(normalizeCPU);
}

export async function getCPUBySlug(slug: string): Promise<CPU | null> {
  const found = (cpusData as Record<string, unknown>[]).find((c) => c.slug === slug);
  return found ? normalizeCPU(found) : null;
}
