# Implementation Plan: Token Analysis Document

**Branch**: `002-token-analysis` | **Date**: 2026-04-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-token-analysis/spec.md`

## Summary

Create a standalone document at `docs/TOKEN-ANALYSIS.md` that provides a rigorous,
measured token-cost breakdown for OpenDream's nightly operation. The document covers
per-component input budgets, per-tick and per-night totals, cost by model tier, and
constitutional compliance verification across memory density scenarios. All estimates
use measured file sizes (~4 chars/token approximation), replacing the scattered rough
figures currently in ARCHITECTURE.md. The nightly total has been corrected from the
original ~12K estimate to ~44K based on measured data (per clarification 2026-04-07).

## Technical Context

**Language/Version**: Markdown (documentation-only feature — no code changes)
**Primary Dependencies**: None (pure documentation)
**Storage**: N/A
**Testing**: Manual review; cross-check against measured file sizes
**Target Platform**: Any Markdown reader (GitHub, VS Code, etc.)
**Project Type**: Documentation artifact within an agent skill
**Performance Goals**: N/A
**Constraints**: Token estimates must use measured file sizes, not rough guesses. ~4 chars/token approximation for English Markdown/YAML.
**Scale/Scope**: Single document (~200-300 lines), read by skill maintainers and operators

### Measured File Sizes (empirical data)

| File | Bytes | Est. Tokens (~4 chars/token) |
|------|------:|-----------------------------:|
| `HEARTBEAT-dream-section.md` | 1,796 | ~449 |
| `prompts.yaml` | 8,059 | ~2,015 |
| `SOUL-fragment.md` | 401 | ~100 |
| `SKILL.md` | 8,677 | ~2,169 |
| `openclaw.json` | 465 | ~116 |
| `memory-sparse.md` (fixture) | 89 | ~22 |
| `memory-medium.md` (fixture) | 406 | ~102 |
| `memory-dense.md` (fixture) | 1,211 | ~303 |

### Gateway Configuration

- `lightContext: true` — only HEARTBEAT.md bootstrapped
- `isolatedSession: true` — no conversation history
- `every: "30m"` — 14 dream ticks + 1 morning recall = 15 ticks/night
- `activeHours: 23:00–06:00 Europe/London`

### Existing Estimates (from ARCHITECTURE.md — to be corrected)

- HEARTBEAT bootstrap: ~400 tokens (rough) → measured ~449
- prompts.yaml read: ~800 tokens (rough) → measured ~2,015
- Memory file: ~500-2500 tokens (rough) → measured 0–303+
- Per-tick total: ~2-5K tokens (rough) → measured ~2,800–3,300
- Per-night total: ~12K tokens (rough) → measured ~44K input tokens
- Cost: Ollama £0, Haiku ~£0.01, Sonnet ~£0.15 → confirmed accurate

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Gate | Principle | Status |
|---|------|-----------|--------|
| 1 | Agent-Is-Dreamer framing preserved? | I | **PASS** — document describes the agent's token costs, no user framing |
| 2 | Sleep architecture (5 cycles) intact? | II | **PASS** — analysis covers 5 cycles × 14 ticks + 1 morning recall, unchanged |
| 3 | Heartbeat-native execution preserved? | III | **PASS** — no changes to heartbeat config or execution; documentation only |
| 4 | Single source of truth respected? | IV | **PASS** — TOKEN-ANALYSIS.md becomes the single source for token estimates (replacing scattered ARCHITECTURE.md fragments) |
| 5 | Agent Skills compliance maintained? | V | **PASS** — SKILL.md not modified; document lives in `docs/` |
| 6 | Token budget <5K/tick, ~44K/night? | TC | **PASS** — no runtime changes; document verifies compliance against corrected ~44K figure |
| 7 | Non-destructive install? | TC | **PASS** — new file creation only, no existing files modified |

All 7 gates pass. No violations.

## Project Structure

### Documentation (this feature)

```text
specs/002-token-analysis/
├── plan.md              # This file
├── research.md          # Phase 0: token estimation methodology research
├── data-model.md        # Phase 1: TickProfile and NightProfile entities
├── quickstart.md        # Phase 1: quick-reference summary
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
docs/
├── ARCHITECTURE.md      # Existing — cost section updated with cross-reference to TOKEN-ANALYSIS.md
└── TOKEN-ANALYSIS.md    # NEW — standalone token analysis document (FR-001)
```

No contracts/ directory needed — this feature produces a documentation artifact with no
external interfaces (no APIs, CLIs, or user-facing interactions).

**Structure Decision**: Documentation-only feature. Single new file at `docs/TOKEN-ANALYSIS.md`.
No source code changes, no test changes, no script changes.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
