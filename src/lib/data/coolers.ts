import coolersData from "../../../public/data/coolers.json";
import { Cooler } from "./types";

function normalizeCooler(item: Record<string, unknown>): Cooler {
  const manufacturer = (item.manufacturer as string) || "Unknown";
  return {
    id: (item.id as string) || "",
    slug: (item.slug as string) || "",
    name: (item.name as string) || "Unknown",
    manufacturer: manufacturer as Cooler["manufacturer"],
    image: (item.image as string) || "",
    officialUrl: (item.officialUrl as string) || "",
    releaseDate: (item.releaseDate as string) || "2023-01-01",
    msrp: (item.msrp as number) || 0,
    description: (item.description as string) || "",
    prices: (item.prices as Cooler["prices"]) || [],
    coolerType: (item.coolerType as Cooler["coolerType"]) || "Air",
    socketCompatibility: (item.socketCompatibility as Cooler["socketCompatibility"]) || [],
    height: (item.height as number | null) || null,
    fanSize: (item.fanSize as number | null) || null,
    fanCount: (item.fanCount as number) || 1,
    radiatorSize: (item.radiatorSize as number | null) || null,
    coolingCapacity: (item.coolingCapacity as number) || 0,
    noiseLevel: (item.noiseLevel as number) || 0,
    tdpRating: (item.tdpRating as number) || 0,
    type: "cooler",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getCoolers(): Promise<Cooler[]> {
  return (coolersData as Record<string, unknown>[]).map(normalizeCooler);
}

export async function getCoolerBySlug(slug: string): Promise<Cooler | null> {
  const found = (coolersData as Record<string, unknown>[]).find((c) => c.slug === slug);
  return found ? normalizeCooler(found) : null;
}
