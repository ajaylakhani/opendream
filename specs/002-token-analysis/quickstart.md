# Quickstart: Token Analysis Document

**Feature**: 002-token-analysis

## What This Feature Delivers

A standalone document at `docs/TOKEN-ANALYSIS.md` that provides:

1. **Per-tick token breakdown** — every input component measured and accounted for
2. **Per-night cost by model tier** — local (free), Haiku (~£0.01), Sonnet (~£0.15)
3. **Budget compliance verification** — pass/fail for 4 memory density scenarios
4. **Calculation methodology** — operators can recompute if files change

## Key Numbers (from research)

| Component | Tokens |
|-----------|-------:|
| System overhead | ~300 |
| HEARTBEAT.md bootstrap | ~449 |
| Heartbeat prompt | ~30 |
| prompts.yaml read | ~2,015 |
| Memory file (dense) | ~303 |
| Cycle file read (mid-night) | ~100 |
| **Dream tick total** | **~3,200** |
| Output per dream tick | ~20 |

Budget headroom at dense memory: ~1,800 tokens (36% of 5K limit).

## What Changes

| Action | File | Details |
|--------|------|---------|
| CREATE | `docs/TOKEN-ANALYSIS.md` | New standalone analysis document |
| UPDATE | `docs/ARCHITECTURE.md` | Add cross-reference to TOKEN-ANALYSIS.md in cost section |

No code changes. No config changes. No runtime impact.
