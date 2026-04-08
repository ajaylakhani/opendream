# Research — README & Contributing Guide

**Feature**: 004-readme-contributing
**Date**: 2026-04-07

---

## R1: Hero image format and sourcing strategy

**Context**: The spec requires a hero image stored in `assets/` that visually
represents an AI dreaming. It must render on GitHub and have meaningful alt text.

**Decision**: Use a PNG file at `assets/hero.png`. Provide a placeholder
reference in the README now; the user will supply or generate the actual image
separately. The README image tag uses a relative path: `![...](assets/hero.png)`.

**Rationale**: PNG is universally supported by GitHub's Markdown renderer.
SVG is also supported but can have rendering inconsistencies with complex
artwork. A relative path ensures the image works without external hosting and
survives forks. The image should be landscape-oriented, approximately 1280×640px
(GitHub's social preview ratio), to display well on both the repo page and
social sharing.

**Alternatives considered**:
- External hosting (Imgur, Cloudinary) → rejected: breaks on forks, adds
  external dependency, violates the "version-controlled" requirement (FR-013).
- SVG → viable but risky for photographic or AI-generated artwork; PNG is
  safer for visual fidelity.
- ASCII art banner → rejected: lacks the "snazzy" visual impact requested.

---

## R2: Badge service and badge selection

**Context**: FR-007 requires badges for license, compatibility, and Python
version. Need to choose a badge service and determine which badges to display.

**Decision**: Use shields.io static badges with the following set:
1. `License: MIT` (green)
2. `Platform: OpenClaw | Hermes` (blue)
3. `Python: 3.10+` (blue)
4. `Status: Experimental` (orange) — honest signal that the project is early

**Rationale**: shields.io is the de facto standard for GitHub README badges.
Static badges (`img.shields.io/badge/...`) require no API integration and
never break. Four badges provide useful metadata without clutter.

**Alternatives considered**:
- Dynamic badges (build status, coverage) → rejected: no CI pipeline exists
  yet; adding fake "passing" badges would be misleading.
- badgen.net → viable alternative but less widely recognized.
- No badges → rejected: FR-007 explicitly requires them.

---

## R3: README section ordering and structure

**Context**: The README needs to balance visual appeal ("snazzy") with
information architecture (installation, how it works, cost, contributing).

**Decision**: Top-to-bottom ordering:
1. Hero image (full-width, centered)
2. Badges (inline, centered below image)
3. One-line tagline + 2-sentence description
4. "What is OpenDream?" (dreamer framing, Philip K. Dick attribution)
5. "Dream Architecture" (5-cycle table)
6. "How It Works" (heartbeat mechanism summary)
7. "Quick Start" (setup.py command)
8. "Manual Installation" (link to INSTALL.md)
9. "Validate" (validate.py command)
10. "Cost" (model tier cost table)
11. "Documentation" (links to ARCHITECTURE.md, REFERENCE.md, TOKEN-ANALYSIS.md)
12. "Contributing" (link to CONTRIBUTING.md)
13. "License" (MIT, one line)
14. "Acknowledgements" (Philip K. Dick inspiration)

**Rationale**: The hero image + badges + tagline pattern is standard for
high-quality open-source READMEs. Placing "What is OpenDream?" before
technical details ensures the dreamer framing (Principle I) is the first
thing a visitor reads. Installation comes after architecture so the reader
understands *what* they're installing before *how*. Cost at the end because
it's a secondary concern.

**Alternatives considered**:
- Installation first → rejected: "snazzy" means leading with visual impact
  and concept, not a pip install command.
- Collapsible details for installation → viable for later but adds complexity
  for v1; keep it flat.

---

## R4: CONTRIBUTING.md structure for a prompt-engineering project

**Context**: OpenDream is unusual — it's not a traditional library or app.
Contributions involve Markdown prompts, YAML configuration, and Python
validation scripts. The contributing guide must reflect this.

**Decision**: CONTRIBUTING.md sections:
1. Welcome & project philosophy (brief)
2. Prerequisites (Python 3.10+, OpenClaw or Hermes workspace)
3. Development Setup (clone, run validate.py)
4. Types of Contributions (bug reports, documentation, prompt tuning,
   Python scripts, new features)
5. Code Style:
   - Python: standard conventions, type hints, run `python3 -m py_compile`
   - Markdown/YAML: consistent indentation, no trailing whitespace
   - Commit messages: conventional commits (`feat:`, `fix:`, `docs:`)
6. Branching & PRs (fork, feature branch, one concern per PR, descriptive title)
7. Feature Development Workflow (reference speckit: `/speckit.specify` →
   `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`)
8. Issue Reporting (reproduction steps, expected vs actual, environment)
9. Code of Conduct (Contributor Covenant reference, brief)

**Rationale**: Separating "types of contributions" clarifies that prompt
tuning and YAML edits are first-class contributions, not just code. The
speckit reference (FR-011) is placed under "Feature Development" so it
doesn't intimidate small-fix contributors. Code of Conduct is expected
for any serious open-source project.

**Alternatives considered**:
- Full Contributor Covenant file → could add later; a summary with a link
  is sufficient for launch.
- DCO sign-off requirement → rejected: too heavy for a small project.

---

## R5: LICENSE file strategy

**Context**: SKILL.md declares `license: MIT` in frontmatter. GitHub
recognizes LICENSE files at the repo root for its license badge and
detection. No LICENSE file currently exists.

**Decision**: Create a `LICENSE` file at the repo root containing the
standard MIT license text with copyright holder "Ajay Lakhani" and
year 2026. This is a minor addition beyond the spec's scope but
directly supports FR-007 (license badge) and GitHub's license detection.

**Rationale**: Without a LICENSE file, GitHub won't auto-detect the license
or show the license badge in the repo sidebar. The MIT text is already
declared in SKILL.md — this just materializes it as a standard file.

**Alternatives considered**:
- No LICENSE file → GitHub won't detect the license; badge would be
  a static shields.io badge only, missing GitHub's native detection.
- Creative Commons → rejected: MIT is already declared and is standard
  for code + documentation projects.
