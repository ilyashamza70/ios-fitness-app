<!-- HI | TDP: 2026-03-10T11:00:00Z | Turin, Italy | appleEquipment -->
---
name: appleEquipment
description: Personal Apple device management repo + WiFi QR code generator — utility toolkit for HI's Apple ecosystem (iPhone/Watch/Mac)
---

# appleEquipment Agent

## Project Overview

This repo started as an **iOS Fitness App** concept for calisthenics on Apple Watch/iPhone (HealthKit integration) and has evolved into a **personal Apple ecosystem utility hub**. The active deliverable is `wifi.py` — a Python QR code generator for WiFi network onboarding. The iOS app remains a planned future project requiring macOS Ventura + Xcode setup.

**Owner:** Hamza Ilyas (ilyashamza70)  
**GitHub Remote:** https://github.com/ilyashamza70/ios-fitness-app.git  
**Branch:** V1  
**Account:** ilyashamza70 (personal, not FKUnited)  
**Relationship to ecosystem:** Personal tools — not part of FKUnited Inc. or PoliTo coursework.

---

## Architecture

```
appleEquipment/
├── .venv/              # Python virtual environment (qrcode, pillow deps)
├── wifi.py             # WiFi QR code generator → outputs wifi_qr.png
├── wifi_qr.png         # Generated QR code image (gitignore candidate)
├── Prioritylist.md     # Development priority tracking
├── ToDoList.txt        # Confluence-style TODO documentation
├── README.md           # iOS fitness app overview (original project scope)
└── status.py           # Smart project status viewer
```

### wifi.py — Current Active Tool
- Generates a WPA-authenticated WiFi QR code image (`wifi_qr.png`)
- Uses `qrcode` library (requires `.venv` activation)
- **⚠️ SECURITY WARNING:** WiFi SSID and password are hardcoded in plaintext. Before any commit or sharing, move credentials to a `.env` file or environment variables. **Never push real WiFi credentials to a public repo.**
- Output format: PNG, black on white, box_size=10, border=4

### iOS Fitness App — Planned (Not Started)
- Target platform: iPhone + Apple Watch
- Language: Swift
- Framework: HealthKit (calories, exercise type, timer sync)
- Exercises: rope, push-ups, chin-ups, muscle-ups, leg raises
- Requires: macOS Ventura on VirtualBox + Xcode

---

## Tech Stack

| Component | Tech |
|-----------|------|
| Current active | Python 3.x, qrcode, Pillow |
| Virtual env | `.venv` (pip-managed) |
| Planned (iOS app) | Swift, Xcode, HealthKit |
| Platform target | iPhone, Apple Watch |
| OS requirement (dev) | macOS Ventura (VirtualBox) |

---

## Development Conventions

- Branch: always work on `V1`; tag releases as `v0.x`
- Python scripts: activate `.venv` before running anything
- Generated files (`*.png`, `*.qr`) should be in `.gitignore`
- Credentials: NEVER hardcode; use `.env` + `python-dotenv`
- iOS work requires macOS environment — document VirtualBox config in README when set up
- README was originally scoped for the iOS app; update it when adding new utilities

---

## Known TODOs

### Priority (from Prioritylist.md)

**Setup (mostly done):**
- ✅ Configure macOS Ventura on VirtualBox
- ⬜ Install Xcode on macOS Ventura
- ✅ Git and GitHub version control
- ✅ Create project documentation

**Documentation (in progress):**
- 🔄 Requirements document (started)
- ⬜ High-level design and architecture
- ⬜ Functional/non-functional requirements
- ⬜ Use case diagrams
- ⬜ Backlog and user stories setup

**Learn Swift and iOS:**
- ⬜ Follow Swift tutorials
- ⬜ Study iOS development basics
- ⬜ Explore HealthKit framework

**Core iOS Features (not started):**
- ⬜ Implement UI for exercise selection
- ⬜ Create input fields (calories, timer, exercise type)
- ⬜ Integrate with Apple HealthKit

**Testing:**
- ⬜ Use Xcode simulator for initial testing
- ⬜ Deploy to device for comprehensive testing

**wifi.py immediate:**
- 🔴 Move WiFi credentials out of source code → `.env`
- ⬜ Add `.gitignore` for `wifi_qr.png` and `.env`
- ⬜ Add CLI args support (pass SSID/password at runtime)

---

## Quick Commands

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Run WiFi QR generator
python wifi.py

# Install dependencies (if .venv is fresh)
pip install qrcode[pil]

# View generated QR code (Windows)
start wifi_qr.png

# Check git status
git status
git log --oneline -5
```

---

## Security Checklist

- [ ] Move WiFi credentials from `wifi.py` to `.env`
- [ ] Add `.env` to `.gitignore`
- [ ] Add `wifi_qr.png` to `.gitignore` (contains network info)
- [ ] Verify no secrets in git history: `git log -p | grep -i password`

---

## Related Projects in HI's Ecosystem

| Repo | Relationship |
|------|-------------|
| `polito/` | MSc Embedded Systems (academic) |
| `FKUnited.it/` | Company portal (business) |
| `homeNetwork/` | Network infrastructure (related to wifi.py use case) |
| `python-scripts/` | Other Python utilities |

---

## Agent Behavior Notes

- This is a **personal utility repo**, not a company or academic project
- Treat `wifi.py` as a quick personal tool — keep it simple
- iOS app is aspirational; do not over-engineer planning before Xcode is set up
- When editing `wifi.py`, always suggest moving credentials to env vars
- Do not commit `wifi_qr.png` — regenerate on demand
