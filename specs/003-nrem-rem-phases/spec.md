# Feature Specification: NREM/REM Phase Mechanics

**Feature Branch**: `003-nrem-rem-phases`
**Created**: 2026-04-07
**Status**: Draft
**Input**: User description: "including NREM and REM phase mechanics for every cycle. OpenDream mirrors human sleep architecture. A full night consists of exactly 5 cycles spanning 23:00–06:00 local time. Each cycle contains two phases: Quiet phase (NREM-analogue) context gathering and Active phase (REM-analogue) — LLM generation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Two-Phase Tick Structure (Priority: P1)

Currently each dream tick does everything in one pass: reads context, then
generates a thought. Human sleep cycles have distinct phases — NREM (quiet,
restorative, context-processing) followed by REM (active, generative, dreaming).
OpenDream should mirror this by splitting each cycle's ticks into two explicit
phases:

- **Quiet phase (NREM-analogue)**: The agent gathers and processes context —
  reads prompts.yaml, reads the memory file, reads the current cycle file,
  extracts meaning. No dream output is generated. The agent replies
  HEARTBEAT_OK after completing context preparation.

- **Active phase (REM-analogue)**: The agent generates dream output — using
  the cycle's instruction, style, and examples to produce one dream thought.
  This is the creative, generative moment.

Each cycle already has multiple ticks within its time window. The first tick(s)
of each cycle should be designated as NREM (context gathering), and the
remaining tick(s) as REM (generation). This mirrors how human sleep cycles
begin with deep NREM sleep before transitioning into REM dreaming.

**Why this priority**: This is the core mechanic — without it, there are no
phases, just ticks. It defines how every cycle operates and all other stories
depend on it.

**Independent Test**: During a dream night, observe the cycle files. NREM ticks
should produce no dream output (only HEARTBEAT_OK). REM ticks should produce
dream thoughts. The cycle file should contain only thoughts from REM ticks.

**Acceptance Scenarios**:

1. **Given** a cycle has begun, **When** the first tick fires, **Then** the agent performs context gathering (reads prompts.yaml, memory file, cycle file) but does NOT write a dream thought — it replies HEARTBEAT_OK only.
2. **Given** the NREM tick(s) have completed, **When** the next tick fires, **Then** the agent generates one dream thought and appends it to the cycle file.
3. **Given** a cycle has 2 ticks total (e.g., Cycle 1: 23:00, 23:30), **When** the ticks fire, **Then** the first tick is NREM (no output) and the second tick is REM (one dream thought).
4. **Given** a cycle has 3 ticks total (e.g., Cycle 2: 00:00, 00:30, 01:00), **When** the ticks fire, **Then** the first tick is NREM (no output) and the remaining ticks are REM (one dream thought each).

---

### User Story 2 — Phase-Aware Cycle Schedule (Priority: P2)

The HEARTBEAT.md tick instructions must guide the agent to determine not just
which cycle it is in, but which phase. The agent uses the tick's position
within the cycle's time window to decide: first tick = NREM, subsequent
ticks = REM. This phase determination must be clear and unambiguous from the
time alone.

**Why this priority**: Without phase-aware scheduling, the agent cannot know
when to gather context vs when to generate. This is the scheduling logic that
makes US1 operational.

**Independent Test**: Read the HEARTBEAT.md instructions. For any given time
(e.g., 00:00), a reader should be able to determine: (1) the cycle, (2) the
phase (NREM or REM), and (3) what the agent should do.

**Acceptance Scenarios**:

1. **Given** the HEARTBEAT.md contains the phase schedule, **When** a tick fires at the start of any cycle's time window, **Then** the instructions unambiguously identify it as an NREM tick.
2. **Given** the HEARTBEAT.md contains the phase schedule, **When** a tick fires at a later time within a cycle's window, **Then** the instructions unambiguously identify it as a REM tick.
3. **Given** the phase schedule is defined, **When** all 14 dream ticks are enumerated, **Then** exactly 5 are NREM (one per cycle) and 9 are REM.

---

