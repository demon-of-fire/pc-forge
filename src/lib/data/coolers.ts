import coolersData from "../../../public/data/coolers.json";
import { Cooler } from "./types";

export async function getCoolers(): Promise<Cooler[]> {
  return coolersData as Cooler[];
}

export async function getCoolerBySlug(slug: string): Promise<Cooler | null> {
  return (coolersData as Cooler[]).find((c) => c.slug === slug) || null;
}
