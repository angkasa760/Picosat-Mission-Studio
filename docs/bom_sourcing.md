# Bill of Materials (BOM) & Sourcing Guide
## 437.2 MHz UHF Turnstile Antenna - Picosat Mission

This document lists all professional-grade components required to fabricate the simulated antenna design.

| Item | Specification | Qty | Purpose | Est. Price | Link |
|------|---------------|-----|---------|------------|------|
| **Beryllium Copper (BeCu) Tape** | Width: 2mm, Thickness: 0.1mm | 4 x 170mm | Antenna Arms (Tape Measure style) | $15.00 | [Mouser](https://www.mouser.com) |
| **SMA Female Connector** | PCB Mount, Through-Hole, 50 Ohm | 4 pcs | Feed Points (Port 1-4) | $8.00 | [DigiKey](https://www.digikey.com) |
| **Coaxial Cable (RG-178)** | 50 Ohm Teflon, Flexible | 1 meter | Inner chassis RF routing | $5.00 | [Adafruit](https://www.adafruit.com) |
| **Aluminium 6061 Block** | 5U Picosat (50x50x1.5mm) | 1 pc | Satellite Chassis (Ground) | $20.00 | [MetalDepot](https://www.metaldepot.com) |
| **Nylon / Delrin Spacers** | 3D Printed or Machined | 4 pcs | Feed Gap Isolation (0.5mm) | $2.00 | [3DHubs](https://www.3dhubs.com) |
| **Nichrome Burn Wire** | 30 AWG | 20cm | Thermal Deployment Mechanism | $5.00 | [Amazon](https://www.amazon.com) |
| **Fishing Line (Nylon)** | 10 lb Test, 0.3mm | 1 meter | Antenna Stowing (Burn release) | $1.00 | [Local Store] |

### 🛠️ Tooling Requirements
1. **NanoVNA-H4**: Essential for tuning the 437.2 MHz resonance.
2. **Metal Snips / Precision Scissors**: For trimming the BeCu tape (±0.5mm accuracy).
3. **Reflow/Soldering Station**: For attaching SMA connectors to the chassis/PCB.

### ⚠️ Fabrication Note
As calculated in our **Sensitivity Analysis**, the design is robust to ±25mm error, but for optimal S11 (-20.5 dB), precision trimming of the BeCu tape to exactly **163.5 mm** is recommended after mounting.

---
*Created by AntiGravity AI | I-Satellite Society*
