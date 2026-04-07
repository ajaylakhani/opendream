# Research: Token Analysis Document

**Feature**: 002-token-analysis
**Date**: 2026-04-07
**Status**: Complete

## R1: Token Estimation Methodology

**Decision**: Use ~4 characters per token as the estimation heuristic for English
Markdown/YAML content.

**Rationale**: This is the widely-accepted approximation for GPT/Claude-family
tokenizers on English text. OpenDream content is Markdown + YAML — primarily English
prose with light formatting. The heuristic is sufficient for budget planning since
exact counts vary by tokenizer (cl100k_base, Claude's tokenizer, etc.) but converge
within ±15% for English text.

**Alternatives considered**:
- Exact tokenizer counting (e.g., `tiktoken` for OpenAI, custom for Claude): More
  precise but adds a Python dependency for a documentation artifact. Overkill
  for budget estimation.
- Conservative ~3 chars/token: Would overestimate by ~25%, making budgets look
  tighter than reality. Rejected for being unnecessarily pessimistic.

---

## R2: What Counts as "Input" for a Dream Tick

**Decision**: Input tokens for a dream tick include:

1. **System prompt overhead** — Tool schemas, system rules injected by the gateway.
   Not under OpenDream's control. Estimated as a flat ~200-400 token overhead.
2. **HEARTBEAT.md bootstrap** — The full HEARTBEAT.md (including the dream section)
   injected via `lightContext: true`. Only the dream-relevant portion is the
   `HEARTBEAT-dream-section.md` asset (~449 tokens), but the full HEARTBEAT.md
   includes other sections too.
3. **Heartbeat prompt** — The custom prompt string from openclaw.json (~30 tokens).
4. **prompts.yaml read** — Read via file tool (~2,015 tokens for full file).
5. **memory/YYYY-MM-DD.md read** — Read via file tool (0-303+ tokens depending on
   density).
6. **Cycle file read** — Current cycle's dream file, grows during the night (0-200
   tokens estimated for mid-night).

**Rationale**: The `lightContext + isolatedSession` config means the input is
deterministic and measurable. Items 1 and 3 are fixed overhead. Items 4-6 are
per-tick variable costs read via tool calls.

**Alternatives considered**:
- Including SKILL.md in the budget: Not applicable — `lightContext: true` strips
  skills from bootstrap. SKILL.md is only loaded during daytime conversations.
- Including conversation history: Not applicable — `isolatedSession: true` means
  no history carry-over between ticks.

---

## R3: Morning Recall Tick — Different Input Profile

**Decision**: The morning recall tick has a significantly different input profile
from regular dream ticks and must be analysed separately.

**Morning recall input**:
1. System prompt overhead (~200-400 tokens) — same as dream tick
2. HEARTBEAT.md bootstrap (~449 tokens) — same as dream tick
3. Heartbeat prompt (~30 tokens) — same as dream tick
4. prompts.yaml read (~2,015 tokens) — same as dream tick, reads `morning_recall` section
5. All 5 cycle files (~14 dream thoughts at ~15-25 tokens each ≈ 210-350 tokens total)
6. Optional memory/YYYY-MM-DD.md read (0-303+ tokens)

The morning recall tick reads more files (all 5 cycle outputs) but produces a longer
output (2-3 sentences ≈ 60-90 tokens vs 8-20 words ≈ 10-25 tokens).

**Rationale**: The spec (FR-006) explicitly requires separate analysis. The morning
recall's input is ~200-350 tokens heavier than a dream tick due to reading all 5
cycle files.

---

## R4: Cost Estimation — Model Pricing Tiers

**Decision**: Use three model tiers for cost estimation:

| Tier | Model Example | Input $/M tokens | Output $/M tokens |
|------|---------------|------------------:|-------------------:|
| Local | Ollama (any) | £0 | £0 |
| Budget | Claude Haiku | ~$0.25/M in | ~$1.25/M out |
| Standard | Claude Sonnet | ~$3.00/M in | ~$15.00/M out |

**Rationale**: These are the most likely models operators will assign to dream ticks.
Local is free. Haiku is the practical choice for low-cost cloud operation. Sonnet is
the upper bound for operators who want higher-quality dream output.

**Alternatives considered**:
- Including GPT-4o-mini / GPT-4o: Valid but OpenClaw/Hermes primarily supports
  Anthropic models. Can be added later.
- Including exact per-model pricing: Prices change frequently. The document should
  include the formula and date, not hardcoded prices.

---

## R5: Budget Headroom and Compliance Verification

**Decision**: The compliance section should test 4 scenarios against the constitutional
<5K/tick limit:

| Scenario | Memory tokens | Expected total |
|----------|-------------:|---------------:|
| No memory file | 0 | ~2,700 tokens |
| Sparse memory | ~22 | ~2,720 tokens |
| Medium memory | ~102 | ~2,800 tokens |
| Dense memory | ~303 | ~3,000 tokens |

All scenarios are well within the <5K budget, giving ~2K tokens of headroom even in
the densest case.

For the nightly limit: 14 dream ticks × ~2,800 avg + 1 morning recall × ~3,100
= ~42,300 tokens. The original ~12K estimate in ARCHITECTURE.md was a rough
calculation. Per clarification (2026-04-07), the constitutional figure has been
corrected to ~44K tokens/night based on measured data. All scenarios pass against
this corrected limit.
token count per night is ~40-45K tokens. The *cost* at Haiku pricing is still ~£0.01,
which aligns with the ARCHITECTURE.md cost estimate. The document should clarify this
distinction.

**Rationale**: The 4-scenario approach directly maps to the test fixtures
(memory-sparse.md, memory-medium.md, memory-dense.md) and the "no memory" edge case.
