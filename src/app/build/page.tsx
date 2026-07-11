"use client";

import { useState, useEffect, Suspense } from "react";
import dynamic from "next/dynamic";
import { useSearchParams } from "next/navigation";
import { BuildProvider, useBuildContext } from "@/context/BuildContext";
import { useBuild } from "@/hooks/useBuild";
import { BuildSlot } from "@/components/builder/BuildSlot";
import { BuildSummary } from "@/components/builder/BuildSummary";
import { CompatibilityPanel } from "@/components/builder/CompatibilityPanel";
import { checkCompatibility } from "@/lib/compatibility/engine";
import { estimatePerformance } from "@/lib/performance/estimator";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Skeleton } from "@/components/ui/Skeleton";
import { ComponentType } from "@/lib/data/types";
import { decodeBuild, encodeBuild } from "@/lib/sharing/shareUrl";
import { exportBuildToJson, importBuildFromJson } from "@/lib/sharing/export";

const ComponentPicker = dynamic(
  () => import("@/components/builder/ComponentPicker").then((m) => m.ComponentPicker),
  {
    ssr: false,
    loading: () => (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div className="rounded-xl bg-white p-8 dark:bg-zinc-900">
          <Skeleton className="h-8 w-48 mb-4" variant="text" />
          <Skeleton className="h-64 w-96" />
        </div>
      </div>
    ),
  }
);

function BuilderContent() {
  const searchParams = useSearchParams();
  const { components, setComponent, removeComponent, clearBuild } = useBuildContext();
  const { totals } = useBuild();
  const [pickingType, setPickingType] = useState<string | null>(null);
  const [showShareModal, setShowShareModal] = useState(false);
  const [shareUrl, setShareUrl] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const data = searchParams.get("data");
    if (data) {
      const build = decodeBuild(data);
      if (build) {
        Object.entries(build.components).forEach(([type, comp]) => {
          setComponent(type as ComponentType, comp);
        });
      }
    }
  }, [searchParams, setComponent]);

  const handleShare = () => {
    const currentBuild = {
      id: crypto.randomUUID(),
      name: "My PCForge Build",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      components,
    };
    const encoded = encodeBuild(currentBuild);
    const url = `${window.location.origin}${window.location.pathname}?data=${encoded}`;
    setShareUrl(url);
    setShowShareModal(true);
    setCopied(false);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const input = document.querySelector<HTMLInputElement>('[data-share-url]');
      if (input) {
        input.select();
        document.execCommand("copy");
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    }
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      const json = evt.target?.result as string;
      const build = importBuildFromJson(json);
      if (build) {
        Object.entries(build.components).forEach(([type, comp]) => {
          setComponent(type as ComponentType, comp);
        });
      }
    };
    reader.readAsText(file);
  };

  const handleExport = () => {
    const currentBuild = {
      id: crypto.randomUUID(),
      name: "My PCForge Build",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      components,
    };
    const json = exportBuildToJson(currentBuild);
    const blob = new Blob([json], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "pcforge-build.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const compatibilityResults = checkCompatibility({
    id: "current-build",
    name: "Current Build",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    components,
  });

  const performance = estimatePerformance({
    id: "current-build",
    name: "Current Build",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    components,
  });

  const slots: { type: ComponentType; label: string }[] = [
    { type: "cpu", label: "Processor" },
    { type: "gpu", label: "Graphics Card" },
    { type: "motherboard", label: "Motherboard" },
    { type: "ram", label: "Memory" },
    { type: "storage", label: "Storage" },
    { type: "psu", label: "Power Supply" },
    { type: "case", label: "Case" },
    { type: "cooler", label: "Cooler" },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100">PC Builder</h1>
          <p className="text-zinc-500 dark:text-zinc-400">Select components to create your custom PC.</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <label className="cursor-pointer">
            <span className="hidden">Import Build</span>
            <input type="file" accept=".json" onChange={handleImport} className="hidden" />
            <Button variant="outline" size="sm">Import JSON</Button>
          </label>
          <Button variant="outline" size="sm" onClick={handleExport}>Export JSON</Button>
          <Button variant="secondary" size="sm" onClick={handleShare}>Share Build</Button>
          <Button variant="danger" size="sm" onClick={clearBuild}>Reset</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-12 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-4">
          {slots.map((slot) => (
            <BuildSlot
              key={slot.type}
              type={slot.type}
              component={components[slot.type]}
              onSelect={() => setPickingType(slot.type)}
              onRemove={() => removeComponent(slot.type)}
            />
          ))}
        </div>

        <div className="space-y-8">
          <BuildSummary totals={totals} />
          <CompatibilityPanel results={compatibilityResults} />
          {performance && (
            <div className="rounded-xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 uppercase mb-4">
                Estimated Performance
              </h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-zinc-500 dark:text-zinc-400">1440p Gaming</span>
                  <span className="text-lg font-bold text-blue-600 dark:text-blue-400">{performance.gaming["1440p"]} FPS</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-zinc-500 dark:text-zinc-400">Productivity</span>
                  <span className="text-lg font-bold text-zinc-900 dark:text-zinc-100">{performance.productivity.videoEditing} / 100</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {pickingType && (
        <ComponentPicker
          type={pickingType as ComponentType}
          open={!!pickingType}
          onClose={() => setPickingType(null)}
          onSelect={(comp) => {
            setComponent(pickingType as ComponentType, comp);
            setPickingType(null);
          }}
        />
      )}

      <Modal 
        open={showShareModal} 
        onClose={() => setShowShareModal(false)} 
        title="Share Your Build" 
        description="Copy the link below to share your current PC configuration with others."
      >
        <div className="space-y-4">
          <div className="flex gap-2">
            <Input 
              readOnly 
              value={shareUrl} 
              data-share-url
              className="flex-1 font-mono text-xs" 
            />
            <Button 
              variant="primary" 
              onClick={handleCopy}
            >
              {copied ? "Copied!" : "Copy"}
            </Button>
          </div>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 text-center">
            This URL encodes your build data. No server is needed to load it.
          </p>
        </div>
      </Modal>
    </div>
  );
}

function BuilderSkeleton() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="space-y-2">
          <Skeleton className="h-8 w-48" variant="text" />
          <Skeleton className="h-4 w-64" variant="text" />
        </div>
        <div className="flex gap-3">
          <Skeleton className="h-9 w-24 rounded-xl" />
          <Skeleton className="h-9 w-24 rounded-xl" />
          <Skeleton className="h-9 w-28 rounded-xl" />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-12 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="flex items-center gap-4 rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">
              <Skeleton className="h-10 w-10 flex-shrink-0 rounded-lg" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-4 w-32" variant="text" />
                <Skeleton className="h-3 w-48" variant="text" />
              </div>
              <Skeleton className="h-8 w-20 rounded-lg" />
            </div>
          ))}
        </div>
        <div className="space-y-6">
          <Skeleton className="h-64 w-full rounded-xl" />
          <Skeleton className="h-48 w-full rounded-xl" />
        </div>
      </div>
    </div>
  );
}

export default function BuildPage() {
  return (
    <BuildProvider>
      <Suspense fallback={<BuilderSkeleton />}>
        <BuilderContent />
      </Suspense>
    </BuildProvider>
  );
}
