# Quickstart: DreamContext Memory File

**Feature**: 001-dream-context-memory

## What changed

OpenDream now explicitly reads the native OpenClaw daily memory file (`memory/YYYY-MM-DD.md`) during dream ticks and uses it to ground dream thoughts in the agent's actual day. Previously, the tick instructions referenced this file but provided no extraction guidance.

## After implementation

1. **Dream thoughts are grounded** — When `memory/YYYY-MM-DD.md` exists, dream output references specific people, events, friction, and tasks from the day.
2. **Graceful fallback** — When no memory file exists, dreaming proceeds from imagination only (no errors).
3. **prompts.yaml has extraction guidance** — A `memory_context` section tells the agent what to look for in the daily notes.
4. **Validation checks memory/** — `validate.py` now reports whether the `memory/` directory exists (optional, informational check).
5. **Test fixtures available** — Sample memory files at different densities for verifying dream quality.

## Verify it works

```bash
# 1. Run validation
python3 scripts/validate.py

# 2. Create a sample memory file for testing
mkdir -p ~/.openclaw/workspace/memory
cp tests/fixtures/memory-medium.md ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md

# 3. Wait for dream window (23:00) or trigger a manual heartbeat
openclaw system event --text "Dream tick test" --mode now

# 4. Check dream output
ls ~/.openclaw/workspace/dreams/$(date +%Y-%m-%d)/
cat ~/.openclaw/workspace/dreams/$(date +%Y-%m-%d)/cycle-1-emotional-review.md
```

## What to expect

- Dream thoughts in cycles 1-3 should reference content from the memory file
- Cycle 4 (Memory Consolidation) decides what matters from the day
- Cycle 5 (Future Simulation) rehearses tomorrow based on today's context
- Morning recall at 06:00 traces themes back to the day's events
