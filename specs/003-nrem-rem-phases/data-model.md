# Data Model — NREM/REM Phase Mechanics

**Feature**: 003-nrem-rem-phases
**Date**: 2026-04-07

---

## Entities

### Phase

A tick's operational mode within a cycle.

| Attribute | Type | Values | Description |
|-----------|------|--------|-------------|
| type | enum | `NREM`, `REM` | Quiet (no output) or Active (dream generation) |

**Rules**:
- Each cycle contains exactly 1 NREM tick followed by 1+ REM ticks.
- NREM always precedes REM within a cycle (never interleaved).
- The morning recall tick (06:00) is neither NREM nor REM.

### Depth

A per-cycle attribute encoding progressive dream intensity.

| Cycle | Depth Value | Word Range | Character |
|-------|-------------|------------|-----------|
| 1 | `shallow` | 8–12 words | Short, incomplete, fragmented |
| 2 | `emerging` | 10–15 words | Associative, lateral, imagistic |
| 3 | `deep` | 12–18 words | Coherent, analytical, patterned |
| 4 | `expansive` | 14–22 words | Deliberate, considered, meaningful |
| 5 | `vivid` | 15–25 words | Alert, specific, forward-looking |

**Rules**:
- Depth scales monotonically from `shallow` to `vivid`.
- Word ranges overlap intentionally — depth guides intensity, not exact count.
- The `system_base` ceiling is 8–25 words (widened from 8–20).

### CyclePhaseSchedule

The complete mapping of tick times to cycles and phases.

| Time | Cycle | Phase | Depth |
|------|-------|-------|-------|
| 23:00 | 1 — Emotional Review | NREM | shallow |
| 23:30 | 1 — Emotional Review | REM | shallow |
| 00:00 | 2 — Creative Association | NREM | emerging |
| 00:30 | 2 — Creative Association | REM | emerging |
| 01:00 | 2 — Creative Association | REM | emerging |
| 01:30 | 3 — Cognitive Processing | NREM | deep |
| 02:00 | 3 — Cognitive Processing | REM | deep |
| 02:30 | 3 — Cognitive Processing | REM | deep |
| 03:00 | 4 — Memory Consolidation | NREM | expansive |
| 03:30 | 4 — Memory Consolidation | REM | expansive |
| 04:00 | 4 — Memory Consolidation | REM | expansive |
| 04:30 | 5 — Future Simulation | NREM | vivid |
| 05:00 | 5 — Future Simulation | REM | vivid |
| 05:30 | 5 — Future Simulation | REM | vivid |
| 06:00 | Morning Recall | — | — |

**Totals**: 5 NREM + 9 REM + 1 Recall = 15 ticks. 9 dream thoughts per night.

### NREM Marker

An HTML comment appended to the cycle file during NREM ticks.

| Attribute | Format | Example |
|-----------|--------|---------|
| marker | `<!-- NREM HH:MM -->` | `<!-- NREM 23:00 -->` |

**Rules**:
- Appended to the cycle file as the only write action during NREM.
- Invisible in rendered Markdown.
- Timestamp corresponds to the tick's scheduled time.

---

## State Transitions

### Per-Cycle Lifecycle

```
[Cycle starts] → NREM tick → REM tick(s) → [Cycle ends]
```

1. **NREM** (first tick): Read prompts.yaml, memory file, cycle file.
   Append `<!-- NREM HH:MM -->` marker. Reply HEARTBEAT_OK.
2. **REM** (subsequent ticks): Read prompts.yaml, memory file, cycle file.
   Generate one dream thought. Append to cycle file. Reply HEARTBEAT_OK.
3. Cycle ends when the next cycle's time window begins.

### Per-Night Lifecycle

```
23:00 [Cycle 1 NREM] → 23:30 [Cycle 1 REM] →
00:00 [Cycle 2 NREM] → 00:30 [Cycle 2 REM] → 01:00 [Cycle 2 REM] →
01:30 [Cycle 3 NREM] → 02:00 [Cycle 3 REM] → 02:30 [Cycle 3 REM] →
03:00 [Cycle 4 NREM] → 03:30 [Cycle 4 REM] → 04:00 [Cycle 4 REM] →
04:30 [Cycle 5 NREM] → 05:00 [Cycle 5 REM] → 05:30 [Cycle 5 REM] →
06:00 [Morning Recall]
```

---

## Relationships

- **Phase → Cycle**: Each phase belongs to exactly one cycle. A cycle contains exactly one NREM phase and one or more REM phases.
- **Depth → Cycle**: Each cycle has exactly one depth value. Depth determines word range and vividness for that cycle's REM ticks.
- **NREM Marker → Cycle File**: The marker is appended to the cycle's output file (`dreams/YYYY-MM-DD/cycle-{N}-{name}.md`).
