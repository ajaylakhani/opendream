# Feature Specification: README & Contributing Guide

**Feature Branch**: `004-readme-contributing`  
**Created**: 2026-04-07  
**Status**: Draft  
**Input**: User description: "create a README with instructions. Make it snazzy and have a hero image. need a contributing.md as i plan for this to be opensource"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Discover & Understand OpenDream (Priority: P1) 🎯 MVP

A developer discovers the OpenDream repository on GitHub. They land on the README and within 60 seconds understand what OpenDream is, see a compelling hero image, and know whether it's relevant to them. The README conveys the project's personality — an AI agent that dreams — through visual flair, clear structure, and concise language.

**Why this priority**: The README is the front door. Without it, no one installs, no one contributes. A visually striking README with a hero image creates immediate intrigue and signals quality.

**Independent Test**: Open the README on GitHub. Verify: (1) hero image renders and sets the tone, (2) project purpose is clear within the first paragraph, (3) the 5-cycle dream architecture is summarised visually, (4) installation instructions are present and complete, (5) a link to the contributing guide exists.

**Acceptance Scenarios**:

1. **Given** a visitor lands on the GitHub repo, **When** they view the README, **Then** they see a hero image at the top that visually represents the concept of an AI dreaming.
2. **Given** a developer reads the README, **When** they reach the "Getting Started" section, **Then** they find both quick-start (setup script) and manual installation paths with clear commands.
3. **Given** a developer reads the README, **When** they scan the page, **Then** they see the 5-cycle dream architecture presented in a visually appealing format (table showing cycle name, time window, and cognitive purpose).
4. **Given** a developer reads the README, **When** they look for licensing and contribution info, **Then** they find an MIT license badge and a link to CONTRIBUTING.md.

---

### User Story 2 — Install OpenDream from the README (Priority: P2)

A developer decides to install OpenDream after reading the README. They follow the installation instructions end-to-end and have a working dream skill in their OpenClaw or Hermes workspace without consulting any other documentation.

**Why this priority**: Installation instructions bridge interest and usage. If someone can't install from the README alone, the project loses users.

**Independent Test**: Follow only the README instructions on a fresh OpenClaw workspace. Verify: (1) setup.py runs without errors, (2) validate.py confirms installation, (3) no external documentation was needed.

**Acceptance Scenarios**:

1. **Given** a developer has an OpenClaw workspace, **When** they run the setup command from the README, **Then** the dream skill is installed and validate.py reports all checks passed.
2. **Given** a developer prefers manual installation, **When** they follow the manual steps in the README, **Then** they achieve the same result as the setup script.
3. **Given** a developer uses Hermes instead of OpenClaw, **When** they read the README, **Then** they find a Hermes compatibility note with the equivalent configuration.

---

### User Story 3 — Contribute to OpenDream (Priority: P3)

A developer wants to contribute to OpenDream — fix a bug, add a feature, or improve documentation. They read CONTRIBUTING.md and understand the contribution workflow, code standards, and how to get their changes reviewed and merged.

**Why this priority**: An open-source project without contribution guidelines creates friction for contributors and inconsistent quality for maintainers.

**Independent Test**: A new contributor reads CONTRIBUTING.md and can: (1) fork and set up the development environment, (2) understand the branching and PR conventions, (3) know what constitutes a good contribution, (4) find the code of conduct expectations.

**Acceptance Scenarios**:

1. **Given** a contributor reads CONTRIBUTING.md, **When** they look for setup instructions, **Then** they find how to clone, install prerequisites, and run validation.
2. **Given** a contributor wants to submit a change, **When** they read the PR section, **Then** they understand the expected PR format, branch naming, and review process.
3. **Given** a contributor is unsure about code standards, **When** they read the style section, **Then** they find concise guidelines covering Python scripts, Markdown/YAML prompts, and commit messages.
4. **Given** a contributor wants to report a bug, **When** they read CONTRIBUTING.md, **Then** they find guidance on filing issues with reproduction steps.

---

### Edge Cases

- What happens when the hero image URL is broken or blocked? The README must include meaningful alt text so the content remains comprehensible without the image.
- What happens when a contributor follows outdated installation instructions? The README should reference the validate.py script as the definitive check for correct installation.
- What happens when someone tries to install on an unsupported platform? The README should clearly state prerequisites (OpenClaw or Hermes, Python 3.x).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The README MUST display a hero image at the top that visually represents the concept of an AI dreaming, with descriptive alt text as fallback.
- **FR-002**: The README MUST include a concise project description (what OpenDream is, the dreamer framing, and the "inspired by" attribution to Philip K. Dick).
- **FR-003**: The README MUST present the 5-cycle dream architecture in a scannable visual format (table showing cycle name, time window, and cognitive purpose).
- **FR-004**: The README MUST include a "Quick Start" section with the setup.py command and expected output.
- **FR-005**: The README MUST include a "Manual Installation" section or link to the existing INSTALL.md reference.
- **FR-006**: The README MUST include a "Validate Installation" section showing the validate.py command.
- **FR-007**: The README MUST display badges for license (MIT), compatibility (OpenClaw/Hermes), and Python version.
- **FR-008**: The README MUST include a "How It Works" summary explaining the heartbeat mechanism, lightContext, and isolatedSession in accessible language.
- **FR-009**: The README MUST link to CONTRIBUTING.md, ARCHITECTURE.md, and REFERENCE.md for deeper reading.
- **FR-010**: CONTRIBUTING.md MUST include sections for: prerequisites, development setup, branching and PR conventions, code style guidelines (Python + Markdown/YAML), commit message format, issue reporting, and code of conduct summary.
- **FR-011**: CONTRIBUTING.md MUST reference the project's existing speckit-based feature workflow for larger changes.
- **FR-012**: The README MUST include a "Cost" section summarising per-night token costs across model tiers.
- **FR-013**: The hero image MUST be stored in the repository's `assets/` directory so it is version-controlled and not dependent on external hosting.

### Key Entities

- **README.md**: The project's primary entry point for GitHub visitors. Top-level file in the repository root.
- **CONTRIBUTING.md**: Contribution guidelines for open-source participants. Top-level file in the repository root.
- **Hero Image**: A visual asset stored in `assets/` that conveys the project's concept. Referenced by the README via a relative path.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new visitor can articulate what OpenDream does within 60 seconds of viewing the README.
- **SC-002**: A developer can complete installation from README instructions alone, confirmed by validate.py passing, within 5 minutes.
- **SC-003**: A contributor can submit their first pull request following only CONTRIBUTING.md guidance, without asking maintainers for process clarification.
- **SC-004**: The README renders correctly on GitHub with hero image visible, badges displayed, tables formatted, and all links functional.

## Assumptions

- The hero image will be a static image file (PNG or SVG) stored in `assets/`. The user will provide or generate the actual image separately; this spec covers the README's reference to it and the alt text, not image creation tooling.
- The MIT license is already declared in SKILL.md metadata. A LICENSE file may be created as part of this feature for GitHub recognition.
- The project uses conventional commits (e.g., `feat:`, `fix:`, `docs:`) based on observed commit history patterns.
- CONTRIBUTING.md will reference the speckit workflow (`/speckit.specify`, `/speckit.plan`, etc.) for feature-level contributions but will not require contributors to use it for small fixes.
- Python 3.10+ is the minimum version, based on the `str | None` type hints in existing scripts.
