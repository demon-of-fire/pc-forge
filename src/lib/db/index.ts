import Dexie, { type Table } from "dexie";
import { PCBuild } from "@/lib/data/types";

export interface SavedBuild extends PCBuild {
  id: string; // IndexedDB key
  name: string;
  createdAt: string;
  updatedAt: string;
}

export class PCForgeDB extends Dexie {
  builds!: Table<SavedBuild>;

  constructor() {
    super("PCForgeDB");
    this.version(1).stores({
      builds: "id, name, createdAt",
    });
  }
}

export const db = new PCForgeDB();
