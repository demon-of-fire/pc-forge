"use client";

import { useBuildContext } from "@/context/BuildContext";
import { BuildTotals, PriceEntry } from "@/lib/data/types";

export function useBuild() {
  const { components, setComponent, removeComponent, clearBuild } = useBuildContext();

  const calculateTotals = (): BuildTotals => {
    const priceByRetailer: Record<string, number> = {};
    let totalPrice = 0;
    let totalPower = 0;

    Object.values(components).forEach((comp) => {
      if (!comp) return;

      // Power consumption (simplified)
      if ('tdp' in comp) totalPower += (comp as { tdp: number }).tdp;
      if ('powerConsumption' in comp) totalPower += (comp as { powerConsumption: number }).powerConsumption;

      // Price - we take the cheapest for the total
      const minPrice = Math.min(...comp.prices.map((p: PriceEntry) => p.price));
      totalPrice += minPrice;

      // Retailer breakdown
      comp.prices.forEach((p: PriceEntry) => {
        priceByRetailer[p.retailer] = (priceByRetailer[p.retailer] || 0) + p.price;
      });
    });

    return {
      price: totalPrice,
      powerConsumption: totalPower,
      priceByRetailer,
    };
  };

  return {
    components,
    setComponent,
    removeComponent,
    clearBuild,
    totals: calculateTotals(),
  };
}
