# Feature Specification: Token Analysis Document

**Feature Branch**: `002-token-analysis`
**Created**: 2026-04-07
**Status**: Draft
**Input**: User description: "can you do a token analysis document"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Understand Nightly Token Cost (Priority: P1)

A skill maintainer or agent operator wants to know the exact token cost of
running OpenDream for one night — broken down by tick, by input component, and
by model tier. Currently, rough estimates are scattered across ARCHITECTURE.md
(~2-5K tokens/tick, ~£0.01/night on Haiku) but there is no single document
that provides a rigorous breakdown. The operator needs this to decide which
model to assign to dream ticks, whether cost is acceptable, and where the
budget headroom is.

**Why this priority**: Cost visibility is the primary reason someone asks for a
token analysis. Without it, operators cannot make informed model selection
decisions or predict monthly spend.

**Independent Test**: Read the token analysis document. It should answer:
"How many tokens does one dream night cost on Haiku vs Sonnet vs local?" without
needing to consult any other file.

**Acceptance Scenarios**:

1. **Given** the token analysis document exists, **When** an operator reads it, **Then** they can determine the per-tick and per-night token count for both input and output, and the cost at each model tier.
2. **Given** a new model pricing tier becomes relevant, **When** an operator consults the document, **Then** the calculation method is clear enough for them to compute the cost themselves.

---

### User Story 2 — Identify Where Token Budget Is Spent (Priority: P2)

A skill developer wants to optimise OpenDream's token usage. They need a
per-component breakdown: how much of the tick budget goes to the HEARTBEAT.md
bootstrap, how much to prompts.yaml, how much to the memory file, how much to
the cycle file read, and how much to output. This helps identify where savings
are possible and where the ceiling is.

**Why this priority**: Without a component breakdown, a developer editing
prompts.yaml cannot assess the impact on token budget. Adding a few lines to
system_base might push a dense-memory tick over 5K.

**Independent Test**: Read the token analysis document. It should show a table
of per-component token counts with min/typical/max ranges and their percentage
of the 5K budget.

**Acceptance Scenarios**:

1. **Given** the token analysis document exists, **When** a developer reads the component breakdown, **Then** they can identify which component consumes the most tokens and where headroom exists.
2. **Given** a developer is considering adding context to prompts.yaml, **When** they consult the token analysis, **Then** they can calculate whether the addition stays within the <5K budget.

---

### User Story 3 — Validate Budget Compliance (Priority: P3)

The constitution mandates <5K tokens per tick and ~44K tokens total per night
(corrected from the original ~12K rough estimate based on measured file sizes).
A reviewer wants a document that proves (or flags violations of) these
constraints under different memory file densities (sparse, medium, dense).

**Why this priority**: Governance — the constitution's token constraints must be
verifiable. The document serves as the evidence that the constraint is met.

**Independent Test**: Read the token analysis document. It should have a
compliance section showing whether each scenario (no memory, sparse, medium,
dense) stays within the constitutional <5K/tick limit.

**Acceptance Scenarios**:

1. **Given** the token analysis document exists, **When** a reviewer checks for budget compliance, **Then** the document shows pass/fail for each memory density scenario against the <5K/tick and ~44K/night limits.
2. **Given** a future change pushes a scenario over budget, **When** the analysis is re-run, **Then** the document clearly flags the violation.

---

### Edge Cases

- What if the memory file is unusually large (e.g., a very busy day with 30+ entries)?
  The document should show the upper bound and note that the model's context window
  truncates naturally beyond a certain size.
- What if prompts.yaml grows significantly in a future update?
  The document should note the current prompts.yaml token count and provide the
  formula for recalculating headroom.
- What about the morning recall tick specifically?
  The morning recall reads ALL five cycle files plus optionally the memory file.
  Its input budget is different from a regular dream tick and should be analysed
  separately.

## Clarifications

### Session 2026-04-07

- Q: The constitutional ~12K tokens/night figure conflicts with the measured ~44K input total. How should compliance be reported? → A: Update the constitutional ~12K figure to ~44K and report compliance against the corrected number.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The token analysis MUST be a standalone document at `docs/TOKEN-ANALYSIS.md` — readable without consulting other files.
- **FR-002**: The analysis MUST break down token usage per component: HEARTBEAT.md bootstrap, system prompt overhead, prompts.yaml read, memory file read, cycle file read, and output generation.
- **FR-003**: The analysis MUST provide per-tick and per-night totals for both input tokens and output tokens.
- **FR-004**: The analysis MUST include cost estimates for at least three model tiers: local (free), budget (e.g., Haiku), and standard (e.g., Sonnet).
- **FR-005**: The analysis MUST show budget compliance against the constitutional constraints (<5K tokens/tick, ~44K tokens/night) for each memory density scenario (no memory, sparse, medium, dense). The ~44K nightly figure replaces the original rough ~12K estimate based on measured file sizes.
- **FR-006**: The analysis MUST separately analyse the morning recall tick, which has a different input profile (reads all 5 cycle files + optional memory file).
- **FR-007**: The analysis MUST include the calculation methodology so operators can recompute if files change.
- **FR-008**: The analysis MUST use measured file sizes from the actual skill files, not rough estimates.

### Key Entities

- **TickProfile**: The token breakdown for a single dream tick — input components, output, and total.
- **NightProfile**: The aggregate cost of all ticks in one dream night (14 dream + 1 morning recall).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator can determine the cost of one dream night on any model tier within 30 seconds of opening the document.
- **SC-002**: The component breakdown accounts for 100% of the per-tick token usage — no unattributed tokens.
- **SC-003**: The compliance section explicitly states pass/fail for each memory density scenario against constitutional limits.
- **SC-004**: The document includes at least one worked example showing how to recalculate if prompts.yaml changes size.

## Assumptions

- Token counts are estimated using the standard approximation of ~4 characters per token (English text in Markdown/YAML). Exact counts vary by model tokeniser.
- The HEARTBEAT.md bootstrap injection is the full file content. The system prompt overhead (tool schemas, rules) is not under OpenDream's control and is estimated as a flat overhead.
- Cycle files grow during the night — early ticks read short files, late ticks read longer ones. The analysis should use average cycle file size at mid-night.
- Output tokens are minimal (one dream thought: 8-20 words ≈ 10-25 tokens; morning recall: 2-3 sentences ≈ 60-90 tokens).
- Cost estimates use publicly available pricing. They will become outdated — the document should include the date of pricing and the formula so operators can recalculate.
