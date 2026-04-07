# Implementation Plan: DreamContext Memory File

**Branch**: `001-dream-context-memory` | **Date**: 2026-04-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-dream-context-memory/spec.md`

## Summary

OpenDream reads the native OpenClaw daily memory file (`memory/YYYY-MM-DD.md`) during dream ticks to ground dream thoughts in the agent's actual day. The implementation adds extraction guidance to `prompts.yaml`, updates tick instructions in `HEARTBEAT-dream-section.md` and `SKILL.md`, and validates graceful fallback when no memory file exists. The morning recall at 06:00 optionally traces dream themes back to the day's context — mirroring human dream recall where the connection may be clear, faint, or absent.

## Technical Context

**Language/Version**: Python 3.x (scripts), Markdown + YAML (prompts/instructions)  
**Primary Dependencies**: OpenClaw gateway (heartbeat mechanism), native file tools (read)  
**Storage**: Flat files — `memory/YYYY-MM-DD.md` (read-only), `dreams/YYYY-MM-DD/*.md` (write)  
**Testing**: Manual verification via `validate.py` + test fixtures in `tests/fixtures/`  
**Target Platform**: OpenClaw or Hermes agent gateway  
**Project Type**: Agent skill (prompt/instruction configuration, no runtime code)  
**Performance Goals**: <5K tokens per dream tick (including prompt overhead, memory file, and output)  
**Constraints**: `lightContext: true` (only HEARTBEAT.md bootstrapped), `isolatedSession: true` (no conversation history), 30-minute tick interval  
**Scale/Scope**: 14 dream ticks + 1 morning recall per night, single agent

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Status | Notes |
|---|-----------|--------|-------|
| I | Agent-Is-Dreamer | PASS | Memory file grounds the agent's own dream process. The agent reads its own day's context — not the user's. |
| II | Sleep Architecture Fidelity | PASS | 5-cycle structure preserved. Memory context feeds all cycles. Morning recall at 06:00 maintained. |
| III | Heartbeat-Native Execution | PASS | Memory file is read via tool calls during existing heartbeat ticks. No external scripts or API calls added. |
| IV | Single Source of Truth | PASS | Extraction guidance lives in `prompts.yaml` (single source for dream-time content). Tick logic stays in HEARTBEAT.md. |
| V | Agent Skills Compliance | PASS | No external dependencies added. Skill remains self-contained and portable across OpenClaw/Hermes. |
| — | Token budget (<5K/tick) | PASS | Memory file ~2,500 tokens + HEARTBEAT bootstrap ~400 + prompts.yaml ~800 + output ~30 = ~3,730 tokens. Within budget. |
| — | Non-destructive install | PASS | No new files created in workspace root. `validate.py` memory check is informational only. |

## Project Structure

### Documentation (this feature)

```text
specs/001-dream-context-memory/
├── plan.md              # This file
├── research.md          # Phase 0 output — 5 research decisions
├── data-model.md        # Phase 1 output — 3 entities (DayMemory, DreamThought, MorningRecall)
├── quickstart.md        # Phase 1 output — verification steps
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
skills/opendream/
├── SKILL.md                          # Skill manifest — tick instructions, morning recall, reporting
├── assets/
│   ├── prompts.yaml                  # Dream persona, cycle instructions, memory_context guidance
│   ├── HEARTBEAT-dream-section.md    # Tick execution logic (merged into workspace HEARTBEAT.md)
│   ├── SOUL-fragment.md              # Daytime reporting persona
│   ├── openclaw.json                 # Gateway config snippet
│   └── viewer.html                   # Live dream viewer (optional)
├── scripts/
│   ├── setup.py                      # Workspace installation
│   ├── validate.py                   # Post-install validation
│   └── dream_events.py               # Viewer SSE server (optional)
├── tests/
│   └── fixtures/
│       ├── memory-sparse.md          # 1 entry — minimal day
│       ├── memory-medium.md          # 5 entries — typical day
│       └── memory-dense.md           # 15 entries — busy day with mixed formats
├── docs/
│   └── ARCHITECTURE.md               # Design decisions
└── references/
    ├── REFERENCE.md                   # Technical reference
    └── INSTALL.md                     # Manual installation guide
```

**Structure Decision**: Single skill directory. No separate src/tests split — this is a prompt/instruction project, not a code project. Test fixtures are sample memory files for verifying dream quality.

## Complexity Tracking

No constitution violations. All gates pass. No complexity justifications needed.
