# How to Choose a PSU

The Power Supply Unit (PSU) is the component that converts AC power from your wall outlet into the DC power your PC components need. A good PSU is the foundation of a reliable system — a bad one can damage every other component. Choosing the right PSU involves calculating your power needs, understanding efficiency ratings, and picking the right form factor.

## Wattage: How Much Do You Need?

The most common question about PSUs is "how many watts do I need?" The answer depends on your specific components, but a systematic approach makes it straightforward.

### Power Consumption by Component

| Component | Idle Power | Typical Load | Peak Power |
|---|---|---|---|
| CPU (mid-range, e.g., Ryzen 5 7600X) | 10-20W | 65-88W | 105W |
| CPU (high-end, e.g., Ryzen 9 7950X) | 20-30W | 120-170W | 230W |
| GPU (mid-range, e.g., RTX 4060 Ti) | 10-15W | 160W | 200W |
| GPU (high-end, e.g., RTX 4080 SUPER) | 15-25W | 300W | 320W |
| GPU (enthusiast, e.g., RTX 4090) | 20-30W | 350W | 450W |
| Motherboard | 30-50W | 50-80W | 80W |
| RAM (2×16GB DDR5) | 5-10W | 10-15W | 15W |
| NVMe SSD | 2-5W | 5-8W | 8W |
| Case fans (3×) | 3-6W | 6-12W | 12W |
| AIO pump | 3-5W | 5-10W | 10W |

### Quick Wattage Guidelines

| System Type | Recommended PSU Wattage |
|---|---|
| Office/basic desktop (iGPU only) | 300-400W |
| Budget gaming (RTX 4060, mid-range CPU) | 550-650W |
| Mid-range gaming (RTX 4070 Ti, Ryzen 7) | 650-750W |
| High-end gaming (RTX 4080, Ryzen 9/i9) | 750-850W |
| Enthusiast (RTX 4090, high-end CPU) | 850-1000W |
| Extreme (dual GPU, multiple drives, custom loop) | 1000-1200W+ |

### The 80% Rule

A PSU operates most efficiently at 40-60% of its rated capacity. Running a 1000W PSU at 300W isn't dangerous, but it's less efficient than running a 650W PSU at 300W. More importantly, you want headroom for transient power spikes — modern GPUs can spike 2-3× their rated power for microseconds.

A good rule of thumb: calculate your expected sustained load and choose a PSU rated for at least 1.5× that amount. If your system draws 450W under full load, a 650-750W PSU is ideal.

## 80+ Efficiency Ratings

The 80+ certification program rates PSUs based on how efficiently they convert AC to DC power at different load levels. Higher efficiency means less wasted energy (which becomes heat) and lower electricity bills.

### Efficiency Tiers

| Rating | 20% Load | 50% Load | 100% Load | Typical Price Premium |
|---|---|---|---|---|
| 80+ (White) | 80% | 80% | 80% | Baseline |
| 80+ Bronze | 82% | 85% | 82% | +5-10% |
| 80+ Silver | 85% | 88% | 85% | +10-15% |
| 80+ Gold | 87% | 90% | 87% | +15-25% |
| 80+ Platinum | 90% | 92% | 89% | +25-40% |
| 80+ Titanium | 92% | 94% | 90% | +40-60% |

### What the Numbers Mean

At 50% load (the most common operating point for a properly sized PSU):

- **80+ Bronze**: 85% efficiency — 15% of power is wasted as heat
- **80+ Gold**: 90% efficiency — 10% of power is wasted as heat
- **80+ Platinum**: 92% efficiency — 8% of power is wasted as heat

For a system drawing 500W at 50% load:
- Bronze PSU draws ~588W from the wall
- Gold PSU draws ~556W from the wall
- Platinum PSU draws ~543W from the wall

The difference between Bronze and Gold saves about 30W of wasted electricity. Over years of use, this adds up — but the bigger benefit of Gold-rated PSUs is that they typically use better internal components (capacitors, MOSFETs, transformers) that last longer and provide cleaner power.

### Is 80+ Gold Worth It?

For most builds, 80+ Gold is the sweet spot. The price premium over Bronze is modest, the efficiency improvement is meaningful, and the component quality is typically better. 80+ Platinum and Titanium are luxury choices — the efficiency gains are real but the price increase is steep for diminishing returns.

For budget builds where every dollar counts, 80+ Bronze from a reputable manufacturer is perfectly fine. Avoid unrated or no-name PSUs regardless of price.

## Modular vs Non-Modular vs Semi-Modular

PSU cable management affects build difficulty, airflow, and aesthetics.

### Non-Modular

All cables are permanently attached to the PSU. You get every cable whether you need it or not.

