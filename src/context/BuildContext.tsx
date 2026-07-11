"use client";

import React, { createContext, useContext, useState, useCallback, ReactNode } from "react";
import { CPU, GPU, Motherboard, RAM, Storage, PSU, Case, Cooler, ComponentType, Component } from "@/lib/data/types";

interface BuildComponents {
  cpu: CPU | null;
  gpu: GPU | null;
  motherboard: Motherboard | null;
  ram: RAM | null;
  storage: Storage | null;
  psu: PSU | null;
  case: Case | null;
  cooler: Cooler | null;
}

interface BuildContextType {
  components: BuildComponents;
  setComponent: (type: ComponentType, component: Component | null) => void;
  removeComponent: (type: ComponentType) => void;
  clearBuild: () => void;
}

const BuildContext = createContext<BuildContextType | null>(null);

export function BuildProvider({ children }: { children: ReactNode }) {
  const [components, setComponents] = useState<BuildComponents>({
    cpu: null,
    gpu: null,
    motherboard: null,
    ram: null,
    storage: null,
    psu: null,
    case: null,
    cooler: null,
  });

  const setComponent = useCallback((type: ComponentType, component: Component | null) => {
    setComponents((prev) => ({
      ...prev,
      [type]: component,
    }));
  }, []);

  const removeComponent = useCallback((type: ComponentType) => {
    setComponents((prev) => ({
      ...prev,
      [type]: null,
    }));
  }, []);

  const clearBuild = useCallback(() => {
    setComponents({
      cpu: null,
      gpu: null,
      motherboard: null,
      ram: null,
      storage: null,
      psu: null,
      case: null,
      cooler: null,
    });
  }, []);

  return (
    <BuildContext.Provider value={{ components, setComponent, removeComponent, clearBuild }}>
      {children}
    </BuildContext.Provider>
  );
}

export function useBuildContext() {
  const context = useContext(BuildContext);
  if (!context) {
    throw new Error("useBuildContext must be used within a BuildProvider");
  }
  return context;
}
