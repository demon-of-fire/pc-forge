"use client";

import { useLiveQuery } from "dexie-react-hooks";
import { db, type SavedBuild } from "@/lib/db";
import { useBuildContext } from "@/context/BuildContext";

export function useSavedBuilds() {
  const { components } = useBuildContext();
  
  const savedBuilds = useLiveQuery(() => db.builds.toArray());

  const saveBuild = async (name: string) => {
    const id = crypto.randomUUID();
    const newBuild: SavedBuild = {
      id,
      name,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      components: { ...components },
    };
    await db.builds.add(newBuild);
    return id;
  };

  const updateBuild = async (id: string, name: string) => {
    await db.builds.update(id, {
      name,
      updatedAt: new Date().toISOString(),
      components: { ...components },
    });
  };

  const deleteBuild = async (id: string) => {
    await db.builds.delete(id);
  };

  const loadBuild = async (id: string) => {
    const build = await db.builds.get(id);
    return build;
  };

  return {
    savedBuilds,
    saveBuild,
    updateBuild,
    deleteBuild,
    loadBuild,
  };
}
