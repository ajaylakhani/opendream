# Data Model: Token Analysis Document

**Feature**: 002-token-analysis
**Date**: 2026-04-07

## Entities

### TickProfile

The token breakdown for a single tick execution.

| Field | Type | Description |
|-------|------|-------------|
| tick_type | enum | `dream` or `morning_recall` |
| system_overhead | integer | Tokens from system prompt + tool schemas (~200-400) |
| heartbeat_bootstrap | integer | Tokens from HEARTBEAT.md injection (~449) |
| heartbeat_prompt | integer | Tokens from custom prompt string (~30) |
| prompts_yaml_read | integer | Tokens from prompts.yaml file read (~2,015) |
| memory_file_read | integer | Tokens from memory/YYYY-MM-DD.md read (0-303+) |
| cycle_file_read | integer | Tokens from current cycle file read (0-350) |
| input_total | integer | Sum of all input components |
| output_tokens | integer | Tokens generated as output (10-25 dream, 60-90 recall) |

**Validation rules**:
- `input_total` MUST equal the sum of all input components
- `input_total` MUST be < 5,000 (constitutional constraint)
- `output_tokens` is significantly smaller than input for dream ticks

**Relationships**:
- A NightProfile contains 14 dream TickProfiles + 1 morning_recall TickProfile

### NightProfile

The aggregate cost of all ticks in one dream night.

| Field | Type | Description |
|-------|------|-------------|
| dream_ticks | integer | Always 14 |
| morning_recall_ticks | integer | Always 1 |
| total_input_tokens | integer | Sum of all tick input totals |
| total_output_tokens | integer | Sum of all tick outputs |
| total_tokens | integer | input + output |
| cost_local | decimal | Always £0.00 |
| cost_budget | decimal | Cost at budget model pricing |
| cost_standard | decimal | Cost at standard model pricing |

**Validation rules**:
- `total_tokens` MUST equal `total_input_tokens` + `total_output_tokens`
- `dream_ticks` is always 14, `morning_recall_ticks` is always 1

### MemoryDensityScenario

A compliance test case for a specific memory file density.

| Field | Type | Description |
|-------|------|-------------|
| scenario_name | string | `none`, `sparse`, `medium`, `dense` |
| memory_bytes | integer | Size of memory file in bytes |
| memory_tokens | integer | Estimated token count |
| tick_input_total | integer | Total input tokens for a dream tick in this scenario |
| budget_limit | integer | Constitutional limit (5,000) |
| headroom | integer | `budget_limit` - `tick_input_total` |
| compliance | enum | `PASS` if headroom > 0, `FAIL` otherwise |

**State transitions**: None — these are static analysis results.
