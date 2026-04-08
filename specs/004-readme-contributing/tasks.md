# Tasks: README & Contributing Guide

**Input**: Design documents from `/specs/004-readme-contributing/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: No new project structure needed — this feature creates new files at the repo root and in the existing `assets/` directory. Phase 1 is a no-op.

*(No tasks — skip to Phase 2)*

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the LICENSE file and hero image placeholder that both US1 and US3 depend on.

- [X] T001 Create the MIT license file at `LICENSE` in the repo root — copyright "Ajay Lakhani", year 2026, standard MIT text
- [X] T002 [P] Create a placeholder hero image reference at `assets/hero.png` — add a minimal 1×1 PNG placeholder so the README image tag doesn't break before the user supplies the real image

**Checkpoint**: LICENSE file exists for badge/link references. Hero image path exists for README image tag.

---

## Phase 3: User Story 1 — Discover & Understand OpenDream (Priority: P1) 🎯 MVP

**Goal**: Create the README.md with hero image, badges, project description, dream architecture table, how it works summary, and documentation links — so visitors immediately understand what OpenDream is.

**Independent Test**: Open README.md on GitHub. Verify: hero image renders (or shows alt text), badges display, project description uses dreamer framing, 5-cycle table is present, documentation links work.

- [X] T003 [US1] Create `README.md` at the repo root with hero image (centered, with descriptive alt text referencing `assets/hero.png`), four shields.io badges (MIT license, OpenClaw/Hermes platform, Python 3.10+, Experimental status), and a one-line tagline with two-sentence project description including Philip K. Dick attribution
- [X] T004 [US1] Add the "What is OpenDream?" section to `README.md` — explain the dreamer framing (the agent dreams, not the user), what happens during 23:00–06:00, and the cognitive purpose of the nightly process
- [X] T005 [US1] Add the "Dream Architecture" section to `README.md` — a table with columns: Cycle, Time Window, Name, Cognitive Purpose — covering all 5 cycles plus morning recall at 06:00
- [X] T006 [US1] Add the "How It Works" section to `README.md` — explain the heartbeat mechanism, `lightContext: true`, `isolatedSession: true`, and the read-process-write tick loop in accessible language, linking to `docs/ARCHITECTURE.md` for details
- [X] T007 [US1] Add the "Cost" section to `README.md` — a table with columns: Model, Approx Cost/Night — showing Local (£0), Haiku (~£0.014), Sonnet (~£0.17), linking to `docs/TOKEN-ANALYSIS.md` for the full breakdown
- [X] T008 [US1] Add the "Documentation" section to `README.md` — links to `docs/ARCHITECTURE.md` (design decisions), `references/REFERENCE.md` (technical detail), `docs/TOKEN-ANALYSIS.md` (token budget), and `references/INSTALL.md` (manual installation)
- [X] T009 [US1] Add the "Contributing" and "License" and "Acknowledgements" footer sections to `README.md` — link to `CONTRIBUTING.md`, one-line MIT license note linking to `LICENSE`, and Philip K. Dick / *Do Androids Dream of Electric Sheep?* attribution

**Checkpoint**: README.md is complete with all sections from R3. A visitor can understand, evaluate, and navigate the project from this file alone.

---

## Phase 4: User Story 2 — Install OpenDream from the README (Priority: P2)

**Goal**: Add installation sections to README.md so a developer can install and validate OpenDream end-to-end from the README alone.

**Independent Test**: Follow only the README instructions on a fresh workspace. Run setup.py and validate.py — both should succeed.

- [X] T010 [US2] Add the "Quick Start" section to `README.md` (after "How It Works") — show `git clone`, `cd opendream`, `python3 scripts/setup.py` commands with expected output summary, and prerequisites (Python 3.10+, OpenClaw or Hermes workspace)
- [X] T011 [US2] Add the "Manual Installation" section to `README.md` — brief summary of the 5 manual steps (backup, merge HEARTBEAT, merge SOUL, create dreams/, configure gateway) with a link to `references/INSTALL.md` for full details
- [X] T012 [US2] Add the "Validate Installation" section to `README.md` — show `python3 scripts/validate.py` command and expected "All checks passed" output, plus a Hermes compatibility note referencing the cron config from `references/REFERENCE.md`

**Checkpoint**: A developer can install OpenDream from the README alone. SC-002 is satisfied.

---

## Phase 5: User Story 3 — Contribute to OpenDream (Priority: P3)

**Goal**: Create CONTRIBUTING.md with all sections needed for open-source contributors to understand how to participate.

**Independent Test**: A new contributor reads CONTRIBUTING.md and can fork, set up, understand code style, submit a PR, and file an issue — without asking the maintainer for clarification.

- [X] T013 [US3] Create `CONTRIBUTING.md` at the repo root with Welcome section (project philosophy — prompt engineering for AI cognition, all contribution types welcome) and Prerequisites section (Python 3.10+, OpenClaw or Hermes workspace for testing)
- [X] T014 [US3] Add the "Development Setup" section to `CONTRIBUTING.md` — clone, run `python3 scripts/validate.py`, and "Types of Contributions" subsection listing: bug reports, documentation improvements, prompt tuning (prompts.yaml), Python script improvements, new features
- [X] T015 [P] [US3] Add the "Code Style" section to `CONTRIBUTING.md` — Python guidelines (standard conventions, type hints, `python3 -m py_compile` check), Markdown/YAML guidelines (consistent indentation, no trailing whitespace), commit message format (conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`)
- [X] T016 [P] [US3] Add the "Branching & Pull Requests" section to `CONTRIBUTING.md` — fork workflow, feature branch naming (`NNN-short-name`), one concern per PR, descriptive title, link back to issue if applicable
- [X] T017 [US3] Add the "Feature Development Workflow" section to `CONTRIBUTING.md` — reference the speckit lifecycle (`/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`) for larger changes, note that small fixes don't require the full workflow
- [X] T018 [US3] Add the "Issue Reporting" and "Code of Conduct" sections to `CONTRIBUTING.md` — issue template guidance (reproduction steps, expected vs actual, environment info), and Contributor Covenant summary with link to the full text

