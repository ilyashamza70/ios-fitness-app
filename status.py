# HI
# TDP: 2026-03-10T11:00:00Z | Turin, Italy | appleEquipment
# status.py — smart project status viewer

import os
import sys
import subprocess
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ── ANSI Colors ──────────────────────────────────────────────────────────────
R  = "\033[0m"       # reset
B  = "\033[1m"       # bold
RED   = "\033[91m"
GRN   = "\033[92m"
YLW   = "\033[93m"
BLU   = "\033[94m"
MAG   = "\033[95m"
CYN   = "\033[96m"
GRY   = "\033[90m"

def c(color, text): return f"{color}{text}{R}"
def header(text):   print(f"\n{B}{BLU}{'─'*60}{R}\n{B}{BLU}  {text}{R}\n{B}{BLU}{'─'*60}{R}")
def ok(msg):        print(f"  {c(GRN,'✓')} {msg}")
def warn(msg):      print(f"  {c(YLW,'⚠')} {msg}")
def err(msg):       print(f"  {c(RED,'✗')} {msg}")
def info(msg):      print(f"  {c(GRY,'·')} {msg}")

REPO = Path(__file__).parent.resolve()

# ── 1. ASCII Banner ───────────────────────────────────────────────────────────
def banner():
    print(f"""
{B}{MAG}
  ╔══════════════════════════════════════════╗
  ║         appleEquipment                  ║
  ║  Apple ecosystem utils + WiFi QR tool   ║
  ╚══════════════════════════════════════════╝{R}
  {GRY}Owner: Hamza Ilyas (ilyashamza70) | Branch: V1{R}
  {GRY}Remote: github.com/ilyashamza70/ios-fitness-app{R}
""")

