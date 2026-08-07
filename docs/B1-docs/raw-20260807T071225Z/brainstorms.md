---
b1_id: B1-20260807T071225Z
phase_state: completed
source_raw: raw-20260807T071225Z
source_url: https://github.com/chatterzhao/freely/issues/4094
produced_candidate: C-20260807T071225Z-A
created_at: 2026-08-07T07:20:00Z
---

# B1_IBM: scan parse_frontmatter 无法解析嵌套 platform_ids

## Input

- 现象：7 个 strict raw（schema_version 1）被 scan 误报 2a_invalid_raw_metadata。
- 根因：`parse_frontmatter` 用简单行解析，嵌套 YAML（platform_ids 子键）被当顶层字段；flow 单行被当字符串。

## Brainstorm

- Option A：改文件格式规避（flow 单行）→ platform_ids 变字符串，不解决。
- Option B：修 parse_frontmatter（yaml.safe_load 优先 + 行解析 fallback）→ 正确解析嵌套，兼容 bullet 混合格式。采用。

## Decision

Option B：parse_frontmatter 优先 yaml.safe_load（严格 YAML 正确处理嵌套），失败回退行解析 + bullet 补充。

## Candidate

- candidate_id: `C-20260807T071225Z-A`
- status: promoted
- milestone: `M-20260807T071225Z-A`
