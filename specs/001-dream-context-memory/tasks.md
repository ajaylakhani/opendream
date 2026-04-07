# Tasks: DreamContext Memory File

**Input**: Design documents from `/specs/001-dream-context-memory/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not requested in the feature specification. Test fixtures are provided for manual verification.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Exact file paths included in each task description

---

## Phase 1: Setup

**Purpose**: Create test fixtures and verify project structure is ready for implementation

- [X] T001 Create `tests/fixtures/` directory for memory file test fixtures
- [X] T002 [P] Create sparse memory fixture (1 entry) at `tests/fixtures/memory-sparse.md`
- [X] T003 [P] Create medium memory fixture (5 entries) at `tests/fixtures/memory-medium.md`
- [X] T004 [P] Create dense memory fixture (15 entries, mixed format: prose + bullets) at `tests/fixtures/memory-dense.md`

**Checkpoint**: Test fixtures ready for verifying dream quality against varied memory content

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add memory context extraction guidance to `prompts.yaml` — the single source of truth for all dream-time behaviour. All user stories depend on this.

**⚠️ CRITICAL**: US1, US2, and US3 cannot proceed without this phase.

- [X] T005 Add `memory_context` section to `assets/prompts.yaml` with extraction guidance (people, friction, tasks, observations, decisions) — per research decision R3
- [X] T006 Update `system_base` in `assets/prompts.yaml` with grounding rules: reference specific content from daily notes when available; dream from imagination when absent; never mention absence
- [X] T007 Update HEARTBEAT tick step 2 in `assets/HEARTBEAT-dream-section.md` to include extraction guidance and explicit `MEMORY.md` exclusion — per FR-006 and R2

**Checkpoint**: Foundation ready — memory context guidance is in place, tick instructions updated

---

## Phase 3: User Story 1 — Dream Tick Reads Today's Context (Priority: P1) 🎯 MVP

**Goal**: During dream ticks, the agent reads `memory/YYYY-MM-DD.md` and produces grounded dream thoughts referencing specific content from the day.

**Independent Test**: Copy `tests/fixtures/memory-medium.md` to `memory/YYYY-MM-DD.md`. Trigger a dream tick. Verify the thought references specific content rather than producing generic output.

- [X] T008 [US1] Update all 5 cycle instructions in `assets/prompts.yaml` to reference daily notes context for their specific cognitive purpose (e.g., Cycle 1 focuses on friction/tension from notes, Cycle 2 cross-references unrelated entries)
- [X] T009 [US1] Update morning recall instruction in `assets/prompts.yaml` to reference memory context when tracing themes
- [X] T010 [P] [US1] Update tick instructions in `SKILL.md` (section "What to do during a dream heartbeat tick") to add memory file read step with graceful skip and explicit `MEMORY.md` exclusion
- [X] T011 [P] [US1] Update `SKILL.md` morning recall section to note that themes should trace back to daily memory file

**Checkpoint**: User Story 1 complete — dream ticks read and use the daily memory file

---

## Phase 4: User Story 2 — Dream Quality with Varied Native Memory Content (Priority: P2)

**Goal**: Dream output remains meaningful regardless of memory file density or format — sparse, dense, structured, or unstructured.

**Independent Test**: Run dream ticks against all three fixtures (`memory-sparse.md`, `memory-medium.md`, `memory-dense.md`). Verify grounded thoughts in all cases, with appropriate scaling.

- [X] T012 [P] [US2] Add `format_guidance` to `memory_context` section in `assets/prompts.yaml` — instruct agent to handle bullets, prose, mixed entries, and unstructured content without expecting a fixed schema
- [X] T013 [P] [US2] Add `edge_cases` to `memory_context` section in `assets/prompts.yaml` — whitespace-only treated as absent, large files truncate naturally, read-only constraint reiterated

**Checkpoint**: User Story 2 complete — dream quality is resilient to varied native memory content

---

## Phase 5: User Story 3 — Morning Recall References Day Context (Priority: P3)

**Goal**: The morning recall at 06:00 MAY demonstrate thematic continuity with the day's memory file — tracing where the connection is natural, not forcing it.

**Independent Test**: Populate `memory/YYYY-MM-DD.md` with known entries. Run all 5 dream cycles. Generate the morning recall. Review whether themes trace back naturally — accept both connected and disconnected outcomes.

- [X] T014 [US3] Update morning recall instruction in `assets/prompts.yaml` to explicitly read `memory/YYYY-MM-DD.md` alongside cycle files and optionally trace themes back to day context — do not force the link
- [X] T015 [US3] Update morning recall tick step in `assets/HEARTBEAT-dream-section.md` to include optional reading of `memory/YYYY-MM-DD.md` for thematic tracing

**Checkpoint**: User Story 3 complete — morning recall optionally connects dream processing back to the day

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, documentation, and verification across all stories

- [X] T016 [P] Update `scripts/validate.py` to add optional (non-critical) check for `memory/` directory presence — per research decision R4
- [X] T017 [P] Update `docs/ARCHITECTURE.md` with design decision: "Daily memory file as dream context input" — document the read-only consumer model and token budget analysis
- [X] T018 [P] Update `references/REFERENCE.md` with memory file interaction details — flow diagram update, memory/YYYY-MM-DD.md in file layout
- [X] T019 [P] Update `references/INSTALL.md` with memory directory prerequisite note
- [X] T020 Run `python3 scripts/validate.py` and verify all checks pass (4 critical + memory optional)
- [X] T021 Run quickstart.md verification steps to confirm end-to-end flow

**Checkpoint**: Feature complete — all documentation, validation, and verification done

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: No dependency on Phase 1 fixtures. BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) completion. Can run in parallel with US1.
- **User Story 3 (Phase 5)**: Depends on US1 (Phase 3) — morning recall builds on dream tick changes
- **Polish (Phase 6)**: Depends on all user stories being complete

### Within Each Phase

- Phase 1: T001 first (directory), then T002–T004 in parallel
- Phase 2: T005 before T006 (memory_context section must exist before system_base references it). T007 in parallel with T006.
- Phase 3: T008 before T009 (cycle instructions before morning recall). T010, T011 parallel after T008.
- Phase 4: T012, T013 fully parallel (independent additions to memory_context section)
- Phase 5: T014 before T015 (prompts.yaml instruction before HEARTBEAT tick step)
- Phase 6: T016–T019 fully parallel. T020, T021 sequential after all others.

### Parallel Opportunities

```
Phase 1:  T002 ─┐
          T003 ─┼─ all parallel (different fixture files)
          T004 ─┘

