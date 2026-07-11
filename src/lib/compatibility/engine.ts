import { 
  CompatibilityResult, PCBuild 
} from "@/lib/data/types";

export function checkCompatibility(build: PCBuild): CompatibilityResult[] {
  const results: CompatibilityResult[] = [];
  const { components } = build;

  // 1. CPU ↔ Motherboard (Socket)
  if (components.cpu && components.motherboard) {
    if (components.cpu.socket !== components.motherboard.socket) {
      results.push({
        check: "CPU Socket",
        status: "incompatible",
        message: "Socket Mismatch",
        details: `The ${components.cpu.name} uses ${components.cpu.socket}, but the ${components.motherboard.name} uses ${components.motherboard.socket}.`,
      });
    } else {
      results.push({
        check: "CPU Socket",
        status: "compatible",
        message: "Socket Compatible",
        details: `Both use ${components.cpu.socket}.`,
      });
    }
  }

  // 2. Motherboard ↔ RAM (DDR Generation)
  if (components.motherboard && components.ram) {
    if (components.motherboard.ddrGeneration !== components.ram.ddrGeneration) {
      results.push({
        check: "RAM Generation",
        status: "incompatible",
        message: "DDR Generation Mismatch",
        details: `The motherboard supports ${components.motherboard.ddrGeneration}, but you selected ${components.ram.ddrGeneration} RAM.`,
      });
    } else {
      results.push({
        check: "RAM Generation",
        status: "compatible",
        message: "DDR Compatible",
        details: `Both use ${components.motherboard.ddrGeneration}.`,
      });
    }
  }

  // 3. PSU Wattage
  if (components.psu) {
    let estimatedDraw = 0;
    if (components.cpu) estimatedDraw += components.cpu.tdp;
    if (components.gpu) estimatedDraw += components.gpu.powerConsumption;
    estimatedDraw += 100; // Base system draw (Fans, SSDs, etc)

    const psuWattage = components.psu.wattage;
    if (psuWattage < estimatedDraw) {
      results.push({
        check: "Power Supply",
        status: "incompatible",
        message: "Insufficient Power",
        details: `Estimated draw is ${estimatedDraw}W, but your PSU only provides ${psuWattage}W.`,
      });
    } else if (psuWattage < estimatedDraw * 1.2) {
      results.push({
        check: "Power Supply",
        status: "warning",
        message: "Tight Power Margin",
        details: `You have ${psuWattage}W. We recommend at least 20% headroom (${Math.ceil(estimatedDraw * 1.2)}W).`,
      });
    } else {
      results.push({
        check: "Power Supply",
        status: "compatible",
        message: "Power Sufficient",
        details: `PSU provides plenty of power for this build.`,
      });
    }
  }

  // 4. Case ↔ GPU (Clearance)
  if (components.case && components.gpu) {
    // In our seed data, GPU length isn't explicit, so we'll assume a default or use a proxy
    // For now, let's just check if it's a very small case and a very large GPU
    if (components.case.formFactor === "Mini-ITX" && components.gpu.vramAmount >= 24) {
      results.push({
        check: "GPU Clearance",
        status: "warning",
        message: "Check GPU Length",
        details: `High-end GPUs like the ${components.gpu.name} are often too long for Mini-ITX cases. Please verify dimensions.`,
      });
    } else {
      results.push({
        check: "GPU Clearance",
        status: "compatible",
        message: "Clearance Likely OK",
        details: `GPU should fit in this ${components.case.formFactor} case.`,
      });
    }
  }

  // 5. Case ↔ Cooler (Clearance)
  if (components.case && components.cooler) {
    if (components.cooler.height && components.case.cpuCoolerClearance < components.cooler.height) {
      results.push({
        check: "Cooler Height",
        status: "incompatible",
        message: "Cooler Too Tall",
        details: `The ${components.cooler.name} is ${components.cooler.height}mm tall, but the case only supports up to ${components.case.cpuCoolerClearance}mm.`,
      });
    } else {
      results.push({
        check: "Cooler Height",
        status: "compatible",
        message: "Height Compatible",
        details: `Cooler fits within case limits.`,
      });
    }
  }

  return results;
}
