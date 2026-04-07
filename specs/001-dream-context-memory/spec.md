# Feature Specification: DreamContext Memory File

**Feature Branch**: `001-dream-context-memory`
**Created**: 2026-04-07
**Status**: Draft
**Input**: User description: "Create spec and validate the OpenDream DreamContext memory/YYYY-MM-DD.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Dream Tick Reads Today's Context (Priority: P1)

During a dream heartbeat tick (23:00–06:00), the agent reads `memory/YYYY-MM-DD.md`
to ground its dream thoughts in what actually happened today. Without this file,
dream output is generic and disconnected from the agent's lived experience.

The agent already references this file at step 2 of every tick in HEARTBEAT.md:
"Use file tools to read `memory/YYYY-MM-DD.md` for today's context (skip if missing)."
Currently the file's structure, content expectations, and population method are
undefined. This story defines them.

**Why this priority**: This is the core purpose of the file — it exists to feed
dream cycles. Without a defined structure, the agent cannot reliably extract
people, events, friction, or tasks from the day.

**Independent Test**: Create a sample `memory/2026-04-07.md` with the defined
structure. Run a simulated dream tick for Cycle 1 (Emotional Review). Verify
the agent references specific content from the file in its dream thought rather
than producing a generic output.

**Acceptance Scenarios**:

1. **Given** a `memory/2026-04-07.md` exists with at least one interaction entry, **When** a dream tick fires during Cycle 1, **Then** the agent reads the file and produces a dream thought that references specific content from the day.
2. **Given** no `memory/2026-04-07.md` exists, **When** a dream tick fires, **Then** the agent skips the read gracefully (no error) and generates a dream thought from longer-term memory or imagination only.
3. **Given** a `memory/2026-04-07.md` exists with multiple entries spanning different categories (interactions, tasks, observations), **When** the agent is in Cycle 2 (Creative Association), **Then** it draws cross-references between unrelated entries from the file.

---

### User Story 2 — Dream Quality with Varied Native Memory Content (Priority: P2)

OpenClaw natively writes `memory/YYYY-MM-DD.md` during daytime sessions. The
content, structure, and density of these native entries vary. OpenDream must
produce meaningful dream output regardless of what OpenClaw writes — from sparse
notes to dense detail — by extracting people, friction, tasks, and observations
from whatever format it finds.

**Why this priority**: OpenDream cannot control what OpenClaw writes. Dream
quality depends on the agent's ability to parse and extract context from
varying native memory content. This story validates resilience.

**Independent Test**: Create three sample `memory/YYYY-MM-DD.md` files with
different densities (1 entry, 5 entries, 15 entries). Run dream ticks against
each. Verify dream thoughts reference specific content in all three cases and
scale appropriately.

**Acceptance Scenarios**:

1. **Given** a native memory file with a single brief entry, **When** a dream tick fires, **Then** the agent still produces a grounded dream thought referencing that entry rather than falling back to generic output.
2. **Given** a native memory file with 15+ entries covering multiple topics, **When** the agent is in Cycle 2 (Creative Association), **Then** it selects and cross-references entries rather than being overwhelmed by volume.
3. **Given** a native memory file with unstructured prose (no categories, no timestamps), **When** a dream tick fires, **Then** the agent extracts meaningful context and produces a relevant dream thought.

---

### User Story 3 — Morning Recall References Day Context (Priority: P3)

At 06:00, the agent writes a morning recall summarising the night. The morning
note should connect dream processing back to the day's context — what friction
was resolved, what patterns were noticed relative to actual events.

**Why this priority**: The morning recall is the visible output of dreaming. Its
quality depends on the dream thoughts, which in turn depend on the memory file.
This story validates the end-to-end chain.

**Independent Test**: Populate a `memory/YYYY-MM-DD.md` with known entries. Run
all five dream cycles. Generate the morning recall. Verify the morning recall
references themes that trace back to specific entries in the memory file.

**Acceptance Scenarios**:

1. **Given** a night of dreaming with a populated memory file, **When** the agent writes the morning recall at 06:00, **Then** the note MAY reference themes traceable to the day's context entries — but is not required to. Like human dream recall, the connection may be clear, faint, or absent.
2. **Given** a night of dreaming with no memory file (empty day), **When** the agent writes the morning recall, **Then** the note summarises dream content alone without acknowledging any absence.

---

### Edge Cases

- What happens when the memory file is malformed or contains only whitespace?
  The agent treats it as empty (same as missing) and proceeds without error.
- What happens when the memory file is very large (many entries in a busy day)?
  The agent reads the full file; the heartbeat's token budget (~5K tokens total
  per tick) naturally limits how much context fits. Entries should be concise
  enough that a full day's worth stays within readable limits.
