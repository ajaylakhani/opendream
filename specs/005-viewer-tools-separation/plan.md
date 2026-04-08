# Implementation Plan: Viewer Tools Separation

**Branch**: `005-viewer-tools-separation` | **Date**: 2026-04-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-viewer-tools-separation/spec.md`

## Summary

Move the optional dream viewer (`dream_events.py`, `viewer.html`) from
`scripts/` and `assets/` into a new `tools/viewer/` directory, separate from
the core skill. Remove the subprocess pip install of viewer dependencies
(aiohttp, watchdog) from `setup.py`. Create a standalone README in
`tools/viewer/` for manual setup. Update all documentation references.
This addresses two security findings: `subprocess-pip-install-in-setup` and
`aiohttp-websocket-server`.

## Technical Context

**Language/Version**: Python 3.x (scripts), Markdown (documentation)
**Primary Dependencies**: None for core skill. aiohttp + watchdog remain viewer-only deps (manually installed).
**Storage**: Flat files — file moves within the repository
**Testing**: `python3 scripts/validate.py` for core skill; manual viewer test
**Target Platform**: OpenClaw/Hermes agents
**Project Type**: Agent skill (refactoring + documentation update)
**Performance Goals**: N/A — no runtime changes
**Constraints**: Core skill must remain self-contained per Principle V. Viewer must still work from its new location.
**Scale/Scope**: 2 files moved, 1 file created, ~6 files modified (setup.py, SKILL.md, CONTRIBUTING.md, constitution, dream_events.py internal path, copilot-instructions.md)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Agent-Is-Dreamer | N/A | No changes to dreamer framing. |
| II. Sleep Architecture Fidelity | N/A | No changes to dream cycles or tick structure. |
| III. Heartbeat-Native Execution | N/A | No changes to heartbeat mechanism. |
| IV. Single Source of Truth | ✅ PASS | Viewer references will be updated to point to the new canonical location. No duplication. |
| V. Agent Skills Compliance | ✅ PASS | *Strengthened* — the viewer was never part of the skill spec but lived alongside skill files. Moving it to `tools/` makes the skill directory cleaner and more compliant with self-containment. |
| Token Budget (<5K/tick) | N/A | No dream-time changes. |
| Development Workflow | ⚠️ UPDATE | Constitution references `scripts/dream_events.py` — must be updated to `tools/viewer/dream_events.py` (FR-009). |

**Gate result: PASS** — all principles satisfied. The Development Workflow section needs a path update (not a violation, just a reference correction). Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/005-viewer-tools-separation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
scripts/
├── setup.py                     # MODIFIED: remove step 5 (viewer deps), 5→4 steps
├── validate.py                  # Unchanged (already doesn't check viewer)
└── dream_events.py              # REMOVED (moved to tools/viewer/)

assets/
├── HEARTBEAT-dream-section.md   # Unchanged
├── SOUL-fragment.md             # Unchanged
├── prompts.yaml                 # Unchanged
├── openclaw.json                # Unchanged
├── hero.png                     # Unchanged
└── viewer.html                  # REMOVED (moved to tools/viewer/)

tools/
└── viewer/
    ├── dream_events.py          # MOVED from scripts/ — internal path updated
    ├── viewer.html              # MOVED from assets/
    └── README.md                # NEW: standalone viewer setup instructions

SKILL.md                         # MODIFIED: viewer paths updated
CONTRIBUTING.md                  # MODIFIED: dream_events.py reference updated
README.md                        # Unchanged (no viewer references currently)
docs/
├── ARCHITECTURE.md              # Unchanged
└── TOKEN-ANALYSIS.md            # Unchanged
references/
├── REFERENCE.md                 # Unchanged
└── INSTALL.md                   # Unchanged

.specify/memory/constitution.md  # MODIFIED: viewer path in Development Workflow
.github/copilot-instructions.md  # MODIFIED: project structure updated
```

**Structure Decision**: New `tools/viewer/` directory at repo root. This follows
the common convention of `tools/` for developer-facing utilities that are not
part of the distributed artifact. The viewer files are co-located so
`dream_events.py` can find `viewer.html` alongside itself.

## Complexity Tracking

No constitution violations — section not required.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
