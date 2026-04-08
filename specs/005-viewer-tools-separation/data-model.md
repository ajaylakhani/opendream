# Data Model: Viewer Tools Separation

**Feature**: 005-viewer-tools-separation | **Date**: 2026-04-08

---

## Entities

### 1. `tools/viewer/` Directory (NEW)

| Attribute | Value |
|-----------|-------|
| Type | Directory |
| Location | `tools/viewer/` (repo root) |
| Purpose | Self-contained optional viewer tooling, decoupled from core skill |
| Contents | `dream_events.py`, `viewer.html`, `README.md` |

### 2. `tools/viewer/dream_events.py` (MOVED)

| Field | Before | After |
|-------|--------|-------|
| Path | `scripts/dream_events.py` | `tools/viewer/dream_events.py` |
| VIEWER_HTML | `SKILL_DIR / "assets" / "viewer.html"` | `Path(__file__).resolve().parent / "viewer.html"` |
| Imports | Unchanged | Unchanged |
| Behaviour | WebSocket server on localhost:9736 | Identical |

### 3. `tools/viewer/viewer.html` (MOVED)

| Field | Before | After |
|-------|--------|-------|
| Path | `assets/viewer.html` | `tools/viewer/viewer.html` |
| Content | Unchanged | Unchanged |

### 4. `tools/viewer/README.md` (NEW)

| Field | Value |
|-------|-------|
| Path | `tools/viewer/README.md` |
| Sections | Purpose, Prerequisites, Install, Usage, How It Works, Back-link |
| Purpose | Replace the automated pip install step with manual instructions |

### 5. `scripts/setup.py` (MODIFIED)

| Field | Before | After |
|-------|--------|-------|
| Step count | 5 | 4 |
| Step 5 | Viewer dependencies (`install_viewer_deps()`) | Removed |
| `VIEWER_DEPS` constant | `["aiohttp", "watchdog"]` | Removed |
| `install_viewer_deps()` | Present (subprocess pip install) | Removed |
| Steps 1–4 | Unchanged | Unchanged |

---

## Relationships

```text
tools/viewer/
├── dream_events.py ──references──▶ viewer.html (co-located, __file__-relative)
├── viewer.html     ──displays────▶ dream events via WebSocket
└── README.md       ──documents───▶ dream_events.py + viewer.html setup

scripts/setup.py ──no longer references──▶ viewer deps

SKILL.md ──points to──▶ tools/viewer/dream_events.py (updated path)
CONTRIBUTING.md ──points to──▶ tools/viewer/dream_events.py (updated path)
constitution.md ──points to──▶ tools/viewer/dream_events.py (updated path)
```

---

## State Transitions

Not applicable — this feature is a file reorganisation with no runtime state changes.

---

## Validation Rules

| Rule | Source |
|------|--------|
| `tools/viewer/dream_events.py` must exist and be importable | FR-001, SC-001 |
| `tools/viewer/viewer.html` must exist | FR-002, SC-001 |
| `tools/viewer/README.md` must exist | FR-004 |
| `scripts/dream_events.py` must NOT exist after migration | FR-001 |
| `assets/viewer.html` must NOT exist after migration | FR-002 |
| `setup.py` must have exactly 4 steps | FR-003 |
| `setup.py` must not contain `subprocess` pip install | FR-003, SC-002 |
| No broken path references in SKILL.md, CONTRIBUTING.md, constitution.md | FR-005–009 |
