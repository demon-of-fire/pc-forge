import casesData from "../../../public/data/cases.json";
import { Case } from "./types";

function normalizeCase(item: Record<string, unknown>): Case {
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
    prices: (item.prices as Case["prices"]) || [],
    formFactor: (item.formFactor as string) || "Mid Tower",
    motherboardSupport: (item.motherboardSupport as Case["motherboardSupport"]) || [],
    gpuClearance: (item.gpuClearance as number) || 0,
    cpuCoolerClearance: (item.cpuCoolerClearance as number) || 0,
    fanSupport: (item.fanSupport as Case["fanSupport"]) || [],
    radiatorSupport: (item.radiatorSupport as string[]) || [],
    driveBays: (item.driveBays as Case["driveBays"]) || { "25 inch": 0, "35 inch": 0 },
    dimensions: (item.dimensions as Case["dimensions"]) || { width: 0, height: 0, depth: 0 },
    weight: (item.weight as number) || 0,
    type: "case",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getCases(): Promise<Case[]> {
  return (casesData as Record<string, unknown>[]).map(normalizeCase);
}

export async function getCaseBySlug(slug: string): Promise<Case | null> {
  const found = (casesData as Record<string, unknown>[]).find((c) => c.slug === slug);
  return found ? normalizeCase(found) : null;
}