**Checkpoint**: CONTRIBUTING.md is complete. A contributor can go from zero to merged PR following this guide alone. SC-003 is satisfied.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation — verify all links, rendering, and cross-references work.

- [X] T019 Review all relative links in `README.md` — verify each link target exists: `assets/hero.png`, `CONTRIBUTING.md`, `LICENSE`, `docs/ARCHITECTURE.md`, `docs/TOKEN-ANALYSIS.md`, `references/REFERENCE.md`, `references/INSTALL.md`, `scripts/setup.py`, `scripts/validate.py`
- [X] T020 Review all relative links in `CONTRIBUTING.md` — verify each link target exists: `scripts/validate.py`, and any cross-references to README.md

**Checkpoint**: All documentation links verified. SC-004 is satisfied.

---

## Dependencies

```
T001 ─┐
T002 ─┼─→ [Phase 2 complete] ─→ T003 → T004 → T005 → T006 → T007 → T008 → T009 ─→ [US1 ✓]
      │                          T010 → T011 → T012 ─→ [US2 ✓]
      │                          T013 → T014 ─┐
      │                                       ├─→ T015 ─┐
      │                                       ├─→ T016 ─┼─→ T017 → T018 ─→ [US3 ✓]
      │                                       └─────────┘
      └─→ T019 ─→ T020 ─→ [Polish ✓]
```

**Parallel opportunities**:
- Phase 2: T001 and T002 can run in parallel (different files)
- Phase 3 and Phase 5: US1 (README.md) and US3 (CONTRIBUTING.md) can run in parallel after Phase 2 — they edit different files
- Phase 5: T015 and T016 can run in parallel (different sections of CONTRIBUTING.md, no dependencies between them)
- Phase 4 depends on Phase 3 (US2 adds sections to the README.md created in US1)

## Implementation Strategy

**MVP**: Complete Phases 2 + 3 (foundational + US1). This delivers a README with hero image, badges, project description, architecture table, how it works, cost, and documentation links. The repository immediately becomes presentable on GitHub.

**Incremental delivery**:
1. Phase 2 + 3 → MVP: Discover & understand (US1)
2. Phase 4 → Installation from README (US2)
3. Phase 5 → Contribution guide (US3)
4. Phase 6 → Link validation and polish
