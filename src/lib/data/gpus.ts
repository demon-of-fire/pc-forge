import gpusData from "../../../public/data/gpus.json";
import { GPU } from "./types";

export async function getGPUs(): Promise<GPU[]> {
  return gpusData as GPU[];
}

export async function getGPUBySlug(slug: string): Promise<GPU | null> {
  return (gpusData as GPU[]).find((gpu) => gpu.slug === slug) || null;
}