**Pros:**
- Cheapest option
- No risk of losing cables

**Cons:**
- Unused cables must be tucked away somewhere in the case
- Cable management is more difficult
- Can obstruct airflow in small cases

### Semi-Modular

Essential cables (24-pin motherboard, 8-pin CPU) are permanently attached. Peripheral cables (SATA, PCIe, fan) are detachable.

**Pros:**
- Good balance of price and manageability
- Essential cables are always connected
- Only attach the peripheral cables you need

**Cons:**
- Still has some permanently attached cables

### Fully Modular

Every cable is detachable.

**Pros:**
- Cleanest cable management — only use the cables you need
- Easiest to build with, especially in small cases
- Can replace cables with custom sleeved cables

**Cons:**
- Most expensive
- Must keep track of cables when not in use

### Recommendation

For most builds, semi-modular or fully modular is worth the small price premium. Cable management significantly affects case airflow and makes maintenance easier. If you're building in a small form factor case, fully modular is almost essential.

## ATX vs SFX vs SFX-L: Form Factor

The PSU form factor must match your case. Using the wrong size won't physically fit.

| Form Factor | Dimensions | Typical Use |
|---|---|---|
| ATX | 150 × 86 × 140-180mm | Standard mid-tower and full-tower cases |
| SFX | 125 × 100 × 63.5mm | Small form factor (SFF) cases |
| SFX-L | 125 × 100 × 130mm | Larger SFF cases, allows bigger fans |
| TFX | 85 × 65 × 175mm | Slim/low-profile cases |
| Flex ATX | 81.5 × 40.5 × 150mm | Ultra-compact builds, servers |

### ATX

The standard form factor for most PC builds. ATX PSUs typically offer the best selection, the highest wattages, and the lowest prices. If you're building in a mid-tower or full-tower case, you almost certainly want an ATX PSU.

### SFX

Designed for small form factor builds. SFX PSUs are physically smaller but still deliver substantial power (up to 750-850W in premium models). They use smaller fans (typically 80-92mm) which can be louder at high loads compared to ATX PSU fans.

### SFX-L

A slightly larger variant of SFX that accommodates a 120mm fan. This allows quieter operation at higher wattages compared to standard SFX. Some SFF cases support SFX-L but not all — check your case specifications.

## Connectors: What Your Components Need

Modern PSUs provide several types of connectors. Ensure your PSU has enough of each type for your components.

| Connector | Used By | Typical Count Needed |
|---|---|---|
| 24-pin ATX | Motherboard | 1 |
| 8-pin (4+4) EPS/CPU | Motherboard CPU power | 1-2 |
| 8-pin (6+2) PCIe | GPU power | 1-4 (depending on GPU) |
| 12VHPWR (16-pin) | RTX 30/40/50 series | 1 (if using adapter or native cable) |
| SATA power | SSDs, HDDs, fan hubs | 2-6 |
| Molex (4-pin peripheral) | Legacy devices, some fan hubs | 0-2 |

### The 12VHPWR Situation

NVIDIA's 12VHPWR connector (introduced with RTX 30-series) has had documented issues with improper seating causing melting. To avoid this:
- Use the native 12VHPWR cable that comes with ATX 3.0 PSUs
- If using an adapter, ensure it's fully seated with a firm click
- Don't bend the cable excessively near the connector
- Consider a PSU with native 12VHPWR support for RTX 40/50 series cards

## Quality Indicators: How to Spot a Good PSU

Not all PSUs are created equal, and wattage alone doesn't tell the whole story.

### What to Look For

- **Reputable brands**: Corsair, Seasonic, EVGA, be quiet!, Super Flower, Thermaltake, MSI, ASUS
- **Warranty length**: 7-10 years indicates manufacturer confidence
- **Japanese capacitors**: Higher quality capacitors last longer and handle heat better
- **80+ certification**: A baseline indicator of quality and efficiency
- **ATX 3.0 compliance**: Ensures proper transient power handling for modern GPUs
- **Professional reviews**: Look for reviews from outlets that do electrical testing (not just unboxing)

### Red Flags

- No 80+ certification
- Warranty under 3 years
- Price significantly below competitors at the same wattage
- No over-current, over-voltage, or short-circuit protection listed
- Unknown or rebranded manufacturers

## Summary

Choose a PSU with at least 1.5× your system's expected power draw, aiming for 40-60% load during typical use. 80+ Gold offers the best balance of efficiency, quality, and price for most builds. Fully modular or semi-modular cable management makes building easier. Ensure the PSU form factor matches your case and that it has the connectors your components need. Never cheap out on the PSU — it's the one component that protects every other component from electrical damage.
