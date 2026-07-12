import ramData from "../../../public/data/ram.json";
import { RAM } from "./types";

function normalizeRAM(item: Record<string, unknown>): RAM {
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
    prices: (item.prices as RAM["prices"]) || [],
    capacity: (item.capacity as number) || 0,
    speed: (item.speed as number) || 0,
    ddrGeneration: (item.ddrGeneration as RAM["ddrGeneration"]) || "DDR5",
    casLatency: (item.casLatency as number) || 0,
    kitSize: (item.kitSize as number) || 1,
    modules: (item.modules as string) || "",
    voltage: (item.voltage as number) || 1.2,
    heatspreader: (item.heatspreader as boolean) || false,
    rgb: (item.rgb as boolean) || false,
    type: "ram",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getRAM(): Promise<RAM[]> {
  return (ramData as Record<string, unknown>[]).map(normalizeRAM);
}

export async function getRAMBySlug(slug: string): Promise<RAM | null> {
  const found = (ramData as Record<string, unknown>[]).find((r) => r.slug === slug);
  return found ? normalizeRAM(found) : null;
}
