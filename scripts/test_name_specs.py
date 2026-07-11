import sys
sys.path.insert(0, 'scripts')

from scrapers.pcpartsuk import extract_specs_from_name

# Test with actual product names from pcparts.uk
test_names = [
    "Intel Core i9-14900K",
    "AMD Ryzen 9 7950X 16 Core 32 Thread",
    "Intel Core i5-14600K 14 Core 20 Thread up to 5.3GHz",
    "NVIDIA GeForce RTX 4090 24GB GDDR6X",
    "AMD Radeon RX 7900 XTX 20GB GDDR6",
    "Corsair Vengeance RGB 32GB (2 x 16GB) DDR5-6000 CL36",
    "Samsung 990 PRO 2TB M.2 NVMe PCIe 4.0",
    "Corsair RM850x 850W 80+ Gold Full Modular",
    "Noctua NH-D15 chromax.black",
    "Fractal Design North TG White",
]

for name in test_names:
    # Determine category from name
    cat = "cpus"
    if "RTX" in name or "GTX" in name or "RX " in name or "Radeon" in name or "GeForce" in name:
        cat = "gpus"
    elif "DDR" in name or "Memory" in name or "RAM" in name:
        cat = "ram"
    elif "SSD" in name or "NVMe" in name or "M.2" in name:
        cat = "storage"
    elif "W " in name and ("PSU" in name or "Power" in name or "80+" in name):
        cat = "psus"
    elif "NH-" in name or "Cooler" in name or "AIO" in name or "Liquid" in name:
        cat = "coolers"
    elif "Case" in name or "Tower" in name:
        cat = "cases"
    
    specs = extract_specs_from_name(cat, name)
    print(f'{cat}: {name}')
    print(f'  Specs: {specs}')