# ── 2. Git Status ─────────────────────────────────────────────────────────────
def git_status():
    header("GIT STATUS")
    def git(cmd):
        try:
            return subprocess.check_output(
                ["git"] + cmd, cwd=REPO,
                stderr=subprocess.DEVNULL, text=True
            ).strip()
        except Exception:
            return None

    branch = git(["rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"
    remote_url = git(["remote", "get-url", "origin"]) or "no remote"
    print(f"  {c(CYN,'Branch:')}  {branch}")
    print(f"  {c(CYN,'Remote:')}  {remote_url}")

    # Ahead/behind
    ab = git(["rev-list", "--left-right", "--count", "HEAD...@{u}"])
    if ab:
        ahead, behind = ab.split()
        if int(ahead) > 0:  warn(f"Ahead of remote by {ahead} commit(s)")
        if int(behind) > 0: warn(f"Behind remote by {behind} commit(s)")
        if ahead == "0" and behind == "0": ok("Up to date with remote")

    # Last 3 commits
    log = git(["log", "--oneline", "-3"])
    if log:
        print(f"\n  {c(CYN,'Last 3 commits:')}")
        for line in log.splitlines():
            info(line)

    # Dirty files
    dirty = git(["status", "--short"])
    if dirty:
        warn(f"Dirty working tree:")
        for line in dirty.splitlines():
            print(f"    {c(RED, line)}")
    else:
        ok("Working tree clean")

# ── 3. README Summary ─────────────────────────────────────────────────────────
def readme_summary():
    header("README SUMMARY")
    readme = REPO / "README.md"
    if not readme.exists():
        err("README.md not found")
        return
    lines = readme.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in lines[:20]:
        if line.strip():
            info(line)

# ── 4. File Structure ─────────────────────────────────────────────────────────
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache"}

def file_structure():
    header("FILE STRUCTURE (depth 2)")
    def walk(path, prefix="", depth=0):
        if depth > 2:
            return
        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        for i, entry in enumerate(entries):
            if entry.name in SKIP_DIRS:
                connector = "└── " if i == len(entries)-1 else "├── "
                print(f"  {prefix}{connector}{c(GRY, entry.name + '/')} {c(GRY,'[skipped]')}")
                continue
            connector = "└── " if i == len(entries)-1 else "├── "
            if entry.is_dir():
                print(f"  {prefix}{connector}{c(CYN, entry.name + '/')}")
                ext = "    " if i == len(entries)-1 else "│   "
                walk(entry, prefix + ext, depth + 1)
            else:
                size = entry.stat().st_size
                size_str = f"{c(GRY, f'({size:,} B)')}" if size > 0 else ""
                print(f"  {prefix}{connector}{entry.name} {size_str}")
    walk(REPO)

# ── 5. TODO List ──────────────────────────────────────────────────────────────
def todo_list():
    header("TODO / TASKS")
    found = False

    # ToDoList.txt
    todo_file = REPO / "ToDoList.txt"
    if todo_file.exists():
        print(f"  {c(YLW, 'From ToDoList.txt:')}")
        for line in todo_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip() and not line.startswith("#"):
                info(line.strip())
        found = True

    # Prioritylist.md
    prio = REPO / "Prioritylist.md"
    if prio.exists():
        print(f"\n  {c(YLW, 'From Prioritylist.md:')}")
        for line in prio.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.strip():
                marker = c(RED,"[ ]") if "\\" not in line.split("\\")[-1] else c(GRN,"[x]")
                # show lines with checkbox-like content
                info(line.strip()[:100])
        found = True

    # Inline # TODO in .py files
    py_todos = []
    for f in REPO.rglob("*.py"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if "# TODO" in line or "# todo" in line.lower():
                py_todos.append(f"{f.name}:{i}  {line.strip()}")
    if py_todos:
        print(f"\n  {c(YLW, 'Inline TODOs in .py files:')}")
        for t in py_todos:
            warn(t)
        found = True

    if not found:
        info("No TODO files found")

# ── 6. Tech Stack Detection ───────────────────────────────────────────────────
def tech_stack():
    header("TECH STACK")
    if (REPO / ".venv").exists():
        ok("Python virtual environment (.venv)")
    if (REPO / "requirements.txt").exists():
        ok("requirements.txt found")
        for line in (REPO / "requirements.txt").read_text().splitlines()[:10]:
            if line.strip() and not line.startswith("#"):
                info(f"  dep: {line.strip()}")
    if (REPO / "package.json").exists():
        ok("Node.js project (package.json)")
    for f in REPO.glob("*.csproj"):
        ok(f".NET project: {f.name}")
    # check for qrcode usage
    for f in REPO.glob("*.py"):
        if f.name == "status.py":
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "qrcode" in text:
            ok(f"qrcode library used in {f.name}")
        if "import" in text:
            imports = [l.strip() for l in text.splitlines() if l.strip().startswith("import") or l.strip().startswith("from")]
            for imp in imports[:5]:
                info(imp)
    if (REPO / "wifi.py").exists():
        ok("wifi.py — WiFi QR code generator")
    if (REPO / "wifi_qr.png").exists():
        warn("wifi_qr.png present (generated artifact — consider .gitignore)")

# ── 7. Quick Commands ─────────────────────────────────────────────────────────
def quick_commands():
    header("QUICK COMMANDS")
    cmds = [
        ("Activate venv (Windows)", r".venv\Scripts\activate"),
        ("Activate venv (Mac/Linux)", "source .venv/bin/activate"),
        ("Generate WiFi QR code", "python wifi.py"),
        ("Install qrcode dep", "pip install qrcode[pil]"),
        ("View QR image (Windows)", "start wifi_qr.png"),
        ("Git status", "git status"),
        ("Git log (5)", "git log --oneline -5"),
        ("Push to remote", "git push origin V1"),
    ]
    for label, cmd in cmds:
        print(f"  {c(GRN, label)}")
        print(f"    {c(GRY, cmd)}")

# ── 8. Health Check ───────────────────────────────────────────────────────────
def health_check():
    header("HEALTH CHECK")
    issues = 0

    # Dirty files
    try:
        dirty = subprocess.check_output(
            ["git", "status", "--short"], cwd=REPO,
            stderr=subprocess.DEVNULL, text=True
        ).strip()
        if dirty:
            n = len(dirty.splitlines())
            warn(f"{n} uncommitted file(s)"); issues += 1
        else:
            ok("No dirty files")
    except Exception:
        err("Could not run git"); issues += 1

    # README check
    if not (REPO / "README.md").exists():
        err("README.md missing"); issues += 1
    else:
        ok("README.md present")

    # .gitignore check
    if not (REPO / ".gitignore").exists():
        warn(".gitignore missing — wifi_qr.png and .env may be committed accidentally"); issues += 1
    else:
        ok(".gitignore present")

    # Large files (>1MB)
    for f in REPO.rglob("*"):
        if f.is_file() and f.stat().st_size > 1_048_576:
            if not any(skip in f.parts for skip in SKIP_DIRS):
                warn(f"Large file: {f.relative_to(REPO)} ({f.stat().st_size//1024}KB)"); issues += 1

    # Security: hardcoded credentials in wifi.py
    wifi_py = REPO / "wifi.py"
    if wifi_py.exists():
        content = wifi_py.read_text(encoding="utf-8", errors="ignore")
        if 'password' in content.lower() and '=' in content:
            err("SECURITY: wifi.py may contain hardcoded credentials — move to .env!"); issues += 1

    print(f"\n  {'Health: ' + c(GRN,'ALL GOOD') if issues == 0 else c(RED, f'{issues} issue(s) found')}")

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    banner()
    git_status()
    readme_summary()
    file_structure()
    todo_list()
    tech_stack()
    quick_commands()
    health_check()
    print()
