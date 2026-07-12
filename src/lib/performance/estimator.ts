import { PCBuild } from "@/lib/data/types";

export function estimatePerformance(build: PCBuild) {
  const { cpu, gpu } = build.components;

  if (!cpu || !gpu) {
    return null;
  }

  // Heuristic: Use a base gaming score and scale it by the GPU's performance
  // and the CPU's gaming score (as a bottleneck factor)
  const gpuScore = gpu.gamingScore ?? 0;
  const cpuGamingFactor = (cpu.gamingScore ?? 0) / 100;
  const overallGamingScore = gpuScore * cpuGamingFactor;

  return {
    gaming: {
      "1080p": Math.round(overallGamingScore * 1.5),
      "1440p": Math.round(overallGamingScore * 1.0),
      "4K": Math.round(overallGamingScore * 0.5),
    },
    productivity: {
      videoEditing: Math.round((cpu.productivityScore ?? 0) * 0.7 + (gpu.aiScore ?? 0) * 0.3),
      streaming: Math.round((cpu.productivityScore ?? 0) * 0.6 + (gpu.gamingScore ?? 0) * 0.4),
      rendering3d: Math.round((cpu.productivityScore ?? 0) * 0.4 + (gpu.aiScore ?? 0) * 0.6),
      aiWorkloads: Math.round((cpu.aiScore ?? 0) * 0.3 + (gpu.aiScore ?? 0) * 0.7),
    },
  };
}
