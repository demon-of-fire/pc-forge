import motherboardsData from "../../../public/data/motherboards.json";
import { Motherboard } from "./types";

export async function getMotherboards(): Promise<Motherboard[]> {
  return motherboardsData as Motherboard[];
}

export async function getMotherboardBySlug(slug: string): Promise<Motherboard | null> {
  return (motherboardsData as Motherboard[]).find((mb) => mb.slug === slug) || null;
}
