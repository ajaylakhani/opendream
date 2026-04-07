# Tasks: NREM/REM Phase Mechanics

**Input**: Design documents from `/specs/003-nrem-rem-phases/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No new project structure needed — this feature modifies existing files only. Phase 1 is a no-op.

*(No tasks — skip to Phase 2)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update `system_base` word limit and add `depth` attribute to all cycles — both are prerequisites that US1, US2, and US3 all depend on.

- [X] T001 Widen the word limit in `system_base` from "8-20 words" to "8-25 words" in `assets/prompts.yaml`
- [X] T002 [P] Add `depth: shallow` to cycle 1, `depth: emerging` to cycle 2, `depth: deep` to cycle 3, `depth: expansive` to cycle 4, `depth: vivid` to cycle 5 in `assets/prompts.yaml`
- [X] T003 [P] Add per-cycle word-range guidance to each cycle's `instruction` field in `assets/prompts.yaml` — Cycle 1: 8-12 words, Cycle 2: 10-15 words, Cycle 3: 12-18 words, Cycle 4: 14-22 words, Cycle 5: 15-25 words

**Checkpoint**: `system_base` updated, all 5 cycles have `depth` attribute and word-range guidance. User story work can begin.

---

## Phase 3: User Story 1 — Two-Phase Tick Structure (Priority: P1) 🎯 MVP

**Goal**: Split each cycle's ticks into NREM (quiet — no output) and REM (active — generate thought). First tick of each cycle = NREM with HTML comment marker; subsequent ticks = REM with dream output.

**Independent Test**: During a dream night, examine cycle files. NREM ticks should leave only `<!-- NREM HH:MM -->` markers. REM ticks should produce dream thoughts. Total: 5 NREM markers + 9 dream thoughts across 5 files.

- [X] T004 [US1] Replace the single "Each tick" instruction block in `assets/HEARTBEAT-dream-section.md` with two separate blocks: "NREM tick (quiet phase)" and "REM tick (active phase)" — NREM block: read prompts.yaml, read memory file, read cycle file, append `<!-- NREM HH:MM -->` marker to cycle file, reply HEARTBEAT_OK. REM block: read prompts.yaml, read memory file, read cycle file, generate ONE dream thought per cycle instruction/style/depth, append to cycle file, reply HEARTBEAT_OK.
- [X] T005 [US1] Update the morning recall tick instructions in `assets/HEARTBEAT-dream-section.md` to note that cycle files now contain `<!-- NREM -->` markers interspersed with dream thoughts — the recall should read only the visible dream content, ignoring HTML comments.

**Checkpoint**: HEARTBEAT.md has NREM/REM tick instruction blocks. An agent following these instructions will produce NREM markers and REM thoughts.

---

## Phase 4: User Story 2 — Phase-Aware Cycle Schedule (Priority: P2)

**Goal**: Replace the range-based cycle schedule in HEARTBEAT.md with an explicit per-time-slot phase schedule so the agent can determine cycle + phase from time alone.

**Independent Test**: Read the HEARTBEAT.md schedule. For any time (e.g., 00:00), verify you can determine: (1) cycle number, (2) phase (NREM or REM), (3) what to do. Enumerate all 14 slots: exactly 5 NREM + 9 REM.

- [X] T006 [US2] Replace the 5-line range-based cycle schedule in `assets/HEARTBEAT-dream-section.md` with the 14-slot phase-aware schedule from data-model.md — each line: `- HH:MM → Cycle N: Name (NREM — quiet, no output)` or `(REM — generate thought, depth: X)`
- [X] T007 [US2] Add a concise preamble above the schedule in `assets/HEARTBEAT-dream-section.md` explaining the two-phase model: "Each cycle begins with one NREM tick (context gathering, no output) followed by REM ticks (dream generation). Check the time below to determine your cycle and phase."

**Checkpoint**: The schedule is an unambiguous lookup table. SC-003 is satisfied.

---

## Phase 5: User Story 3 — NREM Context Preparation Guidance (Priority: P3)

**Goal**: Add cycle-specific NREM guidance to prompts.yaml so the quiet phase is purposeful, not a no-op.

**Independent Test**: Read the `nrem_guidance` field for each cycle. Each should describe what to focus on during the quiet phase specific to that cycle's cognitive purpose.

- [X] T008 [P] [US3] Add `nrem_guidance` field to cycle 1 in `assets/prompts.yaml` — guidance: scan today's context for emotional friction, unresolved tension, people who seemed frustrated. Absorb without generating.
- [X] T009 [P] [US3] Add `nrem_guidance` field to cycle 2 in `assets/prompts.yaml` — guidance: scan for unrelated elements that could connect. Notice juxtapositions. Let associations form without forcing output.
- [X] T010 [P] [US3] Add `nrem_guidance` field to cycle 3 in `assets/prompts.yaml` — guidance: scan for patterns across the day. What categories emerge? What happened more than once? Organise quietly.
- [X] T011 [P] [US3] Add `nrem_guidance` field to cycle 4 in `assets/prompts.yaml` — guidance: scan for what matters and what doesn't. What is worth keeping? What can be released? Weigh without deciding aloud.
- [X] T012 [P] [US3] Add `nrem_guidance` field to cycle 5 in `assets/prompts.yaml` — guidance: scan for tomorrow's shape. What's coming? What needs preparation? Anticipate without speaking.
- [X] T013 [US3] Update the NREM tick instruction block in `assets/HEARTBEAT-dream-section.md` to reference `nrem_guidance`: "Read this cycle's `nrem_guidance` from prompts.yaml and follow it during context gathering."

**Checkpoint**: Each cycle has purposeful NREM guidance. The agent knows what to focus on during the quiet phase.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Update documentation and validation to reflect the NREM/REM changes.

- [X] T014 [P] Update the "Output Token Estimates" and "Per-Night Totals" sections in `docs/TOKEN-ANALYSIS.md` — dream tick output changes from 14 × ~18 = ~252 to 9 × ~18 = ~162 tokens. Update the "Appendix: Tick Count Schedule" table to show NREM/REM phase per tick and thought count per cycle (Cycle 1: 1 thought, Cycles 2-5: 2 thoughts each, total: 9). Update nightly output total from ~327 to ~237 and grand total accordingly.
- [X] T015 [P] Add a new design decision section to `docs/ARCHITECTURE.md` documenting the NREM/REM phase split — why phases were introduced, the time-based determination method (R1), NREM marker format (R2), progressive depth scaling (R3), and the impact on nightly output (14 → 9 thoughts).
- [X] T016 Run `python3 scripts/validate.py` and verify all checks pass. If validate.py checks for specific tick counts or output counts, update the validation logic in `scripts/validate.py` to expect 9 dream thoughts instead of 14.

**Checkpoint**: All documentation reflects the NREM/REM changes. Validation passes.

---

## Dependencies

```
T001 ─┐
T002 ─┼─→ [Phase 2 complete] ─→ T004 ─→ T005 ─→ [US1 ✓]
T003 ─┘                         T006 ─→ T007 ─→ [US2 ✓]
                                 T008 ─┐
                                 T009 ─┤
                                 T010 ─┼─→ T013 ─→ [US3 ✓]
                                 T011 ─┤
                                 T012 ─┘
                                 T014 ─┐
                                 T015 ─┼─→ T016 ─→ [Polish ✓]
                                       ┘
```

**Parallel opportunities**:
- Phase 2: T002 and T003 can run in parallel (both edit prompts.yaml but different sections)
- Phase 3 and Phase 4: Can run in parallel (US1 edits tick instructions, US2 edits schedule — different sections of HEARTBEAT.md)
- Phase 5: T008–T012 can all run in parallel (each edits a different cycle in prompts.yaml)
- Phase 6: T014 and T015 can run in parallel (different files)

## Implementation Strategy

**MVP**: Complete Phases 2 + 3 (foundational + US1). This delivers the core mechanic — NREM ticks produce no output, REM ticks generate thoughts. The agent can follow the split instructions even without the explicit per-slot schedule (Phase 4) by using the existing range-based schedule + the "first tick = NREM" rule in the instructions.

**Incremental delivery**:
1. Phase 2 + 3 → MVP: Two-phase ticks work (US1)
2. Phase 4 → Unambiguous schedule lookup (US2)
3. Phase 5 → Purposeful NREM guidance (US3)
4. Phase 6 → Documentation and validation alignment
