import motherboardsData from "../../../public/data/motherboards.json";
import { Motherboard } from "./types";

function normalizeMotherboard(item: Record<string, unknown>): Motherboard {
  return {
    id: (item.id as string) || "",
    slug: (item.slug as string) || "",
    name: (item.name as string) || "Unknown",
    manufacturer: (item.manufacturer as string) || "Unknown",
    image: (item.image as string) || "",
    officialUrl: (item.officialUrl as string) || "",
    releaseDate: (item.releaseDate as string) || "2023-01-01",
    msrp: (item.msrp as number) || 0,
    description: (item.description as string) || "",
    prices: (item.prices as Motherboard["prices"]) || [],
    socket: (item.socket as Motherboard["socket"]) || "AM5",
    chipset: (item.chipset as string) || "",
    ddrGeneration: (item.ddrGeneration as Motherboard["ddrGeneration"]) || "DDR5",
    ramSlots: (item.ramSlots as number) || 4,
    maxRam: (item.maxRam as number) || 128,
    pcieSlots: (item.pcieSlots as Motherboard["pcieSlots"]) || [],
    m2Slots: (item.m2Slots as number) || 2,
    sataPorts: (item.sataPorts as number) || 4,
    usbPorts: (item.usbPorts as Motherboard["usbPorts"]) || { usb2: 0, usb3: 0, usbC: 0 },
    formFactor: (item.formFactor as Motherboard["formFactor"]) || "ATX",
    wifiVersion: (item.wifiVersion as string) || null,
    bluetoothVersion: (item.bluetoothVersion as string) || null,
    type: "motherboard",
    specs: (item.specs as Record<string, string>) || {},
  };
}

export async function getMotherboards(): Promise<Motherboard[]> {
  return (motherboardsData as Record<string, unknown>[]).map(normalizeMotherboard);
}

export async function getMotherboardBySlug(slug: string): Promise<Motherboard | null> {
  const found = (motherboardsData as Record<string, unknown>[]).find((m) => m.slug === slug);
  return found ? normalizeMotherboard(found) : null;
}