- What happens when two heartbeat ticks fire in rapid succession and both try
  to read the same memory file? No conflict — the file is read-only during
  dream ticks. Only daytime ticks write to it.
- What happens if the agent appends to yesterday's memory file after midnight
  during a late-night session that extends into the dream window? The file
  date is determined by when the interaction occurred. Dream ticks always read
  today's date (the date the dream window opened, i.e., the date at 23:00).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The memory file MUST be located at `memory/YYYY-MM-DD.md` where `YYYY-MM-DD` is the calendar date, relative to the workspace root.
- **FR-002**: OpenDream MUST treat the native memory file as read-only. It MUST NOT write to, modify, or impose structure on `memory/YYYY-MM-DD.md`.
- **FR-003**: OpenDream MUST extract meaningful context (people, friction, tasks, observations) from the native memory file regardless of its format or structure.
- **FR-004**: OpenDream MUST handle memory files of varying density — from a single entry to 15+ entries — without degradation of dream quality.
- **FR-005**: OpenDream MUST gracefully handle unstructured or free-form native memory content (no categories, no timestamps).
- **FR-006**: During dream ticks, the agent MUST read the file using file tools (not bootstrap injection) and skip gracefully if the file is missing. The agent MUST NOT read `MEMORY.md` during dream ticks — only the daily `memory/YYYY-MM-DD.md` file.
- **FR-007**: OpenDream MUST NOT write to the memory file during the dream window (23:00–06:00) or at any other time.
- **FR-008**: OpenDream MUST tolerate memory files of any size up to the heartbeat tick's token budget (~5K tokens total per tick including prompt overhead).
- **FR-009**: OpenDream MUST NOT log or echo sensitive data from the memory file into dream output files.

### Key Entities

- **DayMemory**: A native OpenClaw daily notes file at `memory/YYYY-MM-DD.md`. Written by OpenClaw during daytime sessions. Format and structure are OpenClaw-defined and may vary.
- **DreamContext**: The read-only view of a DayMemory consumed by OpenDream during dream ticks. The agent reads this file via tool call and extracts people, events, friction, and tasks to ground dream thoughts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 80% of dream thoughts in Cycles 1–3 reference specific content from the day's memory file (when the file exists and contains at least 3 entries).
- **SC-002**: Dream thoughts referencing native memory content are distinguishable from generic/imagination-only thoughts by a human reviewer.
- **SC-003**: A human reading the memory file can understand the shape of the agent's day in under 60 seconds.
- **SC-004**: Morning recall MAY demonstrate thematic continuity with the day's memory file when one exists, but is not required to. This mirrors human dream recall — sometimes you know what triggered the dream, sometimes you just remember fragments with no clear origin.
- **SC-005**: The memory file for a full day of typical agent activity stays under 2,000 words, keeping it within the heartbeat tick's token budget.

## Assumptions

- The `memory/` directory already exists in the workspace (or will be created alongside `dreams/` during OpenDream setup).
- `memory/YYYY-MM-DD.md` is a **native OpenClaw feature** — OpenClaw writes daily notes during normal DM sessions. OpenDream is a read-only consumer of this file.
- OpenClaw auto-loads today's and yesterday's daily notes into DM session context. During dream ticks (`lightContext: true`), the file is NOT auto-loaded — the agent reads it via file tools.
- `MEMORY.md` (the longer-term memory file referenced in SKILL.md) is a separate concern and out of scope for this feature. This spec covers only the daily `memory/YYYY-MM-DD.md` file.
- The host gateway (OpenClaw or Hermes) provides file read/write tools that the agent can use during dream ticks.
- Date boundaries follow the agent's configured timezone (from `openclaw.json` `activeHours.timezone`), not UTC.

## Clarifications

### Session 2026-04-07

- Q: Does OpenDream define and write the memory file, or read the native OpenClaw daily memory file? → A: OpenDream reads the native OpenClaw `memory/YYYY-MM-DD.md`. It does not write the file.
- Q: Should the morning recall be required to trace themes back to the day's memory file? → A: No. Optional — trace back if the connection is natural, but don't force it. Mirrors human dream recall: sometimes you know what triggered the dream, sometimes you just remember fragments.
- Q: Should dream ticks also read `MEMORY.md` (long-term memory) via file tools? → A: No. Daily file only — `MEMORY.md` is too large for the tick token budget and not needed for dream grounding.
- Q: Rename "morning note" terminology to what? → A: `morning_recall` everywhere — labels, YAML keys, CSS classes, event names, filenames (`morning-recall.md`).
