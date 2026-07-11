import ramData from "../../../public/data/ram.json";
import { RAM } from "./types";

export async function getRAM(): Promise<RAM[]> {
  return ramData as RAM[];
}

export async function getRAMBySlug(slug: string): Promise<RAM | null> {
  return (ramData as RAM[]).find((ram) => ram.slug === slug) || null;
}
