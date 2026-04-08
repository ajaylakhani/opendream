# Quickstart: Viewer Tools Separation

**Feature**: 005-viewer-tools-separation | **Date**: 2026-04-08

---

## Before → After

| Aspect | Before | After |
|--------|--------|-------|
| Viewer server | `scripts/dream_events.py` | `tools/viewer/dream_events.py` |
| Viewer HTML | `assets/viewer.html` | `tools/viewer/viewer.html` |
| Viewer README | None | `tools/viewer/README.md` |
| setup.py steps | 5 (includes viewer deps) | 4 (viewer deps removed) |
| Security: subprocess pip | Present in setup.py | Removed |
| Security: aiohttp server | In scripts/ alongside core | Isolated in tools/viewer/ |
| Viewer dep install | Automatic (setup.py step 5) | Manual (`pip install aiohttp watchdog`) |

## What Changes for Users

**Core skill users**: Nothing. `setup.py` runs faster (one fewer step) and no
longer requires aiohttp/watchdog. The skill installs and runs identically.

**Viewer users**: Instead of viewer dependencies being installed automatically,
users navigate to `tools/viewer/` and follow the README to install manually:
```bash
pip install aiohttp watchdog
python tools/viewer/dream_events.py
```

## What Changes for Developers

- Viewer-related contributions reference `tools/viewer/` instead of `scripts/` + `assets/`
- SKILL.md viewer section points to new paths
- Constitution Development Workflow section updated

## Files Changed Summary

| Action | File |
|--------|------|
| MOVE | `scripts/dream_events.py` → `tools/viewer/dream_events.py` |
| MOVE | `assets/viewer.html` → `tools/viewer/viewer.html` |
| CREATE | `tools/viewer/README.md` |
| MODIFY | `scripts/setup.py` (remove step 5) |
| MODIFY | `SKILL.md` (update viewer paths) |
| MODIFY | `CONTRIBUTING.md` (update viewer reference) |
| MODIFY | `.specify/memory/constitution.md` (update viewer path) |
| UPDATE | `.github/copilot-instructions.md` (via agent context script) |
