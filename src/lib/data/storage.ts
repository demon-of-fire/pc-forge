import storageData from "../../../public/data/storage.json";
import { Storage } from "./types";

function normalizeStorage(item: Record<string, unknown>): Storage {
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
    prices: (item.prices as Storage["prices"]) || [],
    capacity: (item.capacity as number) || 0,
    interface: (item.interface as Storage["interface"]) || "NVMe",
    readSpeed: (item.readSpeed as number) || 0,
    writeSpeed: (item.writeSpeed as number) || 0,
    nandType: (item.nandType as Storage["nandType"]) || "TLC",
    formFactor: (item.formFactor as string) || "M.2",
    tbw: (item.tbw as number | null) || null,
    type: "storage",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getStorage(): Promise<Storage[]> {
  return (storageData as Record<string, unknown>[]).map(normalizeStorage);
}

export async function getStorageBySlug(slug: string): Promise<Storage | null> {
  const found = (storageData as Record<string, unknown>[]).find((s) => s.slug === slug);
  return found ? normalizeStorage(found) : null;
}
