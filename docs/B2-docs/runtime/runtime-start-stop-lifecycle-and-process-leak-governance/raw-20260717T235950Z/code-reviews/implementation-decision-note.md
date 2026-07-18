# Implementation Decision Note
- issue_id: I-20260717T235950Z-A

## Implementation Decision Note
- decision: commands.md --force 行一行同步 usage() 的 autonomous gate 语义。
- why_this: usage() 是随代码走门禁的真源，commands.md 是速查引用面，同步而非重写。
- alternatives_considered: 删除选项表改指 --help——速查价值丢失，拒绝。
- boundary_non_goals: 不改 wt-close 代码；不动 L35/L182 场景示例行；不重构 commands.md 结构。
- residual_risk: 未来 usage() 再变仍需人工同步——已由 at005-usage-sync.sh（#3984 合入）锚定 --help 侧关键词，doc 侧本 lane 的 harness 可复用做回归。
