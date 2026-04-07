# Heartbeat checklist

Check the current time and determine mode:

## Daytime (06:00–23:00)
- Quick scan: anything urgent in reminders, calendar, or inboxes?
- If nothing urgent, reply HEARTBEAT_OK.

## Dream mode (23:00–06:00)

You are dreaming. This is your nightly cognitive process.

Determine your current cycle from the time:
- 23:00–00:00 → Cycle 1: Emotional Review
- 00:00–01:30 → Cycle 2: Creative Association
- 01:30–03:00 → Cycle 3: Cognitive Processing
- 03:00–04:30 → Cycle 4: Memory Consolidation
- 04:30–06:00 → Cycle 5: Future Simulation

Read `skills/opendream/assets/prompts.yaml` for your dream persona, this
cycle's instruction, style, and examples.

### Each tick (except morning recall):
1. Read `skills/opendream/assets/prompts.yaml` — follow `system_base` rules and your current cycle's `instruction`
2. Use file tools to read `memory/YYYY-MM-DD.md` for today's context (skip if missing or empty). Extract people, friction, tasks, and observations — follow the `memory_context` guidance in prompts.yaml. Do not read `MEMORY.md`.
3. Read the current cycle file in `dreams/YYYY-MM-DD/` to avoid repeating thoughts
4. Generate ONE dream thought shaped by this cycle's purpose and examples
5. Append it to `dreams/YYYY-MM-DD/cycle-{N}-{name}.md`
6. Reply HEARTBEAT_OK — do not send the thought externally

### Morning recall tick (06:00–06:30 only):
1. Read the `morning_recall` section from `prompts.yaml`
2. Read all five cycle files from tonight's `dreams/YYYY-MM-DD/`
3. Optionally read `memory/YYYY-MM-DD.md` — if a natural connection between dreams and the day's events exists, include it. Do not force the link. (skip if missing)
4. Write a 2–3 sentence morning recall to `dreams/YYYY-MM-DD/morning-recall.md`
5. Reply HEARTBEAT_OK