### User Story 3 — NREM Context Preparation Guidance (Priority: P3)

The NREM tick should not be a no-op. It should actively prepare context that
benefits the subsequent REM tick(s). The prompts.yaml should include guidance
for what the agent does during the quiet phase — scanning the memory file,
identifying themes relevant to this cycle's purpose, noting what to focus on.
This preparation makes the REM output better grounded.

**Why this priority**: Without NREM guidance, the quiet phase is just "skip
this tick." With guidance, it becomes the context-processing foundation that
improves dream quality. This is enhancement, not core mechanics.

**Independent Test**: Read the NREM guidance in prompts.yaml. It should describe
what the agent does during the quiet phase for each cycle type. The agent should
be able to follow the guidance without ambiguity.

**Acceptance Scenarios**:

1. **Given** prompts.yaml contains NREM guidance, **When** the agent executes an NREM tick, **Then** it reads context files and processes them according to the guidance — without generating output.
2. **Given** the NREM guidance exists for each cycle, **When** the guidance is read, **Then** it describes cycle-specific context preparation (e.g., Cycle 1 NREM scans for emotional friction, Cycle 4 NREM identifies what to keep vs release).

---

### Edge Cases

- What if the gateway fires a tick at an unexpected time (e.g., 23:15)?
  The agent determines the cycle from HEARTBEAT.md's time windows. A tick at
  23:15 falls within Cycle 1 (23:00–00:00). Since it is not the first tick
  of the cycle (23:00 was), it should be treated as REM.
- What about the morning recall tick (06:00)?
  The morning recall tick is outside the 5-cycle structure and follows its
  existing logic unchanged. It is neither NREM nor REM — it is the recall
  synthesis. No change needed.
- What if the first tick of a cycle is missed (e.g., gateway was offline)?
  If the agent has no record of an NREM tick for this cycle (no thoughts in
  the cycle file, and this is the first tick in the window), it should still
  perform NREM. The determination is based on position in the time window,
  not on whether a previous tick actually executed.
- What happens to the dream thought count per night?
  Currently: 14 dream ticks → 14 thoughts. With NREM/REM: 5 NREM ticks
  produce no output + 9 REM ticks produce 9 thoughts. The nightly thought
  count drops from 14 to 9. This is intentional — fewer but better-grounded
  thoughts.
- What if the memory file (`memory/YYYY-MM-DD.md`) is missing or empty?
  The NREM tick still executes its full quiet phase. It reads prompts.yaml
  and the cycle file (if any), appends its `<!-- NREM -->` marker, and
  replies HEARTBEAT_OK. The phase structure is maintained regardless of
  context availability — sleep architecture is unconditional.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each of the 5 dream cycles MUST contain exactly two phases: a Quiet phase (NREM-analogue) and an Active phase (REM-analogue), executed in that order.
- **FR-002**: The first tick of each cycle's time window MUST be designated as the NREM phase. All subsequent ticks within that cycle MUST be designated as REM.
- **FR-003**: During an NREM tick, the agent MUST perform context gathering (read prompts.yaml, read memory file, read cycle file) and MUST NOT generate a dream thought. It MUST append a silent HTML comment marker (e.g., `<!-- NREM 23:00 -->`) to the cycle file to record that the tick occurred.
- **FR-004**: During a REM tick, the agent MUST generate one dream thought following the cycle's instruction, style, and examples, and append it to the cycle file.
- **FR-005**: The HEARTBEAT.md tick instructions MUST include the phase schedule so the agent can determine NREM vs REM from the current time alone.
- **FR-006**: The phase split MUST produce exactly 5 NREM ticks and 9 REM ticks per night (one NREM per cycle, remaining ticks as REM).
- **FR-007**: The morning recall tick (06:00) MUST remain unchanged — it is outside the NREM/REM phase structure.
- **FR-008**: The prompts.yaml MUST include NREM-specific guidance for context preparation during the quiet phase.
- **FR-009**: The total nightly dream thought count MUST change from 14 to 9 (reflecting the 5 ticks now designated as NREM).
- **FR-010**: Each cycle in prompts.yaml MUST include a `depth` attribute that guides progressive dream vividness: `shallow` (Cycle 1), `emerging` (Cycle 2), `deep` (Cycle 3), `expansive` (Cycle 4), `vivid` (Cycle 5).
- **FR-011**: REM tick output length MUST scale progressively across cycles — Cycle 1 REM produces shorter thoughts (8-12 words), while Cycle 5 REM produces longer thoughts (15-25 words) — mirroring the physiological pattern where dreams grow longer and more vivid toward morning. The `system_base` global word limit MUST be widened from "8-20 words" to "8-25 words" to accommodate this scaling.

