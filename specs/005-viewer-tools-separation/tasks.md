# Tasks: Viewer Tools Separation

**Input**: Design documents from `/specs/005-viewer-tools-separation/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

**Tests**: Not requested — no test tasks generated.

**Organization**: Tasks grouped by user story (US1: Separate Viewer, US2: Update Docs).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)
- Exact file paths included in all descriptions

---

## Phase 1: Setup

**Purpose**: Create the target directory for viewer tooling

- [x] T001 Create `tools/viewer/` directory at repository root

---

## Phase 2: User Story 1 — Separate Viewer from Core Skill (Priority: P1) 🎯 MVP

**Goal**: Move viewer files out of core skill directories into `tools/viewer/`, remove viewer dependency installation from `setup.py`, and provide standalone viewer setup instructions.

**Independent Test**: Run `python3 scripts/setup.py` on a fresh workspace. Verify: (1) setup completes without attempting to install aiohttp or watchdog, (2) `scripts/dream_events.py` and `assets/viewer.html` no longer exist, (3) `tools/viewer/dream_events.py`, `tools/viewer/viewer.html`, and `tools/viewer/README.md` all exist, (4) `python3 tools/viewer/dream_events.py` starts the viewer (with deps installed).

- [x] T002 [P] [US1] Move `scripts/dream_events.py` to `tools/viewer/dream_events.py` — update `VIEWER_HTML` path from `SKILL_DIR / "assets" / "viewer.html"` to `Path(__file__).resolve().parent / "viewer.html"` per R2, then delete `scripts/dream_events.py`
- [x] T003 [P] [US1] Move `assets/viewer.html` to `tools/viewer/viewer.html` (content unchanged), then delete `assets/viewer.html`
- [x] T004 [P] [US1] Create `tools/viewer/README.md` with purpose, prerequisites (Python 3.10+), install command (`pip install aiohttp watchdog`), usage instructions, and back-link to main README per R4
- [x] T005 [US1] Remove viewer dependency installation from `scripts/setup.py` — delete `VIEWER_DEPS` constant, `install_viewer_deps()` function, and step 5 call; change total step count from 5 to 4; update all step number references per R3

**Checkpoint**: Core skill installs cleanly without viewer deps. Viewer runs from `tools/viewer/`. Both security findings resolved.

---

## Phase 3: User Story 2 — Update Documentation References (Priority: P2)

**Goal**: All documentation references to the viewer point to the new `tools/viewer/` paths. Zero stale references remain.

**Independent Test**: Run `grep -rn "scripts/dream_events\|assets/viewer" . --include="*.md" --include="*.py"` from repo root. Verify zero results (excluding historical spec files in `specs/001-*` through `specs/004-*`).

- [x] T006 [P] [US2] Update `SKILL.md` "Live Dream Viewer (Optional)" section — change all paths from `scripts/dream_events.py` to `tools/viewer/dream_events.py` and update any `assets/viewer.html` references to `tools/viewer/viewer.html` per FR-006
- [x] T007 [P] [US2] Update `CONTRIBUTING.md` contributions type table — change `dream_events.py` reference to `tools/viewer/dream_events.py` per FR-007
- [x] T008 [P] [US2] Update `.specify/memory/constitution.md` Development Workflow section — change `scripts/dream_events.py` to `tools/viewer/dream_events.py` per FR-009

**Checkpoint**: All active documentation points to `tools/viewer/`. No stale path references in non-historical files.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and auto-generated file updates

- [x] T009 Update `.github/copilot-instructions.md` project structure via `update-agent-context.sh copilot`
- [x] T010 Run `python3 scripts/validate.py` and grep for stale viewer path references to confirm SC-001 through SC-004

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **US1 (Phase 2)**: Depends on Phase 1 (directory exists)
- **US2 (Phase 3)**: Can start after Phase 1 — does NOT depend on US1 completion (paths are known from plan)
- **Polish (Phase 4)**: Depends on Phase 2 and Phase 3 completion

### Within User Story 1

- T002, T003, T004 can all run in **parallel** (different files, no dependencies)
- T005 is independent of the file moves (modifies `setup.py` only)
- All Phase 2 tasks are parallelizable

### Within User Story 2

- T006, T007, T008 can all run in **parallel** (different files, no dependencies)

### Cross-Story

- US1 and US2 can technically proceed in **parallel** since the target paths (`tools/viewer/`) are known from the plan
- Polish phase (T009, T010) must wait for both stories to complete

---

## Parallel Example: User Story 1

```text
# All four US1 tasks can launch simultaneously:
T002: Move dream_events.py to tools/viewer/dream_events.py (update internal path)
T003: Move viewer.html to tools/viewer/viewer.html
T004: Create tools/viewer/README.md
T005: Remove viewer deps from scripts/setup.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (create directory)
2. Complete Phase 2: US1 (move files + modify setup.py)
3. **STOP and VALIDATE**: Run `setup.py`, verify no viewer dep install
4. Verify viewer works from `tools/viewer/`

### Incremental Delivery

1. Phase 1 → Directory ready
2. Phase 2 (US1) → Security findings resolved, viewer separated (MVP!)
3. Phase 3 (US2) → All docs updated, no stale references
4. Phase 4 (Polish) → Agent context updated, full validation pass

---

## FR Traceability

| FR | Task(s) | Description |
|----|---------|-------------|
| FR-001 | T002, T003 | Move files to `tools/viewer/` |
| FR-002 | T005 | Remove viewer dep install from setup.py |
| FR-003 | T005 | Step count 5→4 |
| FR-004 | T004 | Create `tools/viewer/README.md` |
| FR-005 | T002 | Update VIEWER_HTML internal path |
| FR-006 | T006 | Update SKILL.md viewer paths |
| FR-007 | T007 | Update CONTRIBUTING.md viewer reference |
| FR-008 | — | Already true (validate.py doesn't check viewer) |
| FR-009 | T008 | Update constitution.md viewer path |

## Notes

- [P] tasks = different files, no dependencies between them
- Historical spec files (001–004) are NOT updated — they document state at time of planning
- FR-008 requires no task — `validate.py` already does not check for viewer files or deps
- Commit after each phase for clean git history
