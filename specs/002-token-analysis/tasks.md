# Tasks: Token Analysis Document

**Input**: Design documents from `specs/002-token-analysis/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Not requested — no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Verify empirical data and prepare document structure

- [X] T001 Measure current file sizes with `wc -c` and confirm they match plan.md estimates for all skill files
- [X] T002 Create `docs/TOKEN-ANALYSIS.md` with document header, methodology section, and measured file size table (FR-001, FR-007, FR-008)

---

## Phase 2: User Story 1 — Understand Nightly Token Cost (Priority: P1) 🎯 MVP

**Goal**: An operator can determine the per-tick and per-night token cost at each model tier

**Independent Test**: Read TOKEN-ANALYSIS.md — it answers "How many tokens does one dream night cost on Haiku vs Sonnet vs local?" without consulting any other file

### Implementation for User Story 1

- [X] T003 [US1] Write the dream tick input breakdown table in `docs/TOKEN-ANALYSIS.md` — system overhead, HEARTBEAT bootstrap, heartbeat prompt, prompts.yaml read, memory file read, cycle file read (FR-002, FR-003)
- [X] T004 [US1] Write the morning recall tick input breakdown table in `docs/TOKEN-ANALYSIS.md` — same components plus all 5 cycle file reads (FR-006)
- [X] T005 [US1] Write the output token estimates section in `docs/TOKEN-ANALYSIS.md` — dream tick (~10-25 tokens) and morning recall (~60-90 tokens) (FR-003)
- [X] T006 [US1] Write the per-night totals section in `docs/TOKEN-ANALYSIS.md` — 14 dream ticks + 1 morning recall, total input ~44K and output tokens (FR-003)
- [X] T007 [US1] Write the cost-by-model-tier table in `docs/TOKEN-ANALYSIS.md` — local (£0), Haiku, Sonnet with pricing date and formula (FR-004)

**Checkpoint**: At this point, User Story 1 should be fully functional — an operator can determine nightly cost at any tier

---

## Phase 3: User Story 2 — Identify Where Token Budget Is Spent (Priority: P2)

**Goal**: A developer can identify which component consumes the most tokens and where headroom exists

**Independent Test**: Read TOKEN-ANALYSIS.md — it shows a per-component breakdown with min/typical/max and percentage of 5K budget

### Implementation for User Story 2

- [X] T008 [US2] Write the component budget breakdown table in `docs/TOKEN-ANALYSIS.md` — each component with min/typical/max tokens and percentage of 5K limit (FR-002)
- [X] T009 [US2] Write the worked example in `docs/TOKEN-ANALYSIS.md` — show how to recalculate headroom if prompts.yaml changes size (FR-007, SC-004)

**Checkpoint**: At this point, User Stories 1 AND 2 both work — developer can assess impact of file size changes

---

## Phase 4: User Story 3 — Validate Budget Compliance (Priority: P3)

**Goal**: A reviewer can verify constitutional compliance across all memory density scenarios

**Independent Test**: Read TOKEN-ANALYSIS.md — compliance section shows pass/fail for each scenario against <5K/tick and ~44K/night limits

### Implementation for User Story 3

- [X] T010 [US3] Write the compliance verification section in `docs/TOKEN-ANALYSIS.md` — 4 scenarios (no memory, sparse, medium, dense) with per-tick totals, pass/fail against <5K limit (FR-005)
- [X] T011 [US3] Write the nightly total compliance section in `docs/TOKEN-ANALYSIS.md` — verify ~44K measured total against corrected constitutional ~44K limit, document the correction from ~12K (FR-005)

**Checkpoint**: All three user stories complete — document is fully standalone per FR-001

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Cross-references and final validation

- [X] T012 Add cross-reference in `docs/ARCHITECTURE.md` — update the "Cost per tick" section to point to `docs/TOKEN-ANALYSIS.md` for detailed analysis
- [X] T013 Final review of `docs/TOKEN-ANALYSIS.md` — verify SC-001 (30-second cost lookup), SC-002 (100% token attribution), SC-003 (pass/fail per scenario), SC-004 (worked example present)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **User Story 1 (Phase 2)**: Depends on T002 (document structure exists)
- **User Story 2 (Phase 3)**: Depends on T003 (component breakdown data needed for budget percentages)
- **User Story 3 (Phase 4)**: Depends on T003 (component data needed for compliance totals)
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after T002 — no dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 T003 for component data — but can start in parallel with T004-T007
- **User Story 3 (P3)**: Depends on US1 T003 for component data — but can start in parallel with T004-T007

### Parallel Opportunities

- T003 and T004 can run in parallel (different sections of the same document)
- T008 can start as soon as T003 is complete (uses the same component data)
- T010 can start as soon as T003 is complete (uses the same component data)
- T012 and T013 can run in parallel (different files)

---

## Parallel Example: User Story 1

```
# After T002 creates document structure:
Parallel: T003 (dream tick breakdown) + T004 (morning recall breakdown)
Sequential: T005 (output tokens) → T006 (per-night totals) → T007 (cost table)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: User Story 1 (T003-T007)
3. **STOP and VALIDATE**: Does the document answer "How much does a dream night cost?"
4. If yes — MVP delivered

### Incremental Delivery

1. T001-T002 → Document structure ready
2. T003-T007 → Nightly cost visible → MVP!
3. T008-T009 → Component budget breakdown → Developer utility
4. T010-T011 → Compliance verification → Governance value
5. T012-T013 → Cross-references and final review → Complete

### Single-Author Strategy (expected for documentation)

All tasks are sequential for a single author — total effort is writing ~200-300 lines of Markdown with tables, using measured data from the plan's Technical Context section.
