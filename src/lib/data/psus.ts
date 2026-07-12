import psusData from "../../../public/data/psus.json";
import { PSU } from "./types";

function normalizePSU(item: Record<string, unknown>): PSU {
  return {
    id: (item.id as string) || "",
    slug: (item.slug as string) || "",
    name: (item.name as string) || "Unknown",
    manufacturer: (item.manufacturer as string) || "Unknown",
    image: (item.image as string) || "",
    officialUrl: (item.officialUrl as string) || "",
    releaseDate: (item.releaseDate as string) || "2023-01-01",
    msrp: (item.msrp as number) || 0,
    description: (item.description as string) || "",
    prices: (item.prices as PSU["prices"]) || [],
    wattage: (item.wattage as number) || 0,
    efficiencyRating: (item.efficiencyRating as PSU["efficiencyRating"]) || "80+ Gold",
    modularType: (item.modularType as PSU["modularType"]) || "Full",
    fanSize: (item.fanSize as number) || 120,
    length: (item.length as number) || 140,
    cpuConnectors: (item.cpuConnectors as number) || 2,
    gpuConnectors: (item.gpuConnectors as number) || 4,
    sataConnectors: (item.sataConnectors as number) || 6,
    molexConnectors: (item.molexConnectors as number) || 2,
    atxVersion: (item.atxVersion as string) || "ATX 3.0",
    type: "psu",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getPSUs(): Promise<PSU[]> {
  return (psusData as Record<string, unknown>[]).map(normalizePSU);
}

export async function getPSUBySlug(slug: string): Promise<PSU | null> {
  const found = (psusData as Record<string, unknown>[]).find((p) => p.slug === slug);
  return found ? normalizePSU(found) : null;
}
