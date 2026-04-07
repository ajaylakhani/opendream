# Data Model: DreamContext Memory File

**Feature**: 001-dream-context-memory
**Date**: 2026-04-07

## Entities

### DayMemory (external, read-only)

A native OpenClaw daily notes file. OpenDream does not define or control this entity.

| Field | Type | Description |
|-------|------|-------------|
| path | string | `memory/YYYY-MM-DD.md` relative to workspace root |
| date | date | Calendar date derived from filename (ISO 8601) |
| content | markdown | Free-form Markdown — format varies by OpenClaw version and user configuration |
| owner | system | OpenClaw memory-core plugin (not OpenDream) |

**Lifecycle**: Created by OpenClaw on first daytime write. Populated throughout the day. Never modified by OpenDream.

**Relationships**: One DayMemory → many DreamThoughts (indirectly, via context extraction during dream ticks).

### DreamThought (existing, unchanged)

A single dream thought generated during a dream tick.

| Field | Type | Description |
|-------|------|-------------|
| path | string | `dreams/YYYY-MM-DD/cycle-{N}-{name}.md` |
| cycle | int (1-5) | Which dream cycle produced this thought |
| style | enum | `fragmented` (cycles 1-2) or `reflective` (cycles 3-5) |
| content | string | 8-20 words, one thought per tick |
| grounded | boolean | Whether the thought references specific DayMemory content |

**Lifecycle**: Created by appending during dream tick. Read during morning recall generation.

### MorningRecall (existing, unchanged)

A summary note written at 06:00 after all dream cycles.

| Field | Type | Description |
|-------|------|-------------|
| path | string | `dreams/YYYY-MM-DD/morning-recall.md` |
| content | string | 2-3 sentences summarising the night's processing |
| traces_to_memory | boolean | Whether themes trace back to DayMemory entries |

**Lifecycle**: Created once at 06:00 morning tick. Read when user asks about last night's dreams.

## State Transitions

```
DayMemory states (OpenClaw-managed):
  [absent] → [created] → [accumulating] → [stable]
              (first write)  (daytime)       (23:00, dream window opens)

DreamContext view (OpenDream):
  [absent]     → agent dreams from imagination only
  [present]    → agent reads via file tool, extracts context
  [too-large]  → model context window truncates naturally
```

## Validation Rules

- DayMemory path MUST match `memory/YYYY-MM-DD.md` pattern
- DayMemory is NEVER written by OpenDream (read-only constraint)
- DreamThought SHOULD reference DayMemory content when available (SC-001: 80% target)
- MorningRecall SHOULD trace at least one theme to DayMemory (SC-004)
