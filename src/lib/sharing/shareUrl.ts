import { PCBuild } from "@/lib/data/types";

export function encodeBuild(build: PCBuild): string {
  const json = JSON.stringify(build);
  return btoa(encodeURIComponent(json));
}

export function decodeBuild(encoded: string): PCBuild | null {
  try {
    const json = decodeURIComponent(atob(encoded));
    return JSON.parse(json);
  } catch (e) {
    console.error("Failed to decode build:", e);
    return null;
  }
}
