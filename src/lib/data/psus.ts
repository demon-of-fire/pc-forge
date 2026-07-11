import psusData from "../../../public/data/psus.json";
import { PSU } from "./types";

export async function getPSUs(): Promise<PSU[]> {
  return psusData as PSU[];
}

export async function getPSUBySlug(slug: string): Promise<PSU | null> {
  return (psusData as PSU[]).find((psu) => psu.slug === slug) || null;
}
