---
b1_id: B1-20260618T094846Z
phase_state: completed
source_raw: raw-20260618T094846Z
source_url: https://github.com/chatterzhao/freely/issues/2988
produced_candidate: C-20260618T094846Z-A
created_at: 2026-06-18
---

# B1_IBM: Update Three-Loop SVG — 五层架构重绘

## Input Source

- GitHub issue #2988: https://github.com/chatterzhao/freely/issues/2988
- Raw issue: `docs/B1-docs/raw-20260618T094846Z/issue.md`
- Filed by: platform (AI agent), 2026-06-18

## Problem

Current SVG only shows gate sequence (intake→routing→dispatch→test→pr-create→...), missing five core architecture layers:
ACP protocol layer, A2A protocol layer, Agent Role layer, Skill routing layer, Runtime execution layer.

## Brainstorming

### Option A: Incremental (add missing layers to existing gate-centric layout)
Fast but visually confusing — gates still dominate.

### Option B: Full restructure (Agent Role as top-level container)
Re-frame diagram from Agent Role perspective. Skills are loaded capability modules, gates are sub-structure. This better reflects implementation truth.

## Decision

**Option B: Full restructure.**

Agent Role-driven architecture with five execution layers and three distinguished loop mechanisms (code-level while-true, gate error→retry, Skill behavioral pattern).

## Candidate

- **candidate_id**: C-20260618T094846Z-A
- **status**: absorbed (doc-only change, absorbed into raw-20260618T094846Z)
- **absorbed_into**: raw-20260618T094846Z
- **milestone**: unassigned (doc-only)
