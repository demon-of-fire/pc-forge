import gpusData from "../../../public/data/gpus.json";
import { GPU } from "./types";

function normalizeGPU(item: Record<string, unknown>): GPU {
  const manufacturer = (item.manufacturer as string) || "Unknown";
  return {
    id: (item.id as string) || "",
    slug: (item.slug as string) || "",
    name: (item.name as string) || "Unknown",
    manufacturer: manufacturer as GPU["manufacturer"],
    image: (item.image as string) || "",
    officialUrl: (item.officialUrl as string) || "",
    releaseDate: (item.releaseDate as string) || "2023-01-01",
    msrp: (item.msrp as number) || 0,
    description: (item.description as string) || "",
    prices: (item.prices as GPU["prices"]) || [],
    chipset: (item.chipset as string) || "",
    vramAmount: (item.vramAmount as number) || 0,
    memoryType: (item.memoryType as string) || "",
    memoryBus: (item.memoryBus as number) || 0,
    cudaCores: (item.cudaCores as number) || 0,
    rtCores: (item.rtCores as number) || 0,
    tensorCores: (item.tensorCores as number) || 0,
    baseClock: (item.baseClock as number) || 0,
    boostClock: (item.boostClock as number) || 0,
    powerConsumption: (item.powerConsumption as number) || 0,
    recommendedPsu: (item.recommendedPsu as number) || 0,
    pcieVersion: (item.pcieVersion as GPU["pcieVersion"]) || "PCIe 4.0",
    resolutionTargets: (item.resolutionTargets as GPU["resolutionTargets"]) || { "1080p": 0, "1440p": 0, "4K": 0 },
    gamingScore: (item.gamingScore as number) || 0,
    rayTracingScore: (item.rayTracingScore as number) || 0,
    aiScore: (item.aiScore as number) || 0,
    advantages: (item.advantages as string[]) || [],
    disadvantages: (item.disadvantages as string[]) || [],
    type: "gpu",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getGPUs(): Promise<GPU[]> {
  return (gpusData as Record<string, unknown>[]).map(normalizeGPU);
}

export async function getGPUBySlug(slug: string): Promise<GPU | null> {
  const found = (gpusData as Record<string, unknown>[]).find((g) => g.slug === slug);
  return found ? normalizeGPU(found) : null;
}
