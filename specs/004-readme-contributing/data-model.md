# Data Model — README & Contributing Guide

**Feature**: 004-readme-contributing
**Date**: 2026-04-07

---

## Entities

### README.md

The project's primary entry point for GitHub visitors.

| Section | Purpose | Source of Truth |
|---------|---------|----------------|
| Hero Image | Visual hook — AI dreaming concept | `assets/hero.png` |
| Badges | License, platform, Python version, status | shields.io static URLs |
| Project Description | What OpenDream is + dreamer framing | Original content (summarises SKILL.md) |
| Dream Architecture | 5-cycle table | Summarises `assets/prompts.yaml` cycle data |
| How It Works | Heartbeat mechanism explanation | Summarises `docs/ARCHITECTURE.md` |
| Quick Start | setup.py installation command | References `scripts/setup.py` |
| Manual Installation | Link to detailed steps | Links to `references/INSTALL.md` |
| Validate | validate.py command | References `scripts/validate.py` |
| Cost | Per-night token cost table | Summarises `docs/TOKEN-ANALYSIS.md` |
| Documentation | Links to deeper docs | Links to ARCHITECTURE.md, REFERENCE.md, TOKEN-ANALYSIS.md |
| Contributing | Link to contribution guide | Links to `CONTRIBUTING.md` |
| License | MIT one-liner | References `LICENSE` file |

**Rules**:
- Summaries link to authoritative sources (Principle IV: SoT).
- Hero image uses relative path `assets/hero.png` with descriptive alt text.
- All internal links use relative paths (no absolute URLs to the repo).

### CONTRIBUTING.md

Contribution guidelines for open-source participants.

| Section | Purpose |
|---------|---------|
| Welcome | Project philosophy, what makes a good contribution |
| Prerequisites | Python 3.10+, OpenClaw/Hermes workspace |
| Development Setup | Clone, validate.py |
| Types of Contributions | Bug reports, docs, prompt tuning, scripts, features |
| Code Style | Python conventions, Markdown/YAML standards, commit format |
| Branching & PRs | Fork workflow, branch naming, one concern per PR |
| Feature Development | Speckit workflow for larger changes |
| Issue Reporting | Reproduction steps, expected vs actual |
| Code of Conduct | Contributor Covenant summary |

**Rules**:
- Speckit workflow is recommended for features, not required for small fixes.
- Code style covers both Python scripts and Markdown/YAML prompt files.

### Hero Image

A visual asset conveying the AI dreaming concept.

| Attribute | Value |
|-----------|-------|
| Path | `assets/hero.png` |
| Format | PNG |
| Dimensions | ~1280×640px (landscape, GitHub social preview ratio) |
| Alt text | Descriptive text for accessibility and broken-image fallback |

**Rules**:
- Must render on GitHub's Markdown renderer.
- Stored in repository (not externally hosted) per FR-013.
- User supplies the actual image; implementation creates a placeholder reference.

### LICENSE

Standard MIT license file for GitHub detection.

| Attribute | Value |
|-----------|-------|
| Path | `LICENSE` (repo root) |
| Type | MIT |
| Copyright | Ajay Lakhani, 2026 |

**Rules**:
- Must match the `license: MIT` declaration in SKILL.md frontmatter.
- Enables GitHub's native license detection and sidebar badge.

---

## Relationships

```
README.md
├── references → assets/hero.png (image)
├── references → CONTRIBUTING.md (link)
├── references → LICENSE (link)
├── references → docs/ARCHITECTURE.md (link)
├── references → docs/TOKEN-ANALYSIS.md (data source for cost table)
├── references → references/REFERENCE.md (link)
├── references → references/INSTALL.md (link)
├── references → scripts/setup.py (command reference)
└── references → scripts/validate.py (command reference)

CONTRIBUTING.md
├── references → scripts/validate.py (dev setup)
└── references → speckit workflow (feature development)

LICENSE
└── validates → SKILL.md frontmatter license field
```

---

## State Transitions

N/A — these are static documentation files with no runtime state.
