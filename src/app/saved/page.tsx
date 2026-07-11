"use client";

import { useState } from "react";
import { useSavedBuilds } from "@/hooks/useSavedBuilds";
import { useBuildContext } from "@/context/BuildContext";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";
import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import Link from "next/link";
import { ComponentType, Component } from "@/lib/data/types";
import { BuildProvider } from "@/context/BuildContext";

function SavedBuildsContent() {
  const { savedBuilds, updateBuild, deleteBuild } = useSavedBuilds();
  const { setComponent } = useBuildContext();
  const [editingBuildId, setEditingBuildId] = useState<string | null>(null);
  const [editName, setEditName] = useState("");

  const handleLoad = async (build: { components: Record<string, unknown> }) => {
    Object.entries(build.components).forEach(([type, comp]) => {
      setComponent(type as ComponentType, comp as Component);
    });
  };

  const startEdit = (build: { id: string; name: string }) => {
    setEditingBuildId(build.id);
    setEditName(build.name);
  };

  if (!savedBuilds) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-48 w-full" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-12 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100">Saved Builds</h1>
          <p className="mt-2 text-zinc-500 dark:text-zinc-400">Your locally saved PC configurations.</p>
        </div>
        <Link
          href="/build/"
          className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
        >
          Create New Build
        </Link>
      </div>

      {savedBuilds.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <div className="h-16 w-16 rounded-full bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center text-zinc-400 mb-4">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">No saved builds</h3>
          <p className="text-zinc-500 dark:text-zinc-400 max-w-xs mx-auto">
            Your saved builds will appear here. Start by creating a build in the builder.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {savedBuilds.map((build) => (
            <Card key={build.id} className="p-6 flex flex-col h-full">
              <div className="flex items-start justify-between mb-4">
                <h3 className="font-bold text-zinc-900 dark:text-zinc-100 truncate">{build.name}</h3>
                <Badge variant="default">
                  {Object.values(build.components).filter(Boolean).length}/8 Parts
                </Badge>
              </div>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mb-6">
                Saved on {new Date(build.createdAt).toLocaleDateString()}
              </p>
              <div className="mt-auto flex gap-2">
                <Button 
                  variant="primary" 
                  size="sm" 
                  className="flex-1" 
                  onClick={() => handleLoad(build)}
                >
                  Load
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => startEdit(build)}
                >
                  Rename
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  className="text-red-500 hover:text-red-600" 
                  onClick={() => deleteBuild(build.id)}
                >
                  Delete
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {editingBuildId && (
        <Modal 
          open={!!editingBuildId} 
          onClose={() => setEditingBuildId(null)} 
          title="Rename Build"
        >
          <div className="space-y-4">
            <Input 
              label="Build Name" 
              value={editName} 
              onChange={(e) => setEditName(e.target.value)} 
            />
            <div className="flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setEditingBuildId(null)}>
                Cancel
              </Button>
              <Button 
                variant="primary" 
                onClick={async () => {
                  if (editingBuildId) {
                    await updateBuild(editingBuildId, editName);
                  }
                  setEditingBuildId(null);
                }}
              >
                Save
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

export default function SavedBuildsPage() {
  return (
    <BuildProvider>
      <SavedBuildsContent />
    </BuildProvider>
  );
}

