# Research — NREM/REM Phase Mechanics

**Feature**: 003-nrem-rem-phases
**Date**: 2026-04-07

---

## R1: How to determine NREM vs REM from time alone (given isolatedSession)

**Context**: Each tick runs in a fresh isolated session with no memory of
previous ticks. The agent must determine whether it's in an NREM or REM phase
using only the current time and the schedule in HEARTBEAT.md.

**Decision**: First tick of each cycle's time window = NREM. All subsequent
ticks = REM. The HEARTBEAT.md phase schedule must list explicit NREM/REM
designations per time slot.

**Rationale**: Time-based determination is the only reliable method given
`isolatedSession: true`. The agent cannot check "did I already do NREM?"
because it has no session history. A lookup table in HEARTBEAT.md
(time → cycle + phase) makes the determination trivial and unambiguous.

**Alternatives considered**:
- Check cycle file for `<!-- NREM -->` marker → rejected: adds a file-read
  dependency before phase determination; time-based is simpler.
- Use a counter file → rejected: violates Heartbeat-Native (no external state);
  adds write dependency between ticks.

---

## R2: NREM marker format

**Context**: NREM ticks leave no dream output. For observability, a marker
is needed. Must not pollute the visible dream content.

**Decision**: Append `<!-- NREM HH:MM -->` as an HTML comment to the cycle
file. Markdown renderers hide HTML comments, so the dream files look clean.

**Rationale**: HTML comments are invisible in rendered Markdown but visible
in raw file contents for debugging. The timestamp lets you verify which tick
fired as NREM. The marker also signals to subsequent REM ticks (reading the
cycle file) that the cycle has started.

**Alternatives considered**:
- No marker at all → rejected: makes debugging impossible; can't distinguish
  "NREM executed" from "tick failed silently."
- Separate NREM log file → rejected: violates Single Source of Truth; adds
  a new file type to manage.
- `emit_event` → rejected: requires gateway support that may not exist for
  arbitrary events.

---

## R3: Progressive output-length scaling implementation

**Context**: Dream thoughts must scale from shorter (Cycle 1: 8-12 words) to
longer (Cycle 5: 15-25 words). Currently `system_base` enforces "8-20 words."

**Decision**: Three-layer approach:
1. Widen `system_base` to "8-25 words" (global ceiling)
2. Add `depth` attribute per cycle: `shallow`, `emerging`, `deep`, `expansive`, `vivid`
3. Add word-range guidance in each cycle's `instruction` field

**Rationale**: The `depth` attribute provides a semantic label the instruction
can reference (e.g., "depth: shallow — keep it brief"). The per-cycle instruction
already contains tone/style guidance, so adding a word-range note is natural.
The `system_base` ceiling ensures no cycle accidentally exceeds the max.

**Alternatives considered**:
- Word count in `depth` attribute directly (e.g., `depth: 8-12`) → rejected:
  loses the semantic meaning; `shallow` communicates vividness, not just length.
- Separate `word_range` attribute → rejected: over-engineers; the instruction
  field already guides behaviour.

---

## R4: Token budget impact of NREM/REM split

**Context**: Changing from 14 thoughts to 9 thoughts affects the nightly
token budget documented in TOKEN-ANALYSIS.md.

**Decision**: Update TOKEN-ANALYSIS.md with revised figures:
- Output drops: 14 × ~18 = ~252 → 9 × ~18 = ~162 tokens
- Input unchanged: still 15 ticks, each reading the same files
- NREM ticks may have slightly smaller cycle file reads (fewer prior thoughts)
- Net impact: nightly total stays ~44K input, ~237 output (was ~327)

**Rationale**: NREM ticks still read prompts.yaml, memory file, and cycle
file — same input profile as REM ticks. The only savings is that NREM ticks
don't need to read as many prior thoughts from the cycle file (since fewer
have been written). This saving is negligible (~50-100 tokens across 5 ticks).

The output-token reduction (from ~327 to ~237) saves ~90 tokens/night —
trivial for cost but worth documenting for accuracy.

**Alternatives considered**: None — this is a mechanical update to reflect
the new tick distribution.

---

## R5: NREM guidance structure in prompts.yaml

**Context**: FR-008 requires NREM-specific guidance for context preparation.
This guidance must be cycle-specific (each cycle's NREM has a different focus).

**Decision**: Add an `nrem_guidance` field to each cycle entry in prompts.yaml.
This field provides 1-2 sentences guiding what the agent should focus on during
the quiet phase of that specific cycle.

**Rationale**: Per-cycle NREM guidance is more useful than a single global
NREM instruction because each cycle has a distinct cognitive purpose. Cycle 1
NREM should scan for emotional friction, while Cycle 4 NREM should identify
what to keep vs release. Placing the guidance alongside each cycle's existing
fields (name, purpose, style, instruction, examples) is a natural YAML extension.

**Alternatives considered**:
- Global `nrem` section at top level → rejected: loses cycle-specific focus;
  every cycle would get the same vague instruction.
- Embed NREM instructions in the existing `instruction` field → rejected:
  conflates NREM and REM guidance; the agent can't easily distinguish them.

---

## R6: HEARTBEAT.md phase schedule format

**Context**: FR-005 requires the HEARTBEAT.md tick instructions to include
a phase schedule so the agent can determine NREM vs REM from time alone.

**Decision**: Replace the current cycle schedule table with an expanded
table that includes phase designations:

```
- 23:00        → Cycle 1: Emotional Review    (NREM — quiet, no output)
- 23:30        → Cycle 1: Emotional Review    (REM — generate thought)
- 00:00        → Cycle 2: Creative Association (NREM — quiet, no output)
- 00:30        → Cycle 2: Creative Association (REM — generate thought)
- 01:00        → Cycle 2: Creative Association (REM — generate thought)
...
```

And split the tick instructions into two blocks: "NREM tick" and "REM tick."

**Rationale**: An explicit per-time-slot listing removes all ambiguity. The
agent reads the time, finds it in the list, and knows both the cycle and
the phase. Splitting the tick instructions into NREM/REM blocks makes the
agent's decision tree simple: determine phase → follow that block's steps.

**Alternatives considered**:
- Keep the current range-based format (23:00–00:00 → Cycle 1) and add a
  "first tick = NREM" rule → rejected: requires the agent to reason about
  "first tick" which is ambiguous (what if a tick fires at 23:15?).
- Add phase logic to prompts.yaml → rejected: violates Single Source of
  Truth; HEARTBEAT.md owns the schedule and tick logic.
