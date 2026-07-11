export type Manufacturer =
  | "AMD"
  | "Intel"
  | "NVIDIA"
  | "MSI"
  | "ASUS"
  | "Gigabyte"
  | "ASRock"
  | "EVGA"
  | "Corsair"
  | "G.Skill"
  | "Kingston"
  | "Samsung"
  | "Western Digital"
  | "Seagate"
  | "Crucial"
  | "SK Hynix"
  | "Thermaltake"
  | "Seasonic"
  | "be quiet!"
  | "Cooler Master"
  | "NZXT"
  | "Lian Li"
  | "Fractal Design"
  | "Phanteks";

export type Socket =
  | "AM5"
  | "AM4"
  | "LGA1700"
  | "LGA1851"
  | "LGA1200";

export type DDRGeneration = "DDR4" | "DDR5";

export type FormFactor =
  | "ATX"
  | "Micro-ATX"
  | "Mini-ITX"
  | "E-ATX"
  | "XL-ATX";

export type PCIeVersion = "PCIe 4.0" | "PCIe 5.0" | "PCIe 3.0";

export type StorageInterface = "NVMe" | "SATA";

export type NandType = "TLC" | "QLC" | "MLC" | "SLC";

export type CoolerType = "Air" | "AIO Liquid" | "Custom Liquid";

export type EfficiencyRating =
  | "80+ Bronze"
  | "80+ Gold"
  | "80+ Platinum"
  | "80+ Titanium"
  | "80+ White"
  | "80+ Standard";

export type ModularType = "Full" | "Semi" | "Non-Modular";

export type CompatibilityStatus = "compatible" | "warning" | "incompatible";

export interface PriceEntry {
  retailer: string;
  price: number;
  currency: string;
  url: string;
  availability: "in-stock" | "out-of-stock" | "limited" | "unknown";
  lastChecked: string;
}

export interface ScoreRange {
  min: number;
  max: number;
}

export interface ComponentBase {
  id: string;
  slug: string;
  name: string;
  manufacturer: Manufacturer;
  image: string;
  officialUrl: string;
  releaseDate: string;
  msrp: number;
  description: string;
  prices: PriceEntry[];
}

export interface CPU extends ComponentBase {
  type: "cpu";
  generation: string;
  architecture: string;
  socket: Socket;
  cores: number;
  threads: number;
  baseFrequency: number;
  boostFrequency: number;
  cache: string;
  integratedGraphics: string | null;
  tdp: number;
  gamingScore: number;
  productivityScore: number;
  aiScore: number;
  advantages: string[];
  disadvantages: string[];
}

export interface GPU extends ComponentBase {
  type: "gpu";
  architecture: string;
  vramAmount: number;
  vramType: string;
  memoryBus: number;
  cudaCores: number;
  rtCores: number | null;
  tensorCores: number | null;
  baseClock: number;
  boostClock: number;
  powerConsumption: number;
  recommendedPsu: number;
  pcieVersion: PCIeVersion;
  resolutionTargets: {
    "1080p": number;
    "1440p": number;
    "4K": number;
  };
  gamingScore: number;
  rayTracingScore: number;
  aiScore: number;
  advantages: string[];
  disadvantages: string[];
}

export interface Motherboard extends ComponentBase {
  type: "motherboard";
  socket: Socket;
  chipset: string;
  ddrGeneration: DDRGeneration;
  ramSlots: number;
  maxRam: number;
  pcieSlots: { version: PCIeVersion; x: number }[];
  m2Slots: number;
  sataPorts: number;
  usbPorts: { usb2: number; usb3: number; usbC: number };
  formFactor: FormFactor;
  wifiVersion: string | null;
  bluetoothVersion: string | null;
}

export interface RAM extends ComponentBase {
  type: "ram";
  capacity: number;
  speed: number;
  ddrGeneration: DDRGeneration;
  casLatency: number;
  kitSize: number;
  modules: string;
  voltage: number;
  heatspreader: boolean;
  rgb: boolean;
}

export interface Storage extends ComponentBase {
  type: "storage";
  capacity: number;
  interface: StorageInterface;
  readSpeed: number;
  writeSpeed: number;
  nandType: NandType;
  formFactor: string;
  tbw: number | null;
}

export interface PSU extends ComponentBase {
  type: "psu";
  wattage: number;
  efficiencyRating: EfficiencyRating;
  modularType: ModularType;
  fanSize: number;
  length: number;
  cpuConnectors: number;
  gpuConnectors: number;
  sataConnectors: number;
  molexConnectors: number;
  atxVersion: string;
}

export interface Case extends ComponentBase {
  type: "case";
  formFactor: FormFactor;
  motherboardSupport: FormFactor[];
  gpuClearance: number;
  cpuCoolerClearance: number;
  fanSupport: { size: number; count: number }[];
  radiatorSupport: string[];
  driveBays: { "25 inch": number; "35 inch": number };
  dimensions: { width: number; height: number; depth: number };
  weight: number;
}

export interface Cooler extends ComponentBase {
  type: "cooler";
  coolerType: CoolerType;
  socketCompatibility: Socket[];
  height: number | null;
  fanSize: number | null;
  fanCount: number;
  radiatorSize: number | null;
  coolingCapacity: number;
  noiseLevel: number;
  tdpRating: number;
}

export type Component =
  | CPU
  | GPU
  | Motherboard
  | RAM
  | Storage
  | PSU
  | Case
  | Cooler;

export type ComponentType =
  | "cpu"
  | "gpu"
  | "motherboard"
  | "ram"
  | "storage"
  | "psu"
  | "case"
  | "cooler";

export interface PCBuild {
  id: string;
  name: string;
  createdAt: string;
  updatedAt: string;
  components: {
    cpu: CPU | null;
    gpu: GPU | null;
    motherboard: Motherboard | null;
    ram: RAM | null;
    storage: Storage | null;
    psu: PSU | null;
    case: Case | null;
    cooler: Cooler | null;
  };
}

export interface CompatibilityResult {
  check: string;
  status: CompatibilityStatus;
  message: string;
  details: string;
}

export interface PerformanceEstimate {
  gaming: {
    "1080p": number;
    "1440p": number;
    "4K": number;
  };
  productivity: {
    videoEditing: number;
    streaming: number;
    rendering3d: number;
    aiWorkloads: number;
  };
}

export interface BuildTotals {
  price: number;
  powerConsumption: number;
  priceByRetailer: Record<string, number>;
}

export interface DatabaseMetadata {
  version: string;
  lastUpdated: string;
  totalComponents: Record<ComponentType, number>;
  sources: string[];
}
