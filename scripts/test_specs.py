import sys
sys.path.insert(0, 'scripts')

from scrapers.pcpartsuk import extract_specs_from_name

test_names = {
    "cpus": [
        "Intel Core i9-14900K",
        "AMD Ryzen 9 7950X 16 Core 32 Thread",
        "Intel Core i5-14600K 14 Core 20 Thread up to 5.3GHz",
    ],
    "gpus": [
        "NVIDIA GeForce RTX 4090 24GB GDDR6X",
        "AMD Radeon RX 7900 XTX 20GB GDDR6",
    ],
    "ram": [
        "Corsair Vengeance RGB 32GB (2 x 16GB) DDR5-6000 CL36",
        "G.Skill Trident Z5 64GB (2 x 32GB) DDR5-7200 CL34",
    ],
    "storage": [
        "Samsung 990 PRO 2TB M.2 NVMe PCIe 4.0",
        "WD Black SN850X 1TB M.2 PCIe 4.0",
    ],
    "psus": [
        "Corsair RM850x 850W 80+ Gold Fully Modular",
        "Seasonic PRIME TX-1000 1000W 80+ Titanium",
    ],
    "coolers": [
        "Noctua NH-D15 chromax.black",
        "Corsair iCUE H150i ELITE CAPELLIX 360mm",
    ],
    "cases": [
        "Fractal Design North TG White",
        "Corsair 5000D Airflow Mid Tower",
    ],
}

for cat, names in test_names.items():
    for name in names:
        specs = extract_specs_from_name(cat, name)
        print(f"{cat}: {name}")
        print(f"  Specs: {specs}")