Phase 2:  T005 → T006 ─┐
                  T007 ──┘ parallel with T006

Phase 3:  T008 → T009
          T010 ─┐
          T011 ─┘ parallel with each other, after T008

Phase 4:  T012 ─┐
          T013 ─┘ fully parallel

Phase 6:  T016 ─┐
          T017 ─┼─ all parallel (different files)
          T018 ─┤
          T019 ─┘
          T020 → T021 (sequential validation)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup — create test fixtures
2. Complete Phase 2: Foundational — memory_context + system_base + HEARTBEAT updates
3. Complete Phase 3: User Story 1 — cycle instructions + SKILL.md updates
4. **STOP and VALIDATE**: Trigger a dream tick with `tests/fixtures/memory-medium.md` as today's memory file. Verify grounded output.
5. Deploy if ready — this alone delivers the core value

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Validate grounded dream output → Deploy (MVP!)
3. Add User Story 2 → Validate against all fixture densities → Deploy
4. Add User Story 3 → Validate morning recall tracing → Deploy
5. Polish → Final validation + documentation → Ship

---

## Notes

- This is a prompt/instruction project — tasks modify YAML and Markdown, not runtime code
- No tests need to be written (not requested). Verification is manual via fixtures + validate.py
- The memory file (`memory/YYYY-MM-DD.md`) is read-only — OpenDream never writes to it
- `MEMORY.md` must NOT be read during dream ticks — only the daily file
- Morning recall tracing is optional (SC-004) — mirrors human dream recall
