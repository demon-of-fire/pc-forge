import cpusData from "../../../public/data/cpus.json";
import { CPU } from "./types";

export async function getCPUs(): Promise<CPU[]> {
  return cpusData as CPU[];
}

export async function getCPUBySlug(slug: string): Promise<CPU | null> {
  return (cpusData as CPU[]).find((cpu) => cpu.slug === slug) || null;
}
