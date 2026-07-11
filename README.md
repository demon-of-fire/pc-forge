# PCForge

Open-source PC building, comparison, hardware discovery, and recommendation platform.

## Features

- **PC Builder** — Select components, check compatibility, estimate performance
- **Hardware Database** — Browse CPUs, GPUs, motherboards, RAM, storage, PSUs, cases, and coolers
- **Comparison Tool** — Side-by-side comparison of up to 4 components
- **Learning Centre** — Beginner-friendly guides on PC hardware
- **Save & Share** — Save builds to IndexedDB, share via URL or JSON export
- **Dark Mode** — Automatic light/dark theme with manual override
- **Accessible** — WCAG 2.1 AA compliant, keyboard navigable, screen reader friendly
- **Offline Ready** — PWA with service worker caching
- **Zero Backend** — All data stays in your browser

## Tech Stack

- **Framework:** Next.js 16 (App Router) with static export
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **Storage:** Dexie.js (IndexedDB)
- **Deployment:** GitHub Pages

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/pcforge.git
cd pcforge
npm install
```

### Development
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

### Build
```bash
npm run build
```

### Lint
```bash
npm run lint
```

## Project Structure

```
pcforge/
├── src/
│   ├── app/                  # Next.js App Router pages
│   │   ├── build/            # PC Builder page
│   │   ├── components/       # Hardware browser & detail pages
│   │   ├── compare/          # Comparison tool
│   │   ├── learn/            # Learning centre
│   │   ├── saved/            # Saved builds
│   │   └── settings/         # Settings & theme
│   ├── components/
│   │   ├── ui/               # Reusable UI (Modal, Tabs, Slider, etc.)
│   │   ├── layout/           # Navigation, Footer
│   │   ├── builder/          # BuildSlot, ComponentPicker, CompatibilityPanel
│   │   ├── hardware/         # ComponentCard, ComponentFilter, RangeFilter
│   │   ├── compare/          # Comparison table components
│   │   ├── performance/      # Performance estimation charts
│   │   ├── accessibility/    # Skip links, screen reader utilities
│   │   └── error/            # Error boundary components
│   ├── context/              # React Context providers
│   ├── hooks/                # Custom React hooks
│   └── lib/
│       ├── data/             # Hardware data & types
│       ├── compatibility/    # Compatibility checking engine
│       ├── performance/      # Performance estimation heuristics
│       ├── db/               # Dexie.js IndexedDB layer
│       ├── sharing/          # URL & JSON export
│       ├── themes/           # Dark mode management
│       ├── pricing/          # Price aggregation
│       ├── search/           # Search & filtering
│       └── utils/            # Utility functions
├── scripts/                  # Python data pipeline
├── data/                     # Hardware JSON data
├── content/                  # Learning centre content
└── public/                   # Static assets
```

## Data Pipeline

PCForge includes a Python-based data pipeline for populating and updating hardware data:

### Setup
```bash
cd scripts
pip install -r requirements.txt
```

### Initial Population
```bash
python scripts/initial_populate.py
python scripts/initial_populate.py --category cpus
python scripts/initial_populate.py --dry-run
```

### Daily Updates
```bash
python scripts/daily_update.py
```

### Validation
```bash
python scripts/initial_populate.py --dry-run --verbose
```

## GitHub Actions

- **Initial Population** (`initial-populate.yml`): Manual trigger to populate all hardware data
- **Daily Update** (`daily-update.yml`): Runs daily at 2 AM UTC, creates PR with changes

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Architecture

### Static Export
PCForge uses `output: "export"` in `next.config.ts` to generate a fully static site. All dynamic routes use `generateStaticParams()` to pre-render every possible path at build time.

### Client-Side State
- **Build State:** React Context (`BuildContext`) manages the current PC build
- **Persistence:** Dexie.js stores saved builds in IndexedDB
- **Theme:** `useSyncExternalStore` reads/writes localStorage

### Compatibility Engine
Real-time compatibility checks:
- CPU ↔ Motherboard socket matching
- RAM DDR generation ↔ Motherboard support
- PSU wattage ≥ Component power draw
- GPU length ≤ Case clearance
- Cooler height ≤ Case clearance

### Performance Estimation
Heuristic-based estimates for:
- Gaming FPS at 1080p, 1440p, 4K
- Productivity scores (video editing, 3D rendering)

## License

MIT

## Acknowledgements

Built as an open-source alternative to PCPartPicker.
