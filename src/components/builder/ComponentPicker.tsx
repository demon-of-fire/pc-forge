"use client";

import { useState, useEffect, useMemo } from "react";
import { Component, ComponentType } from "@/lib/data/types";
import { Modal } from "@/components/ui/Modal";
import { ComponentGrid } from "../hardware/ComponentGrid";
import { ComponentSearch } from "../hardware/ComponentSearch";
import { ComponentFilter } from "../hardware/ComponentFilter";
import { Spinner } from "@/components/ui/Spinner";

interface ComponentPickerProps {
  type: ComponentType;
  onSelect: (component: Component) => void;
  onClose: () => void;
  open: boolean;
}

export function ComponentPicker({ type, onSelect, onClose, open }: ComponentPickerProps) {
  const [components, setComponents] = useState<Component[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [manufacturerFilter, setManufacturerFilter] = useState("all");

  useEffect(() => {
    if (!open) return;
    
    async function load() {
      setLoading(true);
      try {
        const loaders: Record<string, () => Promise<Component[]>> = {
          cpu: () => import("@/lib/data").then(m => m.getCPUs()),
          gpu: () => import("@/lib/data").then(m => m.getGPUs()),
          motherboard: () => import("@/lib/data").then(m => m.getMotherboards()),
          ram: () => import("@/lib/data").then(m => m.getRAM()),
          storage: () => import("@/lib/data").then(m => m.getStorage()),
          psu: () => import("@/lib/data").then(m => m.getPSUs()),
          case: () => import("@/lib/data").then(m => m.getCases()),
          cooler: () => import("@/lib/data").then(m => m.getCoolers()),
        };
        
        const data = await loaders[type]();
        setComponents(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [open, type]);

  const filtered = useMemo(() => {
    let result = components;
    if (searchQuery) {
      result = result.filter(c => 
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        c.manufacturer.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    if (manufacturerFilter !== "all") {
      result = result.filter(c => c.manufacturer === manufacturerFilter);
    }
    return result;
  }, [searchQuery, manufacturerFilter, components]);

  const manufacturers = components.length > 0 
    ? Array.from(new Set(components.map(c => c.manufacturer)))
    : [];

  return (
    <Modal 
      open={open} 
      onClose={onClose} 
      title={`Select ${type.toUpperCase()}`} 
      description={`Choose a ${type} for your build.`}
      size="xl"
    >
      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center justify-between">
          <ComponentSearch 
            value={searchQuery} 
            onChange={setSearchQuery} 
            placeholder={`Search ${type}...`} 
          />
          <ComponentFilter 
            label="Manufacturer" 
            value={manufacturerFilter} 
            onChange={setManufacturerFilter} 
            options={manufacturers} 
          />
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <Spinner size="lg" />
            <p className="mt-4 text-zinc-500">Loading components...</p>
          </div>
        ) : (
        <div className="max-h-[60vh] overflow-y-auto pr-2">
          <ComponentGrid 
            components={filtered} 
            type={type} 
            onSelect={(component) => {
              onSelect(component);
              onClose();
            }} 
          />
        </div>

        )}
      </div>
    </Modal>
  );
}
