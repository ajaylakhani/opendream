# Implementation Plan: README & Contributing Guide

**Branch**: `004-readme-contributing` | **Date**: 2026-04-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-readme-contributing/spec.md`

## Summary

Create a visually striking README.md with hero image, badges, installation
instructions, architecture overview, and cost summary. Create CONTRIBUTING.md
with development workflow, code style, PR conventions, and speckit integration.
Both are pure documentation files — no code changes to the skill itself.

## Technical Context

**Language/Version**: Markdown (documentation files), PNG/SVG (hero image asset)
**Primary Dependencies**: None — pure documentation feature
**Storage**: Flat files — `README.md` and `CONTRIBUTING.md` at repo root, hero image in `assets/`
**Testing**: Visual inspection on GitHub; link validation via manual review
**Target Platform**: GitHub repository rendering (github.com Markdown renderer)
**Project Type**: Documentation (open-source project collateral)
**Performance Goals**: N/A
**Constraints**: Hero image must render on GitHub. Badges via shields.io (static badge URLs). All links must use relative paths within the repository.
**Scale/Scope**: 2 new files (README.md, CONTRIBUTING.md) + 1 image asset. No existing files modified.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Agent-Is-Dreamer | ✅ PASS | README description must maintain the dreamer framing — "the agent dreams, not the user." No risk of breaking this in documentation. |
| II. Sleep Architecture Fidelity | ✅ PASS | README summarises the 5-cycle architecture. Does not modify it. |
| III. Heartbeat-Native Execution | N/A | Documentation only — no changes to tick logic or gateway config. |
| IV. Single Source of Truth | ⚠️ NOTE | README will summarise information from SKILL.md, ARCHITECTURE.md, REFERENCE.md. Must link to authoritative sources rather than duplicating detail. Keep summaries high-level. |
| V. Agent Skills Compliance | ✅ PASS | No changes to SKILL.md structure or frontmatter. |
| Token Budget (<5K/tick) | N/A | No dream-time changes. |
| Nightly Total (~56K) | N/A | No dream-time changes. |

**Gate result: PASS** — all principles satisfied. Principle IV requires care during implementation to avoid duplicating SoT content. Proceed to Phase 0.

**Post-design re-check (Phase 1 complete)**: All gates re-confirmed. Design
adds README.md and CONTRIBUTING.md as new files — no existing files modified.
README sections link to authoritative sources (Principle IV: SoT) rather than
duplicating detail. LICENSE file aligns with SKILL.md frontmatter declaration.
No new external dependencies. No dream-time changes.

## Project Structure

### Documentation (this feature)

```text
specs/004-readme-contributing/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
README.md                    # NEW: Project entry point with hero image, badges, instructions
CONTRIBUTING.md              # NEW: Open-source contribution guidelines
assets/
├── hero.png                 # NEW: Hero image for README (placeholder — user supplies actual image)
├── HEARTBEAT-dream-section.md   # Unchanged
├── SOUL-fragment.md             # Unchanged
├── prompts.yaml                 # Unchanged
├── openclaw.json                # Unchanged
└── viewer.html                  # Unchanged
docs/
├── ARCHITECTURE.md              # Unchanged (linked from README)
└── TOKEN-ANALYSIS.md            # Unchanged (cost data sourced from here)
references/
├── REFERENCE.md                 # Unchanged (linked from README)
└── INSTALL.md                   # Unchanged (linked from README)
scripts/
├── setup.py                     # Unchanged (referenced in README instructions)
├── validate.py                  # Unchanged (referenced in README instructions)
└── dream_events.py              # Unchanged
SKILL.md                         # Unchanged (README references metadata)
```

**Structure Decision**: No new directories. Two new root-level Markdown files
and one image asset in the existing `assets/` directory. This follows GitHub
conventions (README.md and CONTRIBUTING.md at root) and the project's existing
pattern of storing assets in `assets/`.

## Complexity Tracking

No constitution violations — section not required.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