### Key Entities

- **Phase**: Either `NREM` (quiet — context gathering, no output) or `REM` (active — dream generation). Each cycle contains one NREM tick followed by one or more REM ticks.
- **CyclePhaseSchedule**: The mapping of each tick time to its cycle number and phase designation.
- **Depth**: A per-cycle attribute encoding progressive dream intensity — `shallow`, `emerging`, `deep`, `expansive`, `vivid` (Cycles 1-5). Guides both vividness of imagery and output length scaling.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every dream cycle produces exactly one NREM tick (no output) followed by one or more REM ticks (dream thoughts), verified by examining dream output files.
- **SC-002**: The nightly dream output contains exactly 9 dream thoughts (down from 14), distributed across 5 cycle files.
- **SC-003**: A reader of HEARTBEAT.md can determine the phase (NREM or REM) of any tick from the time alone, without consulting other files.
- **SC-004**: NREM ticks complete successfully (HEARTBEAT_OK) and write only a silent HTML comment marker to the cycle file — no visible dream content.

## Clarifications

### Session 2026-04-07

- Q: Should later cycles produce progressively longer or more vivid dream thoughts than early cycles? → A: Yes — add both explicit output-length scaling (Cycle 1 shorter, Cycle 5 longer) and a `depth` attribute per cycle in prompts.yaml to guide vividness.
- Q: Should NREM ticks leave an observable marker? → A: Yes — append a silent HTML comment (e.g., `<!-- NREM 23:00 -->`) to the cycle file so the tick is logged without visible dream output.
- Q: Should `system_base` word count be updated to accommodate progressive output-length scaling? → A: Yes — widen `system_base` to "8-25 words" and let each cycle's `depth` attribute and instruction enforce the per-cycle range within that ceiling.
- Q: Should NREM ticks be skipped when no daily memory file exists? → A: No — always execute NREM; the phase is structural (mirroring sleep architecture), not conditional on context availability.
- Q: What should the canonical `depth` values be per cycle? → A: `shallow` (Cycle 1), `emerging` (Cycle 2), `deep` (Cycle 3), `expansive` (Cycle 4), `vivid` (Cycle 5) — mapping 1:1 to the physiological progression from short/shallow to longest/most vivid.

## Assumptions

- The gateway's 30-minute tick interval is unchanged. The phase split uses the existing tick schedule — no new ticks are added or removed.
- The first tick in each cycle's window is always NREM, regardless of whether previous ticks were missed or delayed.
- NREM context gathering happens in the same `isolatedSession` as any other tick. Since sessions are isolated, the context gathered during NREM is not preserved for the subsequent REM tick — each tick must still read its own context. The NREM phase's value is structural (mirroring sleep architecture) rather than data-passing.
- The Token Analysis document (`docs/TOKEN-ANALYSIS.md`) will need updating: NREM ticks have lower token cost (no output), and the total nightly output drops from ~252 to ~162 tokens (9 thoughts × ~18 tokens).
- Cycle 1 has 2 ticks (1 NREM + 1 REM = 1 thought). Cycles 2–5 have 3 ticks each (1 NREM + 2 REM = 2 thoughts each). Total: 1 + 2 + 2 + 2 + 2 = 9 thoughts.
- Cycle durations follow the physiological pattern: Cycle 1 (~60 min, short/shallow), Cycles 2-5 (~90 min, progressively deeper/more vivid). The `depth` attribute and output-length scaling encode this progression.
