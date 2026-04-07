# Implementation Plan: NREM/REM Phase Mechanics

**Branch**: `003-nrem-rem-phases` | **Date**: 2026-04-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-nrem-rem-phases/spec.md`

## Summary

Split each dream cycle's ticks into two explicit phases — NREM (quiet, context
gathering, no output) and REM (active, dream generation) — mirroring human
sleep architecture. Add a `depth` attribute and progressive output-length
scaling so earlier cycles produce shorter/shallower thoughts and later cycles
produce longer/more vivid ones. Update HEARTBEAT.md with a phase-aware schedule,
prompts.yaml with NREM guidance and depth attributes, and TOKEN-ANALYSIS.md
with revised per-night totals (9 thoughts instead of 14).

## Technical Context

**Language/Version**: Markdown + YAML (prompt/instruction files), Python 3.x (validation scripts)
**Primary Dependencies**: None — NREM/REM is a prompt-level feature; no code dependencies
**Storage**: Flat files — `dreams/YYYY-MM-DD/cycle-{N}-{name}.md` (write), `memory/YYYY-MM-DD.md` (read-only)
**Testing**: `python3 scripts/validate.py` + manual review of dream output files
**Target Platform**: OpenClaw/Hermes agents with heartbeat mechanism
**Project Type**: Agent skill (prompt engineering + documentation)
**Performance Goals**: Each tick <5K tokens input. Nightly total ~44K tokens.
**Constraints**: `lightContext: true`, `isolatedSession: true`, 30-min tick interval, 23:00–06:00 active hours
**Scale/Scope**: 14 dream ticks + 1 morning recall = 15 ticks/night. Post-change: 5 NREM + 9 REM + 1 recall = 15 ticks/night.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Agent-Is-Dreamer | ✅ PASS | Feature preserves dreamer framing — NREM/REM are the agent's phases, not the user's. |
| II. Sleep Architecture Fidelity | ✅ PASS | Enhances fidelity — adds NREM/REM phase distinction within existing 5-cycle structure. Cycle order and count unchanged. |
| III. Heartbeat-Native Execution | ✅ PASS | Uses existing 30-min heartbeat ticks. No external scripts or API calls. Phase determination is purely time-based within HEARTBEAT.md. |
| IV. Single Source of Truth | ✅ PASS | Phase schedule in HEARTBEAT.md (tick logic), NREM guidance and depth in prompts.yaml (dream-time behaviour). No duplication. |
| V. Agent Skills Compliance | ✅ PASS | Self-contained changes within skill directory. No external dependencies. |
| Token Budget (<5K/tick) | ✅ PASS | NREM ticks are lighter (no output generation). REM ticks unchanged input profile. Both within <5K budget. |
| Nightly Total (~44K) | ⚠️ NOTE | NREM ticks may be slightly lighter on input (no cycle file needed for avoiding repeats), but the 15-tick count is unchanged. Net impact: nightly total stays ~44K input, output drops from ~327 to ~237 tokens (9 thoughts × ~18 + 1 recall × ~75). |

**Gate result: PASS** — all principles satisfied. Proceed to Phase 0.

**Post-design re-check (Phase 1 complete)**: All gates re-confirmed. Design
adds `depth` + `nrem_guidance` fields to prompts.yaml (Principle IV: SoT for
dream-time behaviour), phase schedule to HEARTBEAT.md (Principle IV: SoT for
tick logic), and HTML comment markers (no SoT violation — observability only).
No new external dependencies. Token budget unchanged.

## Project Structure

### Documentation (this feature)

```text
specs/003-nrem-rem-phases/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
assets/
├── HEARTBEAT-dream-section.md   # Modified: add phase schedule + NREM/REM tick logic
├── prompts.yaml                 # Modified: add depth attribute, NREM guidance, widen word limit
├── SOUL-fragment.md             # Unchanged
├── openclaw.json                # Unchanged
└── viewer.html                  # Unchanged

docs/
├── ARCHITECTURE.md              # Modified: add NREM/REM design decision
└── TOKEN-ANALYSIS.md            # Modified: update tick counts, output totals

scripts/
├── validate.py                  # May need update: validate NREM marker presence
├── setup.py                     # Unchanged
└── dream_events.py              # Unchanged

SKILL.md                         # May need update: reflect NREM/REM in description
```

**Structure Decision**: No new files created. All changes are modifications to existing
prompt/instruction files and documentation. This is a prompt-engineering feature — no
source code directories needed.


