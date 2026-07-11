"use client";

import { useState, useEffect } from "react";
import { Component } from "@/lib/data/types";
import { getCPUs, getGPUs, getMotherboards, getRAM, getStorage, getPSUs, getCases, getCoolers } from "@/lib/data";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Skeleton } from "@/components/ui/Skeleton";

const categoryMap: Record<string, { 
  label: string; 
  loader: () => Promise<Component[]> 
}> = {
  cpus: { label: "CPUs", loader: getCPUs },
  gpus: { label: "GPUs", loader: getGPUs },
  motherboards: { label: "Motherboards", loader: getMotherboards },
  ram: { label: "RAM", loader: getRAM },
  storage: { label: "Storage", loader: getStorage },
  psus: { label: "PSUs", loader: getPSUs },
  cases: { label: "Cases", loader: getCases },
  cooling: { label: "Cooling", loader: getCoolers },
};

export default function ComparePage() {
  const [category, setCategory] = useState<string>("cpus");
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [allComponents, setAllComponents] = useState<Component[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await categoryMap[category].loader();
        setAllComponents(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [category]);

  const toggleSelection = (id: string) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : 
      prev.length < 4 ? [...prev, id] : prev
    );
  };

  const selectedComponents = allComponents.filter(c => selectedIds.includes(c.id));
  const filteredComponents = allComponents.filter(c => 
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 text-center">
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100 sm:text-4xl">
          Compare Hardware
        </h1>
        <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400">
          Side-by-side comparison of specs and prices.
        </p>
      </div>

      <div className="mb-12 flex flex-col gap-6 items-center">
        <div className="flex flex-wrap justify-center gap-2">
          {Object.entries(categoryMap).map(([id, config]) => (
            <Button 
              key={id} 
              variant={category === id ? "primary" : "outline"} 
              onClick={() => {
                setCategory(id);
                setSelectedIds([]);
              }}
            >
              {config.label}
            </Button>
          ))}
        </div>

        <div className="w-full max-w-md">
          <Input 
            placeholder={`Search ${categoryMap[category].label}...`} 
            value={searchQuery} 
            onChange={(e) => setSearchQuery(e.target.value)} 
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-12">
        <div className="lg:col-span-1 space-y-4">
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase">
            Select Components ({selectedIds.length}/4)
          </h3>
          <div className="space-y-2 max-h-[60vh] overflow-y-auto pr-2">
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-12 w-full" />)
            ) : (
              filteredComponents.map(comp => (
                <div 
                  key={comp.id} 
                  className="flex items-center gap-3 p-3 rounded-lg border border-zinc-200 dark:border-zinc-800 cursor-pointer hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
                  onClick={() => toggleSelection(comp.id)}
                >
                  <input 
                    type="checkbox" 
                    checked={selectedIds.includes(comp.id)} 
                    readOnly 
                    className="h-4 w-4 rounded border-zinc-300"
                  />
                  <span className="text-sm font-medium truncate">{comp.name}</span>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="lg:col-span-3 overflow-x-auto">
          {selectedComponents.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-center text-zinc-500">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="mb-4 opacity-20">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <rect x="3" y="3" width="18" height="18" rx="2" />
              </svg>
              <p>Select up to 4 components to compare them.</p>
            </div>
          ) : (
            <div className="min-w-[800px]">
              <div className="grid grid-cols-none gap-0 border-t border-l border-zinc-200 dark:border-zinc-800">
                <div className="grid grid-cols-5 gap-0">
                  <div className="p-4 border-r border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 font-semibold text-sm text-zinc-500 uppercase">
                    Specification
                  </div>
                  {selectedComponents.map(comp => (
                    <div key={comp.id} className="p-4 border-r border-b border-zinc-200 dark:border-zinc-800 text-center font-bold text-zinc-900 dark:text-zinc-100">
                      {comp.name}
                    </div>
                  ))}
                </div>
                {/* Spec rows would go here - dynamically generated based on type */}
                <div className="grid grid-cols-5 gap-0">
                  <div className="p-4 border-r border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-sm text-zinc-500">
                    Price (Cheapest)
                  </div>
                  {selectedComponents.map(comp => (
                    <div key={comp.id} className="p-4 border-r border-b border-zinc-200 dark:border-zinc-800 text-center font-medium">
                      £{Math.min(...comp.prices.map(p => p.price)).toFixed(2)}
                    </div>
                  ))}
                </div>
                <div className="grid grid-cols-5 gap-0">
                  <div className="p-4 border-r border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-sm text-zinc-500">
                    Manufacturer
                  </div>
                  {selectedComponents.map(comp => (
                    <div key={comp.id} className="p-4 border-r border-b border-zinc-200 dark:border-zinc-800 text-center">
                      {comp.manufacturer}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
