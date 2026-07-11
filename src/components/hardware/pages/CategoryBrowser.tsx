"use client";

import { useState, useMemo } from "react";
import { Component, ComponentType } from "@/lib/data/types";

import { ComponentGrid } from "../ComponentGrid";
import { ComponentSearch } from "../ComponentSearch";
import { ComponentFilter } from "../ComponentFilter";
import { RangeFilter } from "../RangeFilter";
import { Badge } from "@/components/ui/Badge";

export function CategoryBrowser({ category, initialComponents, label }: { category: string; initialComponents: Component[]; label: string }) {
  const [components] = useState(initialComponents);
  const [searchQuery, setSearchQuery] = useState("");
  const [manufacturerFilter, setManufacturerFilter] = useState("all");
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 10000]);
  const [scoreRange, setScoreRange] = useState<[number, number]>([0, 100]);

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
    
    result = result.filter(c => {
      const minPrice = Math.min(...c.prices.map(p => p.price));
      return minPrice >= priceRange[0] && minPrice <= priceRange[1];
    });

    if ('gamingScore' in components[0]) {
      result = result.filter(c => {
        const score = (c as { gamingScore?: number }).gamingScore ?? 0;
        return score >= scoreRange[0] && score <= scoreRange[1];
      });
    }

    return result;
  }, [searchQuery, manufacturerFilter, priceRange, scoreRange, components]);

  const manufacturers = components.length > 0 
    ? Array.from(new Set(components.map(c => c.manufacturer)))
    : [];

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-8 flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="info">{label}</Badge>
          </div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100">
            {label}
          </h1>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:flex lg:items-center lg:gap-4">
          <ComponentSearch 
            value={searchQuery} 
            onChange={setSearchQuery} 
            placeholder={`Search ${label}...`} 
          />
          <ComponentFilter 
            label="Manufacturer" 
            value={manufacturerFilter} 
            onChange={setManufacturerFilter} 
            options={manufacturers} 
          />
          <RangeFilter 
            label="Price" 
            value={priceRange} 
            onChange={setPriceRange} 
            min={0} 
            max={10000} 
            unit="£" 
          />
          {('gamingScore' in components[0]) && (
            <RangeFilter 
              label="Score" 
              value={scoreRange} 
              onChange={setScoreRange} 
              min={0} 
              max={100} 
            />
          )}
        </div>
      </div>

      <ComponentGrid components={filtered} type={category as ComponentType} />
    </div>
  );
}
