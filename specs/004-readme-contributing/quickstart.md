# Quickstart — README & Contributing Guide

**Feature**: 004-readme-contributing
**Date**: 2026-04-07

---

## Before

The OpenDream repository has no README.md or CONTRIBUTING.md. A visitor
landing on the GitHub page sees a raw file listing with no context, no
installation guidance, and no contribution pathway. The project is
functionally invisible to potential users and contributors.

**Visitor experience**: Confusion. They must dig into SKILL.md, REFERENCE.md,
and INSTALL.md to piece together what the project does and how to use it.

**Contributor experience**: No guidance on code style, PR conventions, or
development workflow. Potential contributors leave.

---

## After

The repository has a polished README.md with:
- A hero image conveying the AI dreaming concept
- Badges for license (MIT), platform (OpenClaw/Hermes), Python (3.10+)
- Clear project description with the dreamer framing
- 5-cycle dream architecture table
- Quick start and manual installation instructions
- Cost summary
- Links to all documentation

And a CONTRIBUTING.md with:
- Development setup instructions
- Code style for Python + Markdown/YAML
- Branching and PR conventions
- Speckit workflow for feature development
- Issue reporting template guidance
- Code of conduct summary

Plus a LICENSE file for GitHub detection.

**Visitor experience**: Within 60 seconds they understand what OpenDream is,
see the dream architecture, and know how to install it.

**Contributor experience**: Clear pathway from first clone to merged PR,
with style guidelines and workflow documentation.

---

## Key Changes

| File | Change |
|------|--------|
| `README.md` | NEW — project entry point with hero image, badges, instructions, architecture, cost |
| `CONTRIBUTING.md` | NEW — open-source contribution guidelines |
| `LICENSE` | NEW — MIT license text for GitHub detection |
| `assets/hero.png` | NEW — hero image placeholder (user supplies actual image) |

**No existing files are modified.** All changes are additive.
