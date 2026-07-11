import storageData from "../../../public/data/storage.json";
import { Storage } from "./types";

export async function getStorage(): Promise<Storage[]> {
  return storageData as Storage[];
}

export async function getStorageBySlug(slug: string): Promise<Storage | null> {
  return (storageData as Storage[]).find((s) => s.slug === slug) || null;
}
