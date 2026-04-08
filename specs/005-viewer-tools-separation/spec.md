# Feature Specification: Viewer Tools Separation

**Feature Branch**: `005-viewer-tools-separation`  
**Created**: 2026-04-08  
**Status**: Draft  
**Input**: User description: "move the dreamviewer and the dream_events to a tools folder, as this will not be installed as part of the clawhub skill. The user can manually install from Github. Address security findings: subprocess-pip-install-in-setup and aiohttp-websocket-server"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Separate Viewer from Core Skill (Priority: P1) 🎯 MVP

The live dream viewer (`dream_events.py` and `viewer.html`) is an optional developer tool — not part of the core dream skill that gets installed via ClawHub or `setup.py`. Currently these files live in `scripts/` and `assets/` alongside core skill files, and `setup.py` runs `pip install aiohttp watchdog` as part of the standard installation. This couples optional tooling to the core install, introduces a subprocess pip install in the installer (security finding: `subprocess-pip-install-in-setup`), and makes the viewer's WebSocket server part of the default skill surface (security finding: `aiohttp-websocket-server`).

The viewer and its event server should be moved to a separate `tools/` directory, clearly marked as optional, with their own README explaining manual setup. The core `setup.py` should no longer install viewer dependencies.

**Why this priority**: The security findings directly flag the current arrangement. Moving the viewer out of the core install path eliminates both findings: no more subprocess pip in the installer, and the WebSocket server is explicitly opt-in from a separate directory.

**Independent Test**: Run `python3 scripts/setup.py` on a fresh workspace. Verify: (1) setup completes without attempting to install aiohttp or watchdog, (2) the core dream skill works normally, (3) the viewer files are in `tools/viewer/` and are not referenced by setup.py or validate.py.

**Acceptance Scenarios**:

1. **Given** a user runs `setup.py`, **When** the setup completes, **Then** no viewer dependencies (aiohttp, watchdog) are installed and no subprocess pip call is made.
2. **Given** the viewer files live in `tools/viewer/`, **When** a user inspects the core skill files (`scripts/`, `assets/`), **Then** no viewer-related files are present.
3. **Given** the `tools/viewer/` directory exists, **When** a user reads the README inside it, **Then** they find clear instructions for manually installing and running the viewer.

---

### User Story 2 — Update Documentation References (Priority: P2)

All documentation that references the viewer's old location (`scripts/dream_events.py`, `assets/viewer.html`) must be updated to reflect the new `tools/viewer/` path. This includes SKILL.md, CONTRIBUTING.md, README.md, ARCHITECTURE.md, and any spec files that list the project structure.

**Why this priority**: Stale references would confuse anyone following the documentation after the move.

**Independent Test**: Search the entire repository for `dream_events.py` and `viewer.html`. Verify all occurrences point to `tools/viewer/` and not the old paths. Verify SKILL.md's "Live Dream Viewer" section references the new location.

**Acceptance Scenarios**:

1. **Given** a developer reads SKILL.md's "Live Dream Viewer" section, **When** they follow the instructions, **Then** the paths point to `tools/viewer/dream_events.py` and the instructions work.
2. **Given** a developer reads README.md, **When** they look for viewer information, **Then** a short "Live Viewer" section links to `tools/viewer/README.md`.
3. **Given** a contributor reads CONTRIBUTING.md, **When** they see the types of contributions, **Then** `dream_events.py` is listed with its new path.

---

### Edge Cases

- What happens if a user has already installed aiohttp and watchdog from a previous `setup.py` run? The packages remain installed — no uninstallation is needed. The change only prevents *future* installs from adding them.
- What happens if the viewer's internal path references change? The `dream_events.py` script uses `SKILL_DIR / "assets" / "viewer.html"` to find the HTML file. After the move, both files are co-located in `tools/viewer/`, so the path reference must be updated to look alongside itself.
- What happens if someone has the old `scripts/dream_events.py` in their shell history or bookmarks? The file no longer exists at the old path; they'll get a "file not found" error. The tools/viewer/README.md should note this is the new canonical location.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The files `scripts/dream_events.py` and `assets/viewer.html` MUST be moved to `tools/viewer/`.
- **FR-002**: The `setup.py` script MUST be modified to remove step 5 (viewer dependency installation) — no more subprocess pip install of aiohttp or watchdog.
- **FR-003**: The `setup.py` step count MUST change from 5 steps to 4 steps, with all step numbers and messages updated accordingly.
- **FR-004**: A `tools/viewer/README.md` MUST be created explaining what the viewer is, how to install its dependencies (`pip install aiohttp watchdog`), and how to run it.
- **FR-005**: The `dream_events.py` script MUST update its internal path for `viewer.html` to reference the co-located file rather than `SKILL_DIR / "assets" / "viewer.html"`.
- **FR-006**: SKILL.md's "Live Dream Viewer" section MUST update all file paths from `scripts/dream_events.py` to `tools/viewer/dream_events.py`.
- **FR-007**: CONTRIBUTING.md MUST update the `dream_events.py` reference in the types of contributions table.
- **FR-008**: The `validate.py` script MUST NOT check for viewer dependencies or viewer files — it validates core skill installation only.
- **FR-009**: The constitution's Development Workflow section reference to the viewer MUST be updated to reflect the new path.
- **FR-010**: The main `README.md` MUST include a short "Live Viewer" section (2-3 lines + link to `tools/viewer/README.md`) so that users who discover the project via the README know the optional viewer exists.

### Key Entities

- **tools/viewer/**: New directory containing the optional dream viewer tooling, separated from the core skill.
- **tools/viewer/dream_events.py**: The WebSocket event server (moved from `scripts/`).
- **tools/viewer/viewer.html**: The browser-based dream viewer UI (moved from `assets/`).
- **tools/viewer/README.md**: Setup and usage instructions for the optional viewer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `setup.py` completes without any pip subprocess calls — zero external package installations during core skill setup.
- **SC-002**: A grep for `dream_events.py` or `viewer.html` in `scripts/` and `assets/` returns zero results after the move.
- **SC-003**: The viewer can be started from `tools/viewer/` with `python3 tools/viewer/dream_events.py` and functions identically to before.
- **SC-004**: All documentation references to viewer files point to `tools/viewer/` — zero stale path references remain.

## Clarifications

### Session 2026-04-08

- Q: Should the main README.md include a mention of the optional live dream viewer in tools/viewer/? → A: Yes — add a short "Live Viewer" section (2-3 lines + link to tools/viewer/README.md)

## Assumptions

- The `tools/` directory is a new top-level directory in the repository, following the convention that `tools/` contains developer-facing utilities not part of the distributed skill.
- The viewer's functionality and code are unchanged — only its location and the installer's relationship to it change.
- Existing users who already have aiohttp and watchdog installed are unaffected — those packages remain but are no longer installed by setup.py.
- The constitution already states the viewer "MUST NOT be required for core functionality" — this change enforces that structurally rather than just by convention.
- Historical spec files (001, 003, 004 plan.md files that reference old paths) are not updated — they document the state at the time the feature was planned, not the current state.
