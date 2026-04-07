# Research: DreamContext Memory File

**Feature**: 001-dream-context-memory
**Date**: 2026-04-07

## R1: Native OpenClaw Memory File Behaviour

**Question**: How does OpenClaw populate `memory/YYYY-MM-DD.md` and what format does it use?

**Decision**: OpenClaw writes daily notes as plain Markdown during normal DM sessions. The format is OpenClaw-defined and may vary — free-form prose, bullet points, or structured entries. OpenDream treats it as opaque input.

**Rationale**: The OpenClaw Memory documentation confirms: "memory/YYYY-MM-DD.md — daily notes. Running context and observations. Today and yesterday's notes are loaded automatically." The file is written by the memory-core plugin. OpenDream cannot impose structure on it.

**Alternatives considered**:
- Define a strict schema for the memory file → Rejected: violates read-only consumer model; OpenClaw owns the file.
- Create a separate dream-context file → Rejected: duplicates data; adds complexity without benefit.

## R2: Context Loading During Dream Ticks

**Question**: What context is available to the agent during dream ticks (`lightContext: true` + `isolatedSession: true`)?

**Decision**: Only `HEARTBEAT.md` is bootstrapped. All other context must be read via tool calls. The agent reads `prompts.yaml` (dream persona/instructions) and `memory/YYYY-MM-DD.md` (daily context) each tick.

**Rationale**: OpenClaw Heartbeat docs confirm: `lightContext: true` "keeps only HEARTBEAT.md from workspace bootstrap files." The Context docs confirm bootstrap files are: AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md. With lightContext, only HEARTBEAT.md is injected. `isolatedSession: true` means no conversation history.

**Alternatives considered**:
- Also read `MEMORY.md` each tick → Rejected: too large for the ~5K token budget per tick; daily file is sufficient.
- Bootstrap memory file instead of tool-reading → Rejected: `lightContext: true` cannot be configured to include additional files beyond HEARTBEAT.md.

## R3: Memory Context Extraction Strategy

**Question**: How should prompts.yaml guide the agent to extract useful context from varying memory file formats?

**Decision**: Add a `memory_context` section to `prompts.yaml` with extraction guidance that applies across all cycles. Each cycle instruction already references "today's context" — the memory_context section formalises what to look for: people, friction, tasks, observations, decisions. The instructions are format-agnostic.

**Rationale**: Current `system_base` says "You may reference people and events from today's context naturally" — but provides no guidance on how to extract those from the file. Cycles 1–2 already reference "today's interactions" and "today's context" in their instructions. Adding explicit extraction guidance ensures consistent quality regardless of native memory file format.

**Alternatives considered**:
- Embed extraction logic in HEARTBEAT.md → Rejected: HEARTBEAT.md handles tick scheduling, not content interpretation. Violates Single Source of Truth (prompts.yaml owns dream-time behaviour).
- Let the agent figure it out with no guidance → Rejected: inconsistent quality; fragile to model changes.

## R4: Validation Script Updates

**Question**: What should `validate.py` check regarding the memory directory?

**Decision**: Add an optional (non-critical) check for the `memory/` directory presence. It is optional because OpenClaw creates it on first write — it may not exist before the agent has its first conversation.

**Rationale**: Current validation checks HEARTBEAT.md, SOUL.md, dreams/, and gateway config. Memory directory is an OpenClaw native directory, not created by OpenDream setup. Its absence is informational, not a setup failure.

**Alternatives considered**:
- Make it a critical check → Rejected: OpenClaw creates it automatically; failing setup validation for a missing native directory is misleading.
- Create directory in setup.py → Rejected: OpenDream should not create OpenClaw-owned directories.

## R5: Token Budget Analysis

**Question**: Does reading `memory/YYYY-MM-DD.md` fit within the ~5K token budget per tick?

**Decision**: Yes. The memory file for a typical day is under 2,000 words (~2,500 tokens). Combined with HEARTBEAT.md bootstrap (~400 tokens), prompts.yaml read (~800 tokens), and dream output (~30 tokens), the total stays within budget.

**Rationale**: Constitution mandates <5K tokens per tick. From ARCHITECTURE.md: "Each heartbeat tick is a full agent turn. With `isolatedSession: true` and `lightContext: true`, each tick costs roughly 2–5K tokens." The spec mandates (SC-005) that the memory file stays under 2,000 words. If a file exceeds the budget, the model's context window naturally truncates it — no explicit handling needed.

**Alternatives considered**:
- Summarise the memory file before dream ticks → Rejected: over-engineering; the file is expected to be concise. Token truncation handles edge cases.
- Read only relevant sections → Rejected: agent cannot determine relevance without reading the file first.
