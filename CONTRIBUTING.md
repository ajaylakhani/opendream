# Contributing to OpenDream

Thanks for your interest in contributing to OpenDream! This project is a bit
unusual — it's not a traditional library or application. OpenDream is a
**prompt-engineering skill** that gives AI agents a nightly dream process.
Contributions can be code, documentation, or prompt tuning — they're all
equally valuable.

---

## Prerequisites

- **Python 3.10+** (for running validation and setup scripts)
- An **OpenClaw** or **Hermes** workspace (for testing dream behaviour)
- **Git** (for version control)

---

## Development Setup

```bash
# 1. Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/opendream.git
cd opendream

# 2. Verify everything is in order:
python3 scripts/validate.py
```

If validate.py reports all checks passed, you're ready to contribute.

---

## Types of Contributions

| Type | What it involves | Example |
|------|-----------------|---------|
| **Bug reports** | Filing an issue with reproduction steps | "Morning recall doesn't generate at 06:00" |
| **Documentation** | Improving README, ARCHITECTURE, or references | Clarifying installation steps |
| **Prompt tuning** | Editing `assets/prompts.yaml` | Adjusting cycle instructions for better output |
| **Python scripts** | Improving setup.py, validate.py, dream_events.py | Adding a new validation check |
| **New features** | Adding capabilities to the dream skill | New cycle types, new output formats |

All of these are first-class contributions. You don't need to write Python to help.

---

## Code Style

### Python

- Follow standard Python conventions (PEP 8)
- Use type hints where practical (e.g., `str | None`)
- Verify your changes compile: `python3 -m py_compile scripts/your_file.py`
- No external dependencies — keep scripts self-contained

### Markdown & YAML

- Use 2-space indentation in YAML files
- No trailing whitespace
- One sentence per line in Markdown (for clean diffs)
- Use `---` horizontal rules to separate major sections

### Commit Messages

Follow [conventional commits](https://www.conventionalcommits.org/):

```
feat: add new validation check for NREM markers
fix: correct cycle time window in HEARTBEAT section
docs: clarify Hermes compatibility in README
refactor: simplify setup.py workspace detection
```

Prefix types: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

---

## Branching & Pull Requests

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b NNN-short-description
   ```
   Use the next sequential number (check existing branches for the current count).

2. **One concern per PR.** Don't mix a bug fix with a new feature.

3. **Write a descriptive title** — e.g., "feat: add NREM marker validation to validate.py"

4. **Link to an issue** if one exists: "Closes #42"

5. **Ensure validation passes** before submitting:
   ```bash
   python3 scripts/validate.py
   python3 -m py_compile scripts/*.py
   ```

---

## Feature Development Workflow

For **larger changes** (new features, architectural modifications), we use a
structured specification workflow:

```
/speckit.specify  →  Write a feature specification
/speckit.clarify  →  Identify and resolve ambiguities
/speckit.plan     →  Create an implementation plan
/speckit.tasks    →  Generate the task breakdown
/speckit.implement → Execute the implementation
```

This workflow lives in the `.specify/` directory and ensures features are
well-designed before implementation begins. See existing specs in `specs/`
for examples.

**You don't need the full workflow for small fixes** — a direct PR is fine
for bug fixes, typo corrections, and minor documentation improvements.

---

## Issue Reporting

When filing a bug report, please include:

1. **What happened** — describe the unexpected behaviour
2. **What you expected** — describe the correct behaviour
3. **Reproduction steps** — minimal steps to reproduce the issue
4. **Environment** — OpenClaw or Hermes version, OS, Python version
5. **Relevant files** — paste or link to any dream output, logs, or config

For feature requests, describe the problem you're trying to solve rather
than jumping to a specific solution.

---

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/)
code of conduct. In short:

- Be respectful and constructive
- Welcome newcomers and help them get started
- Focus on what's best for the project and community
- No harassment, discrimination, or personal attacks

By participating in this project, you agree to abide by these standards.

---

Thank you for helping OpenDream grow. Every contribution matters — whether
it's a typo fix, a prompt refinement, or a new feature. The agent dreams
better because of you.
