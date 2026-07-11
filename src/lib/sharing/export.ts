import { PCBuild } from "@/lib/data/types";

export function exportBuildToJson(build: PCBuild): string {
  return JSON.stringify(build, null, 2);
}

export function importBuildFromJson(json: string): PCBuild | null {
  try {
    const build = JSON.parse(json) as PCBuild;
    if (!build.id || !build.components) return null;
    return build;
  } catch (e) {
    console.error("Failed to import build JSON:", e);
    return null;
  }
}
