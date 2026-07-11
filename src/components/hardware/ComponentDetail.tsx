"use client";

import { Component } from "@/lib/data/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface ComponentDetailProps {
  component: Component;
}

export function ComponentDetail({ component }: ComponentDetailProps) {
  return (
    <div className="max-w-5xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div className="space-y-6">
          <div className="aspect-square relative overflow-hidden rounded-2xl bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-800">
            <img
              src={component.image}
              alt={component.name}
              className="h-full w-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = "/images/placeholder.jpg";
              }}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Card className="p-4 text-center">
              <span className="text-xs text-zinc-500 dark:text-zinc-400 uppercase">Gaming Score</span>
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {('gamingScore' in component) ? component.gamingScore : 'N/A'}
              </div>
            </Card>
            <Card className="p-4 text-center">
              <span className="text-xs text-zinc-500 dark:text-zinc-400 uppercase">AI Score</span>
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                {('aiScore' in component) ? component.aiScore : 'N/A'}
              </div>
            </Card>
          </div>
        </div>

        <div className="flex flex-col">
          <div className="mb-6">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm font-medium text-blue-600 dark:text-blue-400 uppercase tracking-wider">
                {component.manufacturer}
              </span>
              <Badge>{component.type.toUpperCase()}</Badge>
            </div>
            <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100 mb-4">
              {component.name}
            </h1>
            <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">
              {component.description}
            </p>
          </div>

          <div className="mb-8">
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase mb-3">
              Key Specifications
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3">
              {/* This is simplified, in reality I'd map based on component type */}
              <SpecItem label="Release Date" value={component.releaseDate} />
              <SpecItem label="MSRP" value={`£${component.msrp}`} />
            </div>
          </div>

          <div className="mt-auto">
            <Button className="w-full h-12 text-base" size="lg">
              Add to Build
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

function SpecItem({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-zinc-100 dark:border-zinc-800">
      <span className="text-sm text-zinc-500 dark:text-zinc-400">{label}</span>
      <span className="text-sm font-medium text-zinc-900 dark:text-zinc-100">{value}</span>
    </div>
  );
}
