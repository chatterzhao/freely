# Brainstorm: platform-adapter key standardization
- 来源: raw-20260508T121541Z (#257)
## Discovery
pull_raw_issue 用 created_at 覆盖标题中的 canonical key，导致 key 不一致。
## Decision
标题已有 raw-{key} 时跳过标准化。
