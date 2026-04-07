# Quickstart — NREM/REM Phase Mechanics

**Feature**: 003-nrem-rem-phases

---

## What changes

OpenDream's nightly dream process now mirrors human sleep more closely.
Each cycle's ticks are split into two phases:

- **NREM (quiet phase)**: The first tick of each cycle gathers context
  without generating output. It reads prompts.yaml, the memory file, and
  the cycle file, then silently marks its presence with an HTML comment.

- **REM (active phase)**: Subsequent ticks generate dream thoughts as before,
  but now with progressive depth — earlier cycles produce shorter, fragmented
  thoughts; later cycles produce longer, more vivid ones.

## What stays the same

- 15 ticks per night (same heartbeat interval, same active hours)
- 5 cycles in fixed order (Emotional Review → Future Simulation)
- Morning recall at 06:00
- All files in the same locations
- Token budget: <5K per tick, ~44K per night

## What's different

| Before | After |
|--------|-------|
| 14 dream thoughts per night | 9 dream thoughts per night |
| All ticks generate output | 5 NREM ticks (quiet) + 9 REM ticks (generate) |
| 8–20 word limit (all cycles) | 8–25 word limit (progressive: 8–12 in Cycle 1, 15–25 in Cycle 5) |
| No depth attribute | `depth` attribute per cycle: shallow → emerging → deep → expansive → vivid |
| No NREM markers | `<!-- NREM HH:MM -->` comment in cycle files |

## Files modified

1. **`assets/HEARTBEAT-dream-section.md`** — Phase-aware schedule + split NREM/REM tick instructions
2. **`assets/prompts.yaml`** — `depth` attribute, NREM guidance per cycle, widened word limit
3. **`docs/TOKEN-ANALYSIS.md`** — Updated output totals (9 thoughts instead of 14)
4. **`docs/ARCHITECTURE.md`** — New design decision documenting NREM/REM choice

## Verification

After implementation, verify:

1. Run `python3 scripts/validate.py` — all checks should pass
2. Check HEARTBEAT.md includes the phase schedule with NREM/REM designations
3. Check prompts.yaml includes `depth` and `nrem_guidance` for each cycle
4. Check `system_base` word limit is "8-25 words"
